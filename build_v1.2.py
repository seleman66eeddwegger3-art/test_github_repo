#!/usr/bin/env python3
"""
Build v1.2 from index.html — Way of Code aesthetic.
Precise anchor placement for left nav.
"""
import re, os

SRC = "/Users/eight/test_github_repo/index.html"
OUT = "/Users/eight/test_github_repo/v1.2.html"

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ── Extract body content ──
body_start = html.find("<body>") + len("<body>")
body_end = html.find("</body>")
body = html[body_start:body_end]

# ── Remove theme toggle and scripts ──
body = re.sub(r'<button[^>]*class="theme-toggle"[^>]*>.*?</button>', '', body, flags=re.DOTALL)
body = re.sub(r'<script[^>]*>.*?theme.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)

# ── Insert anchor IDs at key positions ──
# We insert <div id="actN"></div> just before the content
# Act 1 prologue: "第一幕　异教的庭院" 
body = body.replace(
    '<div class="scene-header">第一幕　异教的庭院</div>',
    '<div id="act1-intro" class="scene-header">第一幕　异教的庭院</div>',
    1
)

# Act 1 full mansion: "第一幕「第一场」—— 百合的庭院"
body = body.replace(
    '<div class="scene-header">第一幕「第一场」—— 百合的庭院</div>',
    '<div id="act1" class="scene-header">第一幕「第一场」—— 百合的庭院</div>',
    1
)

# Act 2: "第二居所" ... "魔法厅"
body = body.replace(
    '<p>## 第二居所</p>',
    '<p id="act2">## 第二居所</p>',
    1
)

# Act 3: "第三寓所" with "伪神议会" 
# Find the first occurrence after Act 1 ends
m = re.search(r'<p>第三寓所</p>\s*<p>8</p>\s*<p>伪神议会</p>', body)
if m:
    insert = '<p id="act3">第三寓所</p>\n<p>8</p>\n<p>伪神议会</p>'
    body = body[:m.start()] + insert + body[m.end():]

# Act 4: "第四章 受伤的月桂" (first occurrence with play text, around line 2412)
body = body.replace(
    '<p>第四章 受伤的月桂</p>',
    '<p id="act4">第四章 受伤的月桂</p>',
    1
)

# Act 5: "第五居所。乐园"
body = body.replace(
    '<p><strong>第五居所。乐园</strong></p>',
    '<p id="act5"><strong>第五居所。乐园</strong></p>',
    1
)

# ── Verify anchors ──
for anchor in ['act1-intro', 'act1', 'act2', 'act3', 'act4', 'act5']:
    count = body.count(f'id="{anchor}"')
    print(f"  id={anchor}: {count} occurrences")

# ── Build the left nav ──
nav_html = '''    <nav class="left-nav">
        <a href="#top" title="顶部">§</a>
        <span class="nav-sep"></span>
        <a href="#act1-intro" title="序幕">I</a>
        <a href="#act1" title="第一幕 · 百合的庭院">I°</a>
        <a href="#act2" title="第二幕 · 魔幻之室">II</a>
        <a href="#act3" title="第三幕 · 伪神会议">III</a>
        <a href="#act4" title="第四幕 · 受伤的月桂">IV</a>
        <a href="#act5" title="第五幕 · 乐园">V</a>
    </nav>'''

# ── Add top anchor + nav ──
body = '<div id="top"></div>\n' + nav_html + '\n' + body

# ── New CSS (Way of Code) ──
new_css = '''    <style>
        :root {
            --bg:        #2d2e28;
            --bg-soft:   #3a3b34;
            --text:      #e8e2d0;
            --text-dim:  #9a9485;
            --accent:    #8B3A3A;
            --gold:      #c9a96e;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'EB Garamond', 'Noto Serif SC', Georgia, serif;
            font-size: 20px;
            line-height: 2.2;
            color: var(--text);
            background-color: var(--bg);
            min-height: 100vh;
        }

        /* ── Left Navigation ── */
        .left-nav {
            position: fixed;
            left: 36px;
            top: 50%;
            transform: translateY(-50%);
            z-index: 100;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .left-nav a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 13px;
            font-style: italic;
            letter-spacing: 2px;
            color: var(--text-dim);
            text-decoration: none;
            border: 1px solid var(--bg-soft);
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .left-nav a:hover {
            color: var(--gold);
            border-color: var(--gold);
            background: rgba(201, 169, 110, 0.08);
        }
        .left-nav .nav-sep {
            width: 38px;
            height: 1px;
            background: var(--bg-soft);
            margin: 2px auto;
        }

        /* ── Container ── */
        .container {
            max-width: 720px;
            margin: 0 auto;
            padding: 120px 60px 200px;
        }

        /* ── Header ── */
        header {
            text-align: center;
            margin-bottom: 120px;
            padding-bottom: 60px;
            border-bottom: 1px solid var(--bg-soft);
        }
        h1 {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: 2.6em;
            font-weight: 400;
            color: var(--gold);
            letter-spacing: 0.08em;
            margin-bottom: 20px;
        }
        .subtitle {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: 1.2em;
            color: var(--text-dim);
            letter-spacing: 0.12em;
            margin-bottom: 8px;
        }
        .author {
            font-size: 0.95em;
            color: var(--text-dim);
            opacity: 0.6;
        }

        /* ── Scene Headers ── */
        .scene-header {
            text-align: center;
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: 1.4rem;
            color: var(--gold);
            letter-spacing: 0.15em;
            margin: 100px 0 50px;
            padding: 40px 0;
            border-top: 1px solid var(--bg-soft);
            border-bottom: 1px solid var(--bg-soft);
            scroll-margin-top: 80px;
        }
        .scene-header strong {
            color: var(--accent);
            font-weight: 400;
        }

        /* ── Paragraphs = Breath Units ── */
        p {
            margin-bottom: 2.4em;
            text-align: justify;
            hyphens: auto;
        }

        /* ── Stage Directions ── */
        .stage-direction {
            font-style: italic;
            color: var(--text-dim);
            font-size: 0.92rem;
            line-height: 2;
            margin: 2.4em 0 2.4em 1.8em;
            padding: 1.2em 1.8em;
            border-left: 2px solid var(--bg-soft);
            background: rgba(58, 59, 52, 0.2);
            border-radius: 0 4px 4px 0;
        }

        /* ── Character Names ── */
        strong {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-weight: 500;
            color: var(--gold);
            letter-spacing: 0.05em;
            font-size: 1.05em;
        }

        /* ── Editor Note ── */
        .editor-note {
            margin: 60px 0;
            padding: 36px 40px;
            background: rgba(139, 58, 58, 0.06);
            border-left: 3px solid var(--accent);
            border-radius: 0 4px 4px 0;
            font-size: 0.95em;
            line-height: 2;
        }
        .editor-note p { margin-bottom: 1.5em; }
        .editor-note p:last-child { margin-bottom: 0; }

        /* ── Dedication ── */
        .dedication {
            margin: 80px 0;
            padding: 60px 0;
            border-top: 1px solid var(--bg-soft);
            border-bottom: 1px solid var(--bg-soft);
            text-align: center;
        }
        .dedication h2 {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: 1.6rem;
            font-weight: 400;
            color: var(--gold);
            letter-spacing: 0.2em;
            margin-bottom: 40px;
        }
        .dedication p {
            font-style: italic;
            color: var(--text-dim);
            max-width: 520px;
            margin: 0 auto 1.8em;
            text-align: center;
        }

        /* ── Dividers ── */
        .divider {
            width: 60px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--bg-soft), transparent);
            margin: 60px auto;
            color: transparent;
            font-size: 0;
            line-height: 0;
            text-indent: -9999px;
            overflow: hidden;
        }

        /* ── h2 ── */
        h2 {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: 1.8rem;
            font-weight: 400;
            color: var(--gold);
            letter-spacing: 0.1em;
            margin: 80px 0 40px;
            text-align: center;
        }

        /* ── Footnotes ── */
        .footnote-ref {
            color: var(--accent);
            cursor: pointer;
            font-size: 0.75em;
            vertical-align: super;
            text-decoration: none;
        }
        .footnote-ref:hover { color: var(--gold); }

        /* ── Anchor offset ── */
        [id] { scroll-margin-top: 60px; }

        /* ── Responsive ── */
        @media (max-width: 900px) {
            .left-nav { left: 16px; gap: 8px; }
            .left-nav a { width: 32px; height: 32px; font-size: 12px; }
            .container { padding: 80px 40px 140px; max-width: 100%; }
        }
        @media (max-width: 768px) {
            .left-nav { display: none; }
            .container { padding: 60px 24px 100px; }
            body { font-size: 18px; }
            h1 { font-size: 2em; }
            .scene-header { font-size: 1.2rem; margin: 60px 0 30px; }
        }
    </style>'''

# ── Assemble final HTML ──
# Replace style block
new_html = re.sub(
    r'<style>.*?</style>',
    new_css,
    html,
    flags=re.DOTALL
)

# Replace body content
new_html = re.sub(
    r'<body>.*?</body>',
    f'<body>\n{body}\n</body>',
    new_html,
    flags=re.DOTALL
)

# Update title
new_html = new_html.replace(
    "<title>《圣塞巴斯蒂安的殉难》完整学术中文译本</title>",
    "<title>圣塞巴斯蒂安的殉难 — Le Martyre de Saint Sébastien (v1.2)</title>"
)

# Fix font loading
new_html = re.sub(
    r'<link[^>]*fonts\.googleapis\.com[^>]*>',
    '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">',
    new_html
)

# Remove theme toggle's CSS custom properties if they exist inline
new_html = new_html.replace('[data-theme="dark"]', '[data-theme="v1.2"]')

# Write
with open(OUT, "w", encoding="utf-8") as f:
    f.write(new_html)

size = os.path.getsize(OUT)
print(f"\n✅ v1.2.html written: {size:,} bytes → {OUT}")
