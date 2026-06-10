#!/usr/bin/env python3
"""
拆 posts.js → posts-manifest.js + posts-1.js + posts-2.js + ...

设计:
- manifest: 轻量元数据 (无 body), 含 id/date/time/title/summary/tags/page
- posts-N.js: 每页 9 条全文 (含 body)
- 排序: 按 date 倒序, 同 date 按 time 倒序 (跟 index.html 原 sort 一致)
- 命名: page 1 = 最新 9 条

用法:
    python3 split_posts.py                 # 拆 + 输出
    python3 split_posts.py --page-size 12  # 自定义每页条数
"""
import re
import json
import sys
from pathlib import Path

POSTS_JS = Path(__file__).parent / 'posts.js'
PAGE_SIZE = 9


def load_posts():
    """读 posts.js, 拿 POSTS 数组 (用 node 跑, 避免 U+2014 eval 错)."""
    import subprocess
    r = subprocess.run(
        ['node', '-e', '''
const fs = require('fs');
const c = fs.readFileSync('posts.js', 'utf-8');
const fn = new Function(c.replace('window.HERMES_POSTS = POSTS;', 'return POSTS;'));
const POSTS = fn();
process.stdout.write(JSON.stringify(POSTS));
'''],
        cwd=POSTS_JS.parent,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(r.stdout)


def sort_posts(posts):
    """跟 index.html 现有 sort 一致: date 倒序, 同 date 按 time 倒序."""
    return sorted(
        posts,
        key=lambda p: (p['date'], p.get('time', '00:00')),
        reverse=True,
    )


def split_pages(posts, page_size):
    """按 page_size 切分."""
    pages = []
    for i in range(0, len(posts), page_size):
        pages.append(posts[i:i + page_size])
    return pages


def make_manifest(posts, pages, page_size):
    """manifest: 轻量元数据 + page 映射."""
    page_of = {}
    for idx, page in enumerate(pages, 1):
        for p in page:
            page_of[p['id']] = idx
    manifest_posts = [
        {
            'id': p['id'],
            'date': p['date'],
            'time': p.get('time', '00:00'),
            'title': p['title'],
            'summary': p['summary'],
            'tags': p['tags'],
            'page': page_of[p['id']],
        }
        for p in posts
    ]
    return {
        'totalPosts': len(posts),
        'pageSize': page_size,
        'totalPages': len(pages),
        'generatedAt': __import__('datetime').datetime.now().isoformat(timespec='seconds'),
        'posts': manifest_posts,
    }


def js_escape(s):
    """JS template literal 字符串转义: 反引号 + ${} + 反斜杠."""
    if not isinstance(s, str):
        s = str(s)
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')


def js_stringify(value, indent=0):
    """递归把 Python 值转成 JS 字面量, 用于写到 .js 文件."""
    pad = '  ' * indent
    npad = '  ' * (indent + 1)
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return '`' + js_escape(value) + '`'
    if isinstance(value, list):
        if not value:
            return '[]'
        items = [npad + js_stringify(v, indent + 1) + ',' for v in value]
        return '[\n' + '\n'.join(items) + '\n' + pad + ']'
    if isinstance(value, dict):
        if not value:
            return '{}'
        items = []
        for k, v in value.items():
            # 键名: 只接受标识符样式, 否则用引号
            if re.match(r'^[A-Za-z_$][A-Za-z0-9_$]*$', k):
                key = k
            else:
                key = '`' + js_escape(k) + '`'
            items.append(f'{npad}{key}: {js_stringify(v, indent + 1)},')
        return '{\n' + '\n'.join(items) + '\n' + pad + '}'
    raise TypeError(f'不支持的类型: {type(value)}')


def write_manifest(manifest, path):
    """写 posts-manifest.js."""
    content = (
        '// Hermes Agent 笔记 — 轻量 manifest (无 body)\n'
        f'// 生成于 {manifest["generatedAt"]} | 总 {manifest["totalPosts"]} 条 | '
        f'每页 {manifest["pageSize"]} 条 | 共 {manifest["totalPages"]} 页\n'
        '// 主页用: totalPosts/totalPages + 渲染卡片 (title/summary/tags)\n'
        '// 详情页用: 查 id → page 字段 → fetch 对应 posts-N.js\n'
        'window.HERMES_MANIFEST = '
        + js_stringify(manifest, 0)
        + ';\n'
    )
    path.write_text(content, encoding='utf-8')
    return len(content)


def write_page(posts, page_no, path):
    """写 posts-N.js."""
    content = (
        f'// Hermes Agent 笔记 — 第 {page_no} 页 (共 {len(posts)} 条)\n'
        f'// 加载方式: <script src="posts-{page_no}.js"></script> 或 fetch + new Function\n'
        f'window.HERMES_PAGE_{page_no} = '
        + js_stringify(posts, 0)
        + ';\n'
    )
    path.write_text(content, encoding='utf-8')
    return len(content)


def main():
    page_size = PAGE_SIZE
    if '--page-size' in sys.argv:
        idx = sys.argv.index('--page-size')
        page_size = int(sys.argv[idx + 1])

    posts = load_posts()
    posts = sort_posts(posts)
    pages = split_pages(posts, page_size)
    manifest = make_manifest(posts, pages, page_size)

    base = POSTS_JS.parent
    files = []

    # manifest
    mpath = base / 'posts-manifest.js'
    sz = write_manifest(manifest, mpath)
    files.append((mpath.name, sz, manifest['totalPosts']))

    # pages
    for i, page_posts in enumerate(pages, 1):
        ppath = base / f'posts-{i}.js'
        sz = write_page(page_posts, i, ppath)
        files.append((ppath.name, sz, len(page_posts)))

    # 输出汇总
    print(f'✅ 拆页完成: 总 {manifest["totalPosts"]} 条 / {manifest["totalPages"]} 页 (每页 {page_size} 条)')
    print()
    print(f'{"文件":<24} {"大小":>8}  {"条目":>6}')
    print('-' * 44)
    for name, sz, cnt in files:
        print(f'{name:<24} {sz:>6} B  {cnt:>6}')

    # 总大小对比
    total = sum(sz for _, sz, _ in files)
    orig = POSTS_JS.stat().st_size
    delta = total - orig
    print('-' * 44)
    print(f'{"合计":<24} {total:>6} B')
    print(f'原 posts.js: {orig} B  (Δ {delta:+d} B)')


if __name__ == '__main__':
    main()
