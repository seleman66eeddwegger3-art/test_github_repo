#!/usr/bin/env python3
"""Simple markdown to HTML converter for academic text."""

import re
import sys

def extract_footnotes(content):
    """Extract all footnote definitions from markdown content."""
    footnotes = {}
    lines = content.split('\n')
    current_key = None
    current_text = []
    
    for line in lines:
        m = re.match(r'\[\^(\d+)\]:\s*\*\*(.+?)\*\*', line)
        if m:
            if current_key:
                footnotes[current_key] = ' '.join(current_text)
            current_key = m.group(1)
            rest = line[m.end():].strip()
            if rest.startswith('——'):
                current_text = [m.group(2) + rest]
            else:
                current_text = [m.group(2) + rest] if rest else [m.group(2)]
        elif current_key and line.strip() and not line.startswith('##') and not line.startswith('---'):
            if line.startswith('[^'):
                footnotes[current_key] = ' '.join(current_text)
                current_key = None
                current_text = []
            else:
                current_text.append(line.strip())
        else:
            if current_key:
                footnotes[current_key] = ' '.join(current_text)
            current_key = None
            current_text = []
    
    if current_key:
        footnotes[current_key] = ' '.join(current_text)
    
    return footnotes


def simple_convert(markdown_content, footnotes):
    """Simple conversion focusing on structure."""
    
    lines = markdown_content.split('\n')
    html_lines = []
    
    in_editor_note = False
    in_dedication = False
    
    def convert_footnote_refs(text):
        def replacer(m):
            num = m.group(1)
            if num in footnotes:
                return f'<sup class="footnote-ref" onclick="showFootnote(this,{num})">[{num}]</sup>'
            return m.group(0)
        return re.sub(r'\[\^(\d+)\]', replacer, text)
    
    for line in lines:
        if '进度记录' in line or '下一块' in line:
            continue
        
        if re.match(r'\[\^(\d+)\]:', line):
            continue
            
        if re.match(r'^[一二三四五六七八九十]+、', line):
            continue
            
        if line.startswith('# 《'):
            continue
        
        if line.startswith('## 编者说明'):
            in_editor_note = True
            html_lines.append('<div class="editor-note">')
            continue
            
        if in_editor_note:
            if line.startswith('---') or (line.startswith('##') and '编者说明' not in line):
                in_editor_note = False
                html_lines.append('</div>')
                if line.startswith('##') and '编者说明' not in line:
                    html_lines.append(f'<h2>{line[3:]}</h2>')
            else:
                html_lines.append(f'<p>{line}</p>')
            continue
            
        if '致莫里斯·巴雷斯' in line and '##' in line:
            in_dedication = True
            html_lines.append('<div class="dedication"><h2>致谢</h2>')
            continue
            
        if in_dedication:
            if '【致莫里斯·巴雷斯 完】' in line:
                in_dedication = False
                html_lines.append('</div>')
            else:
                html_lines.append(f'<p>{line}</p>')
            continue
        
        if line.strip() == '---':
            html_lines.append('<div class="divider">· · ·</div>')
            continue
            
        if re.match(r'##?\s*第[一二三四五六七八九十]+幕', line) or \
           '第一幕' in line or '第二幕' in line or '第三幕' in line or \
           '第四幕' in line or '第五幕' in line or \
           '「第一场」' in line or '「第二场」' in line:
            clean = re.sub(r'^#+\s*', '', line)
            html_lines.append(f'<div class="scene-header">{clean}</div>')
            continue
            
        if re.match(r'##?\s*第.+?场', line):
            clean = re.sub(r'^#+\s*', '', line)
            html_lines.append(f'<div class="scene-header">{clean}</div>')
            continue
        
        if line.startswith('**场景**') or line.startswith('**（原文') or \
           line.startswith('**人物**') or line.startswith('**双生子'):
            clean = line.replace('**', '')
            html_lines.append(f'<div class="stage-direction">{clean}</div>')
            continue
        
        if line.startswith('**学术脚注'):
            continue
            
        if re.match(r'^\*\*[A-Za-z\u4e00-\u9fff·]+[，。、]*\*\*$', line):
            clean = re.sub(r'\*\*', '', line)
            html_lines.append(f'<p class="character">{clean}</p>')
            continue
        
        if line.strip():
            processed = convert_footnote_refs(line)
            html_lines.append(f'<p>{processed}</p>')
    
    return '\n'.join(html_lines)


def generate_footnotes_section(footnotes):
    """Generate HTML for footnotes section."""
    if not footnotes:
        return ''
    
    items = []
    for num, text in sorted(footnotes.items(), key=lambda x: int(x[0])):
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        items.append(f'<div class="footnote-item" id="fn-{num}"><span class="footnote-anchor">[{num}]</span> {text}</div>')
    
    return f'''
    <div class="footnotes-section">
        <h2>注释</h2>
        {''.join(items)}
    </div>'''


def generate_html(body_content, footnotes_html):
    """Generate complete HTML document."""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>《圣塞巴斯蒂安的殉难》完整学术中文译本</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #faf8f5;
            --text-color: #2c2c2c;
            --header-color: #1a1a1a;
            --accent-color: #8b4513;
            --accent-light: #d4a574;
            --border-color: #e0dcd4;
            --note-bg: #f5f0e8;
            --note-border: #c9b896;
            --hover-bg: #f0ebe3;
            --shadow: rgba(0,0,0,0.08);
        }}
        
        [data-theme="dark"] {{
            --bg-color: #1a1917;
            --text-color: #e8e4dc;
            --header-color: #f0ece4;
            --accent-color: #d4a574;
            --accent-light: #8b4513;
            --border-color: #3d3a33;
            --note-bg: #252420;
            --note-border: #5c554a;
            --hover-bg: #2a2824;
            --shadow: rgba(0,0,0,0.3);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Serif SC', 'Source Serif 4', Georgia, serif;
            font-size: 18px;
            line-height: 1.9;
            color: var(--text-color);
            background-color: var(--bg-color);
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .container {{
            max-width: 820px;
            margin: 0 auto;
            padding: 60px 40px 100px;
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--note-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.2s ease;
        }}
        
        .theme-toggle:hover {{
            background: var(--hover-bg);
        }}
        
        header {{
            text-align: center;
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        h1 {{
            font-size: 2.4em;
            font-weight: 600;
            color: var(--header-color);
            margin-bottom: 20px;
            letter-spacing: 0.05em;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            color: var(--accent-color);
            font-style: italic;
            margin-bottom: 10px;
        }}
        
        .author {{
            font-size: 1em;
            color: var(--text-color);
            opacity: 0.8;
        }}
        
        .editor-note {{
            margin-top: 30px;
            padding: 25px 30px;
            background: var(--note-bg);
            border-left: 3px solid var(--accent-color);
            border-radius: 0 6px 6px 0;
            font-size: 0.95em;
            line-height: 1.8;
        }}
        
        .editor-note p {{
            margin-bottom: 15px;
        }}
        
        .editor-note p:last-child {{
            margin-bottom: 0;
        }}
        
        h2 {{
            font-size: 1.6em;
            font-weight: 600;
            color: var(--header-color);
            margin: 50px 0 25px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
            letter-spacing: 0.03em;
        }}
        
        .scene-header {{
            font-size: 1.15em;
            font-weight: 500;
            color: var(--accent-color);
            margin: 40px 0 20px;
            padding: 15px 20px;
            background: var(--note-bg);
            border-radius: 6px;
            border-left: 3px solid var(--accent-light);
        }}
        
        .stage-direction {{
            font-style: italic;
            color: var(--text-color);
            opacity: 0.85;
            margin: 20px 0;
            padding: 15px 20px;
            background: var(--note-bg);
            border-radius: 6px;
            font-size: 0.95em;
        }}
        
        .character {{
            font-weight: 600;
            color: var(--accent-color);
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        
        p {{
            margin-bottom: 1em;
        }}
        
        .footnote-ref {{
            font-size: 0.75em;
            vertical-align: super;
            color: var(--accent-color);
            cursor: pointer;
            text-decoration: none;
            padding: 0 2px;
            transition: color 0.2s;
        }}
        
        .footnote-ref:hover {{
            color: var(--accent-light);
        }}
        
        .footnotes-section {{
            margin-top: 80px;
            padding-top: 40px;
            border-top: 2px solid var(--border-color);
        }}
        
        .footnotes-section h2 {{
            font-size: 1.3em;
            margin-bottom: 25px;
        }}
        
        .footnote-item {{
            margin-bottom: 15px;
            padding: 12px 18px;
            background: var(--note-bg);
            border-radius: 6px;
            font-size: 0.9em;
        }}
        
        .divider {{
            text-align: center;
            margin: 50px 0;
            color: var(--border-color);
            font-size: 1.5em;
            letter-spacing: 0.5em;
        }}
        
        .dedication {{
            margin: 40px 0;
            padding: 30px;
            text-align: center;
        }}
        
        .dedication p {{
            margin-bottom: 1em;
        }}
        
        .dedication h2 {{
            border: none;
            margin-bottom: 30px;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                color-scheme: dark;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 30px 20px 60px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            body {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">◐ 切换主题</button>
    <div class="container">
        <header>
            <h1>《圣塞巴斯蒂安的殉难》</h1>
            <p class="subtitle">Le Martyre de Saint Sébastien</p>
            <p class="author">Gabriele d'Annunzio 著</p>
            <p class="subtitle" style="margin-top:15px;font-size:0.9em;">完整学术中文译本</p>
        </header>
        
        {body_content}
        
        {footnotes_html}
        
    </div>
    
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
            localStorage.setItem('theme', current === 'dark' ? 'light' : 'dark');
        }}
        
        function showFootnote(el, num) {{
            document.querySelectorAll('.footnote-content').forEach(f => {{
                f.classList.remove('visible');
            }});
            
            const footnote = document.getElementById('fn-' + num);
            if (footnote) {{
                const rect = el.getBoundingClientRect();
                footnote.style.top = (rect.bottom + window.scrollY + 5) + 'px';
                footnote.style.left = Math.min(rect.left, window.innerWidth - 420) + 'px';
                footnote.classList.add('visible');
                
                setTimeout(() => {{
                    document.addEventListener('click', closeFootnote);
                }}, 0);
            }}
        }}
        
        function closeFootnote(e) {{
            if (!e.target.classList.contains('footnote-ref')) {{
                document.querySelectorAll('.footnote-content').forEach(f => {{
                    f.classList.remove('visible');
                }});
                document.removeEventListener('click', closeFootnote);
            }}
        }}
        
        const saved = localStorage.getItem('theme');
        if (saved) {{
            document.documentElement.setAttribute('data-theme', saved);
        }} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            document.documentElement.setAttribute('data-theme', 'dark');
        }}
    </script>
</body>
</html>'''


if __name__ == '__main__':
    with open('/Users/eight/hermes_data/doc/临时/Le_martyre_de_Saint_Sebastien_完整学术中文译本.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    footnotes = extract_footnotes(content)
    print(f"Extracted {len(footnotes)} footnotes")
    
    body = simple_convert(content, footnotes)
    footnotes_html = generate_footnotes_section(footnotes)
    html = generate_html(body, footnotes_html)
    
    with open('/Users/eight/test_github_repo/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML generated successfully!")