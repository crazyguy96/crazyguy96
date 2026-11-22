#!/usr/bin/env python3
"""
Build a completely self-contained HTML preview where all SVGs are directly inlined.
- Zero file:// image references (fixes the "nothing is visible" blank image issue).
- Fonts (Instrument Serif, Geist, Geist Mono) embedded directly in HTML <head>.
- 100% exact vector layout, typography, animations, and icons.
- 4 color palettes combining Greige/Beige, Grey, Black, Dark Pink, and Yellow.
- ALL 4 Featured Projects (Meeting, Delay, Vision, Mazdoor).
- ALL 3 About Me cards (Code, Sports, Work).
- ALL 3 Skills cards (Languages, ML, Tools).
- Untouched macOS Terminal card.
- Activity card.
"""
import os
import re
import base64
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
FONTS_DIR = os.path.join(ROOT, "fonts")
OUT_HTML = os.path.expanduser("~/.gemini/antigravity/brain/e783699c-ef1e-42bc-9a95-a5a1f8b56063/real_svg_palette_previews.html")
PREVIEWS_DIR = os.path.expanduser("~/.gemini/antigravity/brain/e783699c-ef1e-42bc-9a95-a5a1f8b56063/palette_previews")

FONT_FILES = {
    "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
    "serif-i": ("Instrument Serif", "italic", 400, "serif-italic.woff"),
    "sans": ("Geist", "normal", 400, "geist-400.woff"),
    "sans-b": ("Geist", "normal", 600, "geist-600.woff"),
    "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
}

def get_font_css():
    out = []
    for k, (fam, style, weight, fn) in FONT_FILES.items():
        p = os.path.join(FONTS_DIR, fn)
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};src:url(data:font/woff;base64,{b64}) format('woff');}}")
    return "\n".join(out)

def prepare_svg(svg_path, prefix):
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Strip inner @font-face to save space (since defined globally in HTML head)
    content = re.sub(r'@font-face\{[^}]+\}', '', content)
    
    # Prefix IDs to avoid DOM clashes between options
    content = re.sub(r'id="([a-zA-Z0-9_-]+)"', lambda m: f'id="{prefix}_{m.group(1)}"', content)
    content = re.sub(r'url\(#([a-zA-Z0-9_-]+)\)', lambda m: f'url(#{prefix}_{m.group(1)})', content)
    content = re.sub(r'href="#([a-zA-Z0-9_-]+)"', lambda m: f'href="#{prefix}_{m.group(1)}"', content)
    
    return content

OPTIONS = [
    {
        "id": "opt1",
        "dir": "option_1_studio_greige",
        "name": "Option 1: Studio Greige (Light Paper)",
        "badge": "Editorial Stone",
        "badge_style": "background:#be123c22; color:#fb7185; border:1px solid #be123c55;",
        "desc": "A rich oatmeal greige (#ece7de) base, carbon black text (#141414), crimson dark pink (#be123c) & saffron yellow (#ca8a04). Removes harsh white paper while preserving sharp readability.",
        "swatches": [
            ("#ece7de", "#ECE7DE Greige"),
            ("#141414", "#141414 Black"),
            ("#be123c", "#BE123C Dark Pink"),
            ("#ca8a04", "#CA8A04 Yellow"),
        ]
    },
    {
        "id": "opt2",
        "dir": "option_2_dark_greige",
        "name": "Option 2: Dark Charcoal Greige (Warm Dark Mode)",
        "badge": "Warm Synthwave Dark",
        "badge_style": "background:#facc1522; color:#fde047; border:1px solid #facc1555;",
        "desc": "Deep charcoal greige (#1e1d1b) surface, warm sand beige text (#f0ebe1), glowing dark rose (#fb7185) & electric canary (#facc15). Seamless dark mode harmony with the macOS terminal.",
        "swatches": [
            ("#1e1d1b", "#1E1D1B Dark Greige"),
            ("#f0ebe1", "#F0EBE1 Beige Text"),
            ("#fb7185", "#FB7185 Dark Pink"),
            ("#facc15", "#FACC15 Yellow"),
        ]
    },
    {
        "id": "opt3",
        "dir": "option_3_bauhaus_linen",
        "name": "Option 3: Bauhaus Sand Linen (Warm Sandstone)",
        "badge": "Bauhaus Sandstone",
        "badge_style": "background:#6366f122; color:#a5b4fc; border:1px solid #6366f155;",
        "desc": "Tactile sandstone linen (#f4efe6) base, pitch carbon (#111111) text, bold dark rose (#e11d48) & bauhaus canary (#eab308). Clean, warm architectural look.",
        "swatches": [
            ("#f4efe6", "#F4EFE6 Sand Linen"),
            ("#111111", "#111111 Pitch Black"),
            ("#e11d48", "#E11D48 Dark Rose"),
            ("#eab308", "#EAB308 Canary"),
        ]
    },
    {
        "id": "opt4",
        "dir": "option_4_titanium_concrete",
        "name": "Option 4: Titanium Concrete Greige (Industrial Muted)",
        "badge": "Modern Titanium",
        "badge_style": "background:#ec489922; color:#f472b6; border:1px solid #ec489955;",
        "desc": "Neutral concrete greige (#e5e2da), graphite ink (#18181b), magenta noir (#c026d3) & tuscan gold (#ca8a04). Balanced, muted modern engineering tone.",
        "swatches": [
            ("#e5e2da", "#E5E2DA Concrete"),
            ("#18181b", "#18181B Graphite"),
            ("#c026d3", "#C026D3 Magenta Pink"),
            ("#ca8a04", "#CA8A04 Gold"),
        ]
    }
]

def build_html():
    font_css = get_font_css()
    terminal_src = os.path.join(ROOT, "cards", "terminal.svg")
    
    panels_html = []
    tabs_html = []
    
    for idx, opt in enumerate(OPTIONS):
        active_class = "active" if idx == 0 else ""
        tabs_html.append(f"""
      <button class="tab-btn {active_class}" onclick="showOption('{opt['id']}', this)">
        <span>{opt['name']}</span>
      </button>""")
        
        opt_dir = os.path.join(PREVIEWS_DIR, opt["dir"])
        p_id = opt["id"]
        
        # Prepare SVGs inline
        hero_svg = prepare_svg(os.path.join(opt_dir, "hero.svg"), f"{p_id}_hero")
        term_svg = prepare_svg(terminal_src, f"{p_id}_term")
        
        # 4 Social Icons
        icon_linkedin = prepare_svg(os.path.join(opt_dir, "icon-linkedin.svg"), f"{p_id}_in")
        icon_leetcode = prepare_svg(os.path.join(opt_dir, "icon-leetcode.svg"), f"{p_id}_lc")
        icon_codeforces = prepare_svg(os.path.join(opt_dir, "icon-codeforces.svg"), f"{p_id}_cf")
        icon_github = prepare_svg(os.path.join(opt_dir, "icon-github.svg"), f"{p_id}_gh")

        # 3 About Cards
        about_code_svg = prepare_svg(os.path.join(opt_dir, "about-code.svg"), f"{p_id}_abcode")
        about_sports_svg = prepare_svg(os.path.join(opt_dir, "about-sports.svg"), f"{p_id}_absport")
        about_work_svg = prepare_svg(os.path.join(opt_dir, "about-work.svg"), f"{p_id}_abwork")
        
        # 4 Project Cards
        meeting_svg = prepare_svg(os.path.join(opt_dir, "meeting.svg"), f"{p_id}_meet")
        delay_svg = prepare_svg(os.path.join(opt_dir, "delay.svg"), f"{p_id}_delay")
        vision_svg = prepare_svg(os.path.join(opt_dir, "vision.svg"), f"{p_id}_vis")
        mazdoor_svg = prepare_svg(os.path.join(opt_dir, "mazdoor.svg"), f"{p_id}_maz")
        
        # 3 Skills Cards
        lang_svg = prepare_svg(os.path.join(opt_dir, "skills-languages.svg"), f"{p_id}_lang")
        ml_svg = prepare_svg(os.path.join(opt_dir, "skills-ml.svg"), f"{p_id}_ml")
        tools_svg = prepare_svg(os.path.join(opt_dir, "skills-tools.svg"), f"{p_id}_tools")
        
        # Activity Card
        activity_svg = prepare_svg(os.path.join(opt_dir, "activity.svg"), f"{p_id}_act")
        
        swatches_html = "".join([
            f'<div class="swatch"><div class="dot" style="background:{hex};"></div>{label}</div>'
            for hex, label in opt["swatches"]
        ])
        
        panel = f"""
    <!-- {opt['name']} -->
    <div id="panel-{p_id}" class="view-panel {active_class}">
      <div class="palette-banner">
        <div class="palette-info">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <h3 style="margin:0;">{opt['name']}</h3>
            <span class="badge" style="{opt['badge_style']}">{opt['badge']}</span>
          </div>
          <p>{opt['desc']}</p>
        </div>
        <div class="swatches">
          {swatches_html}
        </div>
      </div>

      <div class="gh-canvas">
        <!-- 1. Hero Card -->
        <div class="card-wrap center">{hero_svg}</div>
        
        <!-- 2. Untouched macOS Terminal -->
        <div class="card-wrap center" style="margin-top:14px;">{term_svg}</div>

        <!-- 2.5 Social & Platform Icons (LinkedIn, LeetCode, Codeforces, GitHub) -->
        <div class="social-row">
          <div class="icon-wrap">{icon_linkedin}</div>
          <div class="icon-wrap">{icon_leetcode}</div>
          <div class="icon-wrap">{icon_codeforces}</div>
          <div class="icon-wrap">{icon_github}</div>
        </div>

        <!-- 3. About Me (3 Cards) -->
        <div class="section-title">About Me</div>
        <div class="row-3">
          <div class="card-wrap col-3">{about_code_svg}</div>
          <div class="card-wrap col-3">{about_sports_svg}</div>
          <div class="card-wrap col-3">{about_work_svg}</div>
        </div>

        <!-- 4. Featured Projects (ALL 4 CARDS: Meeting, Delay, Vision, Mazdoor) -->
        <div class="section-title">Featured Projects (All 4 Projects)</div>
        <div class="row-2">
          <div class="card-wrap col-2">{meeting_svg}</div>
          <div class="card-wrap col-2">{delay_svg}</div>
        </div>
        <div class="row-2" style="margin-top:12px;">
          <div class="card-wrap col-2">{vision_svg}</div>
          <div class="card-wrap col-2">{mazdoor_svg}</div>
        </div>

        <!-- 5. Tools & Technologies (3 Cards: Languages, ML, Tools) -->
        <div class="section-title">Tools &amp; Technologies (24 Pure Vector Icons)</div>
        <div class="row-3">
          <div class="card-wrap col-3">{lang_svg}</div>
          <div class="card-wrap col-3">{ml_svg}</div>
          <div class="card-wrap col-3">{tools_svg}</div>
        </div>

        <!-- 6. Contribution Activity -->
        <div class="section-title">Contribution Activity</div>
        <div class="card-wrap center">{activity_svg}</div>
      </div>
    </div>"""
        panels_html.append(panel)
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Real Inline SVG Palette Previews — Greige, Black, Dark Pink, Yellow</title>
  <style>
    /* Embedded Exact Profile Fonts */
    {font_css}

    :root {{
      --bg: #0d1117;
      --text: #c9d1d9;
      --border: #30363d;
      --card-bg: #161b22;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 30px 20px;
      background: var(--bg);
      color: var(--text);
      transition: background 0.2s ease;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 28px;
    }}
    h1 {{
      font-size: 24px;
      margin: 0 0 6px 0;
      color: #f0f6fc;
      letter-spacing: -0.4px;
    }}
    p.sub {{
      margin: 0;
      font-size: 14px;
      color: #8b949e;
      line-height: 1.5;
    }}
    .controls {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .toggle-group {{
      display: flex;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 3px;
    }}
    .toggle-btn {{
      background: transparent;
      border: none;
      color: #8b949e;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .toggle-btn.active {{
      background: #388bfd;
      color: #ffffff;
    }}

    /* Tabs */
    .tabs {{
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
      overflow-x: auto;
      padding-bottom: 4px;
    }}
    .tab-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .tab-btn:hover {{
      border-color: #8b949e;
    }}
    .tab-btn.active {{
      background: #1f6feb22;
      border-color: #58a6ff;
      color: #58a6ff;
    }}

    /* Banner */
    .palette-banner {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .palette-info h3 {{
      margin: 0;
      font-size: 16px;
      color: #f0f6fc;
    }}
    .palette-info p {{
      margin: 0;
      font-size: 13px;
      color: #8b949e;
      line-height: 1.4;
    }}
    .badge {{
      font-size: 11px;
      font-family: monospace;
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 600;
    }}
    .swatches {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .swatch {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-family: monospace;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
    }}
    .dot {{
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }}

    /* GitHub Canvas */
    .gh-canvas {{
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 32px 24px;
      background: var(--bg);
      margin-bottom: 40px;
    }}
    .section-title {{
      font-size: 17px;
      font-weight: 600;
      color: #f0f6fc;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      margin: 30px 0 16px 0;
    }}

    /* Responsive Inline SVG Wrappers */
    .card-wrap svg {{
      width: 100%;
      height: auto;
      display: block;
      border-radius: 14px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }}
    .center {{
      text-align: center;
      margin-bottom: 14px;
    }}
    .row-3 {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .col-3 {{
      width: 32.5%;
    }}
    .row-2 {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .col-2 {{
      width: 49%;
    }}

    /* Social Icons Row */
    .social-row {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 16px;
      margin: 18px 0 24px 0;
    }}
    .icon-wrap svg {{
      width: 42px;
      height: 42px;
      display: block;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      transition: transform 0.2s ease;
    }}
    .icon-wrap svg:hover {{
      transform: translateY(-2px);
    }}

    .view-panel {{
      display: none;
    }}
    .view-panel.active {{
      display: block;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>Real Inline SVG Palette Previews</h1>
        <p class="sub">Embedded directly as native inline SVGs (100% visible, zero file:// blocks).<br>Exact fonts, exact layouts, untouched macOS Terminal card, and all 4 projects included.</p>
      </div>
      <div class="controls">
        <div class="toggle-group">
          <button class="toggle-btn active" onclick="setCanvasMode('dark')">GitHub Dark</button>
          <button class="toggle-btn" onclick="setCanvasMode('light')">GitHub Light</button>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="tabs">
      {''.join(tabs_html)}
    </div>

    <!-- Option Panels with Inline SVGs -->
    {''.join(panels_html)}

  </div>

  <script>
    function showOption(optId, btn) {{
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('panel-' + optId).classList.add('active');
      btn.classList.add('active');
    }}

    function setCanvasMode(mode) {{
      const isDark = mode === 'dark';
      document.body.style.background = isDark ? '#0d1117' : '#f6f8fa';
      document.body.style.color = isDark ? '#c9d1d9' : '#24292f';
      document.querySelectorAll('.gh-canvas').forEach(c => {{
        c.style.background = isDark ? '#0d1117' : '#ffffff';
        c.style.borderColor = isDark ? '#30363d' : '#d0d7de';
      }});
      document.querySelectorAll('.toggle-btn').forEach(b => b.classList.toggle('active'));
    }}
  </script>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated self-contained inline SVG preview at: {OUT_HTML} ({len(html_content)//1024} KB)")

if __name__ == "__main__":
    build_html()
