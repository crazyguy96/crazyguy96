#!/usr/bin/env python3
"""
Generate all profile SVG cards for Jatin Mehra (crazyguy96).
Design: High-craft Paper & Ink UI/UX, embedding Instrument Serif, Geist, and Geist Mono
with physics-based entrance, sheen, and micro-interactions.
"""
import base64
import datetime
import json
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA_FILE = os.path.join(ROOT, "data", "contributions.json")
OUT_DIR = os.path.join(ROOT, "cards")
FONTS_DIR = os.path.join(ROOT, "fonts")

# Palette tokens: Crisp White & Ink with Dark Rose / Pink accent
WHITE = "#ffffff"
PAPER = "#f7f7f5"
BORDER = "#e4e4df"
BORDER_SOFT = "#eeeeea"
INK = "#111111"
INK_SOFT = "#4a4a4e"
MUTED = "#76767c"

# Project accents
BLUE = "#e11d48"    # Bold Dark Rose / Crimson Pink (replaces earlier #2563eb blue!)
AMBER = "#d97706"   # Amber / Gold
VIOLET = "#7c3aed"  # Violet (DINOv2)
GREEN = "#059669"   # Emerald Green

SERIF = "'Instrument Serif', Georgia, serif"
SANS = "Geist, system-ui, -apple-system, sans-serif"
MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

FONT_FILES = {
    "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
    "serif-i": ("Instrument Serif", "italic", 400, "serif-italic.woff"),
    "sans": ("Geist", "normal", 400, "geist-400.woff"),
    "sans-b": ("Geist", "normal", 600, "geist-600.woff"),
    "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
}

BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.12)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
@keyframes sheen{0%{transform:translateX(-300px) skewX(-20deg)}22%,100%{transform:translateX(500px) skewX(-20deg)}}
.r{opacity:0;animation:rise .75s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .85s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 2s ease-in-out infinite}
.sh{animation:sheen 6s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){.r,.f,.g,.p,.live,.nu{animation:none!important;opacity:1!important;transform:none!important}.sh{display:none}}
"""


def font_face():
    out = []
    for k in ["serif", "serif-i", "sans", "sans-b", "mono"]:
        fam, style, weight, fn = FONT_FILES[k]
        path = os.path.join(FONTS_DIR, fn)
        if os.path.exists(path):
            b64 = base64.b64encode(open(path, "rb").read()).decode()
            out.append(
                f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
            )
    return "".join(out)


def write_card(name, svg_content):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"wrote cards/{name} ({len(svg_content) // 1024} KB)")


SHEEN_DEF = """
<defs>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".45"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
"""


# ---- 1 · hero.svg -------------------------------------------------------------
def build_hero():
    w, h = 880, 230
    css = font_face() + BASE_CSS
    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Jatin Mehra - Data Science &amp; AI at IIT Guwahati">
<title>Jatin Mehra — Data Science &amp; AI · IIT Guwahati</title>
<style>{css}</style>
<defs>
  <clipPath id="hero-clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".4"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>
    <stop offset=".5" stop-color="{BLUE}"/><stop offset=".58" stop-color="{INK}"/>
    <stop offset="1" stop-color="{INK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>

<!-- Card Surface -->
<g clip-path="url(#hero-clip)">
  <rect width="{w}" height="{h}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
  <rect class="sh" x="0" y="0" width="140" height="{h}" fill="url(#card-sheen)" transform="translate(-300 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<!-- Left Content -->
<g transform="translate(44, 40)">
  <g class="f" style="animation-delay:0.1s">
    <circle cx="4" cy="4" r="3.5" fill="{BLUE}" class="live"/>
    <text x="16" y="8" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">DATA SCIENCE &amp; AI · IIT GUWAHATI (2025–2029)</text>
  </g>
  <text class="r" style="animation-delay:0.2s" x="0" y="68" font-family="{SERIF}" font-size="62" letter-spacing="-1.5" fill="{INK}">
    Jatin <tspan font-style="italic" fill="url(#shine)">Mehra</tspan>
  </text>
  <text class="r" style="animation-delay:0.35s" x="2" y="104" font-family="{SANS}" font-size="16" fill="{INK_SOFT}">
    Machine learning systems for messy, real-world inputs.
  </text>
  <text class="r" style="animation-delay:0.5s" x="2" y="132" font-family="{MONO}" font-size="12" fill="{MUTED}">
    Speech AI · Computer Vision · Explainable ML · DSA
  </text>
</g>

<!-- Right Side Visual Moment: Acoustic Spectrum Envelope -->
<g transform="translate(580, 36)">
  <rect class="f" style="animation-delay:0.3s" width="256" height="158" rx="10" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
  <text class="f" style="animation-delay:0.4s" x="16" y="24" font-family="{MONO}" font-size="10.5" fill="{MUTED}">ACOUSTIC SPECTRUM f(t)</text>
  
  <!-- Waveform lines -->
  <line x1="16" y1="80" x2="240" y2="80" stroke="#dfdfd9" stroke-width="1"/>
  <line x1="16" y1="52" x2="240" y2="52" stroke="#e8e8e2" stroke-width="0.75" stroke-dasharray="2 3"/>
  <line x1="16" y1="108" x2="240" y2="108" stroke="#e8e8e2" stroke-width="0.75" stroke-dasharray="2 3"/>
  
  <!-- Envelope trace -->
  <path class="f" style="animation-delay:0.5s" d="M 20 80 C 35 68, 45 92, 60 80 C 75 56, 85 104, 100 80 C 115 44, 125 116, 140 80 C 155 58, 165 102, 180 80 C 195 70, 205 90, 220 80 L 236 80" 
        fill="none" stroke="#b4b4aa" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Vibrant Accent Signal -->
  <path class="r" style="animation-delay:0.65s" d="M 40 80 C 55 60, 65 100, 80 80 C 95 48, 105 112, 120 80 C 135 52, 145 108, 160 80 C 175 64, 185 96, 200 80" 
        fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-linecap="round"/>

  <!-- Readouts -->
  <text class="f" style="animation-delay:0.8s" x="16" y="140" font-family="{MONO}" font-size="10" fill="{MUTED}">16 kHz log-mel</text>
  <text class="f" style="animation-delay:0.85s" x="240" y="140" text-anchor="end" font-family="{MONO}" font-size="9.5" font-weight="600" fill="{BLUE}">Evidence-Grounded &#8599;</text>
</g>
</svg>"""
    write_card("hero.svg", content)


# ---- 2 · terminal.svg ---------------------------------------------------------
def build_terminal(theme="dark"):
    w, h = 880, 248
    
    if theme == "dark":
        bg = "#0d1117"
        header_bg = "#161b22"
        border = "#30363d"
        dot1, dot2, dot3 = "#ff5f56", "#ffbd2e", "#27c93f"
        title_color = "#8b949e"
        branch_color = "#6e7681"
        prompt_color = "#38bdf8"
        cmd_color = "#f0f6fc"
        cursor_color = "#38bdf8"
        out_primary = "#f0f6fc"
        out_dim = "#c9d1d9"
        out_muted = "#8b949e"
        c_meet = "#38bdf8"
        c_delay = "#fbbf24"
        c_vit = "#a78bfa"
        c_mazdoor = "#34d399"
        success = "#34d399"
    else:
        bg = "#ffffff"
        header_bg = "#f7f7f5"
        border = "#e4e4df"
        dot1, dot2, dot3 = "#ff5f56", "#ffbd2e", "#27c93f"
        title_color = "#76767c"
        branch_color = "#a1a1aa"
        prompt_color = "#2563eb"
        cmd_color = "#111111"
        cursor_color = "#2563eb"
        out_primary = "#111111"
        out_dim = "#27272a"
        out_muted = "#71717a"
        c_meet = "#2563eb"
        c_delay = "#d97706"
        c_vit = "#7c3aed"
        c_mazdoor = "#059669"
        success = "#059669"

    css = font_face() + """
.term-mono { font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 13px; }
.term-header { font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11.5px; }
@media (prefers-reduced-motion: reduce) {
  clipPath rect { width: 100% !important; }
  rect, g, text { animation: none !important; opacity: 1 !important; }
}
"""

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Interactive Developer Terminal - Jatin Mehra">
<title>jatin@iitg: ~/projects (zsh)</title>
<style>{css}</style>
<defs>
  <!-- Clip path Command 1: whoami -->
  <clipPath id="c1-clip">
    <rect x="20" y="-14" width="0" height="24">
      <animate attributeName="width" 
               values="0; 0; 52; 52; 52; 0; 0" 
               keyTimes="0; 0.03; 0.10; 0.88; 0.94; 0.98; 1" 
               dur="14s" repeatCount="indefinite" />
    </rect>
  </clipPath>

  <!-- Clip path Command 2: ls projects/ -->
  <clipPath id="c2-clip">
    <rect x="20" y="-14" width="0" height="24">
      <animate attributeName="width" 
               values="0; 0; 100; 100; 100; 0; 0" 
               keyTimes="0; 0.19; 0.28; 0.88; 0.94; 0.98; 1" 
               dur="14s" repeatCount="indefinite" />
    </rect>
  </clipPath>

  <!-- Clip path Command 3: meeting-assistant audio verify -->
  <clipPath id="c3-clip">
    <rect x="20" y="-14" width="0" height="24">
      <animate attributeName="width" 
               values="0; 0; 380; 380; 380; 0; 0" 
               keyTimes="0; 0.38; 0.54; 0.88; 0.94; 0.98; 1" 
               dur="14s" repeatCount="indefinite" />
    </rect>
  </clipPath>
</defs>

<!-- Window Frame Surface -->
<rect width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{border}" stroke-width="1"/>
<path d="M 0 14 Q 0 0 14 0 L {w-14} 0 Q {w} 0 {w} 14 L {w} 36 L 0 36 Z" fill="{header_bg}"/>
<line x1="0" y1="36" x2="{w}" y2="36" stroke="{border}" stroke-width="1"/>

<!-- Traffic lights -->
<circle cx="22" cy="18" r="4.5" fill="{dot1}"/>
<circle cx="38" cy="18" r="4.5" fill="{dot2}"/>
<circle cx="54" cy="18" r="4.5" fill="{dot3}"/>

<!-- Header Info -->
<text x="74" y="22" class="term-header" fill="{title_color}">jatin@iitg: ~/projects</text>
<text x="230" y="22" class="term-header" fill="{branch_color}">git:(<tspan fill="{prompt_color}">main</tspan>)</text>

<!-- Live Pulse on Right -->
<g transform="translate({w - 92}, 13)">
  <circle cx="4" cy="5" r="3" fill="{success}">
    <animate attributeName="opacity" values="1; 0.3; 1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="14" y="9" class="term-header" fill="{branch_color}" font-size="10.5">ACTIVE</text>
</g>

<!-- Terminal Execution Body -->
<g transform="translate(24, 62)" class="term-mono">

  <!-- CMD 1: whoami -->
  <g>
    <text x="0" y="0" fill="{prompt_color}" font-weight="600">$</text>
    <text x="20" y="0" fill="{cmd_color}" clip-path="url(#c1-clip)">whoami</text>
    
    <rect y="-12" width="7.5" height="15" rx="1.5" fill="{cursor_color}">
      <animate attributeName="x" 
               values="20; 20; 74; 74; 74; 20" 
               keyTimes="0; 0.03; 0.10; 0.13; 0.94; 1" 
               dur="14s" repeatCount="indefinite"/>
      <animate attributeName="opacity" 
               values="1; 0; 1; 1; 1; 0; 0" 
               keyTimes="0; 0.015; 0.03; 0.10; 0.125; 0.13; 1" 
               dur="14s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Output 1 -->
  <g transform="translate(20, 22)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.125; 0.14; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0">
      <tspan fill="{out_primary}" font-weight="600">Jatin Mehra</tspan>
      <tspan fill="{out_muted}"> · B.Tech Data Science &amp; AI @ </tspan>
      <tspan fill="{prompt_color}">IIT Guwahati</tspan>
      <tspan fill="{out_muted}"> (2025–2029)</tspan>
    </text>
  </g>

  <!-- CMD 2: ls projects/ -->
  <g transform="translate(0, 48)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.18; 0.185; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0" fill="{prompt_color}" font-weight="600">$</text>
    <text x="20" y="0" fill="{cmd_color}" clip-path="url(#c2-clip)">ls projects/</text>
    
    <rect y="-12" width="7.5" height="15" rx="1.5" fill="{cursor_color}">
      <animate attributeName="x" 
               values="20; 20; 122; 122; 122; 20" 
               keyTimes="0; 0.19; 0.28; 0.31; 0.94; 1" 
               dur="14s" repeatCount="indefinite"/>
      <animate attributeName="opacity" 
               values="0; 0; 1; 1; 1; 0; 0" 
               keyTimes="0; 0.185; 0.19; 0.28; 0.305; 0.31; 1" 
               dur="14s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Output 2: 4 Projects -->
  <g transform="translate(20, 70)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.31; 0.325; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0">
      <tspan fill="{c_meet}" font-weight="600">ai-meeting-assistant/</tspan>
      <tspan fill="{out_muted}">   </tspan>
      <tspan fill="{c_delay}" font-weight="600">land-delay-risk/</tspan>
      <tspan fill="{out_muted}">   </tspan>
      <tspan fill="{c_vit}" font-weight="600">galaxy-vit/</tspan>
      <tspan fill="{out_muted}">   </tspan>
      <tspan fill="{c_mazdoor}" font-weight="600">mazdoor-evidence-kit/</tspan>
    </text>
  </g>

  <!-- CMD 3: meeting-assistant pipeline -->
  <g transform="translate(0, 96)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.365; 0.37; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0" fill="{prompt_color}" font-weight="600">$</text>
    <text x="20" y="0" fill="{cmd_color}" clip-path="url(#c3-clip)">meeting-assistant --audio keynote.wav --verify</text>
    
    <rect y="-12" width="7.5" height="15" rx="1.5" fill="{cursor_color}">
      <animate attributeName="x" 
               values="20; 20; 402; 402; 402; 20" 
               keyTimes="0; 0.38; 0.54; 0.57; 0.94; 1" 
               dur="14s" repeatCount="indefinite"/>
      <animate attributeName="opacity" 
               values="0; 0; 1; 1; 1; 0; 0" 
               keyTimes="0; 0.37; 0.38; 0.54; 0.565; 0.57; 1" 
               dur="14s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Output 3a: Faster-Whisper + Mini-Equalizer -->
  <g transform="translate(20, 118)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.575; 0.59; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0">
      <tspan fill="{prompt_color}" font-weight="600">[Faster-Whisper]</tspan>
      <tspan fill="{out_dim}"> Transcribed 42m audio in 8.4s · </tspan>
      <tspan fill="{success}" font-weight="600">RTF 0.03x (Fast)</tspan>
    </text>
    <!-- Dancing Mini-Equalizer Waveform -->
    <g transform="translate(390, -10)">
      <rect x="0" y="4" width="2" height="8" rx="1" fill="{prompt_color}">
        <animate attributeName="height" values="8; 14; 6; 12; 8" dur="0.7s" repeatCount="indefinite"/>
        <animate attributeName="y" values="4; 1; 5; 2; 4" dur="0.7s" repeatCount="indefinite"/>
      </rect>
      <rect x="4" y="2" width="2" height="12" rx="1" fill="{prompt_color}">
        <animate attributeName="height" values="12; 5; 14; 7; 12" dur="0.7s" repeatCount="indefinite"/>
        <animate attributeName="y" values="2; 5.5; 1; 4.5; 2" dur="0.7s" repeatCount="indefinite"/>
      </rect>
      <rect x="8" y="5" width="2" height="6" rx="1" fill="{prompt_color}">
        <animate attributeName="height" values="6; 13; 7; 15; 6" dur="0.7s" repeatCount="indefinite"/>
        <animate attributeName="y" values="5; 1.5; 4.5; 0.5; 5" dur="0.7s" repeatCount="indefinite"/>
      </rect>
      <rect x="12" y="3" width="2" height="10" rx="1" fill="{prompt_color}">
        <animate attributeName="height" values="10; 4; 12; 6; 10" dur="0.7s" repeatCount="indefinite"/>
        <animate attributeName="y" values="3; 6; 2; 5; 3" dur="0.7s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>

  <!-- Output 3b: Ground Truth Verification -->
  <g transform="translate(20, 138)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.63; 0.645; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0">
      <tspan fill="{success}" font-weight="600">&#x2713; </tspan>
      <tspan fill="{out_dim}">Verified </tspan>
      <tspan fill="{out_primary}" font-weight="600">14 action items, 4 decisions</tspan>
      <tspan fill="{out_muted}"> against transcript context</tspan>
    </text>
  </g>

  <!-- BLOCK 4: Ready Active Prompt -->
  <g transform="translate(0, 164)">
    <animate attributeName="opacity" 
             values="0; 0; 1; 1; 0; 0" 
             keyTimes="0; 0.68; 0.69; 0.88; 0.94; 1" 
             dur="14s" repeatCount="indefinite"/>
    <text x="0" y="0" fill="{prompt_color}" font-weight="600">$</text>
    
    <rect x="20" y="-12" width="7.5" height="15" rx="1.5" fill="{cursor_color}">
      <animate attributeName="opacity" 
               values="1; 0; 1; 0; 1; 0; 1; 0; 1; 0; 1" 
               keyTimes="0; 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9; 1" 
               dur="2.5s" repeatCount="indefinite"/>
    </rect>
  </g>

</g>
</svg>"""
    write_card("terminal.svg", content)


# ---- 3 · Project Cards (meeting, delay, vision, mazdoor) -----------------------
CARD_W = 434
CARD_H = 226


def build_project_card(filename, category, title, desc_lines, tags, accent_color, right_svg, delay):
    w, h = CARD_W, CARD_H
    css = font_face() + BASE_CSS
    
    # Generate description lines
    desc_svg = []
    y_start = 58
    for i, line in enumerate(desc_lines):
        y = y_start + i * 17
        desc_svg.append(
            f'<text class="f" style="animation-delay:{delay + 0.15 + i * 0.04:.2f}s" '
            f'x="0" y="{y:.1f}" font-family="{SANS}" font-size="11.5" fill="{INK_SOFT}">{escape(line)}</text>'
        )
    desc_str = "\n    ".join(desc_svg)

    # Generate tag pills (anchored at y=137)
    tags_svg = []
    cur_x = 0
    for j, tag in enumerate(tags):
        tag_w = round(len(tag) * 5.8 + 14)
        tags_svg.append(
            f'<g class="f" style="animation-delay:{delay + 0.32 + j * 0.05:.2f}s" transform="translate({cur_x}, 137)">\n'
            f'      <rect width="{tag_w}" height="20" rx="4" fill="{PAPER}" stroke="{BORDER}" stroke-width="0.8"/>\n'
            f'      <text x="{tag_w / 2:.1f}" y="13.5" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{INK_SOFT}">{escape(tag)}</text>\n'
            f'    </g>'
        )
        cur_x += tag_w + 6
    tags_str = "\n    ".join(tags_svg)

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)} - {escape(category)}">
<title>{escape(title)}</title>
<style>{css}</style>
<defs>
  <clipPath id="card-clip-{filename}"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".4"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>

<!-- Card Surface -->
<g clip-path="url(#card-clip-{filename})">
  <rect width="{w}" height="{h}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
  <rect class="sh" style="animation-delay:{delay + 1.2:.2f}s" x="0" y="0" width="120" height="{h}" fill="url(#card-sheen)" transform="translate(-280 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<!-- Left Content Block -->
<g transform="translate(24, 28)">
  <!-- Category Tag -->
  <g class="f" style="animation-delay:{delay:.2f}s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{accent_color}"/>
    <text x="12" y="6.5" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" font-weight="600" fill="{accent_color}">{escape(category)}</text>
  </g>
  
  <!-- Title -->
  <text class="f" style="animation-delay:{delay + 0.1:.2f}s" x="0" y="34" font-family="{SANS}" font-weight="600" font-size="18.5" fill="{INK}" letter-spacing="-0.3">
    {escape(title)}
  </text>
  
  <!-- Description (What I worked on) -->
  <g>
    {desc_str}
  </g>

  <!-- Divider -->
  <line class="f" style="animation-delay:{delay + 0.3:.2f}s" x1="0" y1="125" x2="234" y2="125" stroke="#ebebe6" stroke-width="0.8"/>

  <!-- Tech Stack Tag Pills -->
  {tags_str}

  <!-- Interactive Action Arrow -->
  <text class="nu" x="224" y="152" font-family="{MONO}" font-size="13" font-weight="600" fill="{accent_color}">&#8599;</text>
</g>

<!-- Right Schematic Visual Box -->
<g transform="translate(274, 18)">
  <rect class="f" style="animation-delay:{delay + 0.15:.2f}s" width="138" height="190" rx="10" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
  {right_svg}
</g>
</svg>"""
    write_card(f"{filename}.svg", content)
    if filename == "vision":
        write_card("vision-transformers.svg", content)


def generate_project_cards():
    # 1. meeting.svg
    meeting_visual = f"""
  <text class="f" style="animation-delay:0.4s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">SPEECH WAVEFORM</text>
  <path class="r" style="animation-delay:0.5s" d="M 14 50 h 10 l 4 -8 l 6 16 l 7 -22 l 7 28 l 8 -18 l 6 12 l 8 -8 h 30" 
        fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <line class="f" style="animation-delay:0.6s" x1="14" y1="76" x2="106" y2="76" stroke="#d5d5cf" stroke-width="2" stroke-linecap="round"/>
  <line class="f" style="animation-delay:0.65s" x1="14" y1="88" x2="84" y2="88" stroke="#dcdcd7" stroke-width="2" stroke-linecap="round"/>
  <text class="f" style="animation-delay:0.7s" x="14" y="116" font-family="{MONO}" font-size="9" fill="{MUTED}">16 kHz log-mel · 0.4s</text>
  
  <!-- Verified check badge -->
  <g transform="translate(14, 134)" class="f" style="animation-delay:0.75s">
    <rect width="118" height="24" rx="4" fill="#fff1f2" stroke="#fecdd3" stroke-width="1"/>
    <path d="M 10 12 l 3 3 l 6 -6" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-linecap="round"/>
    <text x="24" y="15" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{BLUE}">EVIDENCE GROUNDED</text>
  </g>
  <text class="f" style="animation-delay:0.85s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{BLUE}">&#x2713; Verified Decisions</text>
"""
    meeting_desc = [
        "Inter IIT ML bootcamp pipeline turning",
        "audio into minutes & action items.",
        "Faster-Whisper transcription checked",
        "against ground-truth evidence."
    ]
    build_project_card(
        "meeting", "SPEECH PIPELINE", "AI Meeting Assistant",
        meeting_desc, ["Faster-Whisper", "Verification"],
        BLUE, meeting_visual, 0.1
    )

    # 2. delay.svg
    delay_visual = f"""
  <text class="f" style="animation-delay:0.45s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">SHAP ATTRIBUTION</text>
  
  <g transform="translate(14, 38)" font-family="{MONO}" font-size="8.5">
    <text x="0" y="10" fill="{INK_SOFT}">Clearance</text>
    <rect class="r" style="animation-delay:0.55s" x="52" y="3" width="54" height="8" rx="2" fill="{AMBER}"/>
    
    <text x="0" y="28" fill="{INK_SOFT}">Disputes</text>
    <rect class="r" style="animation-delay:0.65s" x="52" y="21" width="40" height="8" rx="2" fill="{AMBER}" opacity="0.85"/>
    
    <text x="0" y="46" fill="{INK_SOFT}">Budget</text>
    <rect class="r" style="animation-delay:0.72s" x="52" y="39" width="30" height="8" rx="2" fill="{AMBER}" opacity="0.65"/>

    <text x="0" y="64" fill="{INK_SOFT}">Buffer</text>
    <rect class="r" style="animation-delay:0.78s" x="52" y="57" width="20" height="8" rx="2" fill="#71717a"/>
    <line x1="52" y1="0" x2="52" y2="70" stroke="#d5d5cf" stroke-width="1"/>
  </g>
  
  <!-- Risk Score -->
  <g transform="translate(14, 134)" class="f" style="animation-delay:0.85s">
    <rect width="110" height="24" rx="4" fill="#fef3c7" stroke="#fde68a" stroke-width="1"/>
    <text x="12" y="16" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{AMBER}">RISK INDEX: 78.4%</text>
  </g>
  <text class="f" style="animation-delay:0.95s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{AMBER}">High Delay Probability</text>
"""
    delay_desc = [
        "Smart India Hackathon PS 26017.",
        "Compares ML classifiers for infra delay",
        "risk; uses SHAP attribution to explain",
        "predictions on unlabeled projects."
    ]
    build_project_card(
        "delay", "EXPLAINABLE ML", "Land Delay Prediction",
        delay_desc, ["LightGBM", "XGBoost", "SHAP"],
        AMBER, delay_visual, 0.2
    )

    # 3. vision.svg
    vision_blue = "#2563eb"
    vision_visual = f"""
  <text class="f" style="animation-delay:0.5s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">ViT ATTENTION MAP</text>
  
  <!-- Astronomical Galaxy Drawing -->
  <g transform="translate(69, 74)">
    <ellipse cx="0" cy="0" rx="46" ry="19" transform="rotate(-26)" fill="#eff6ff" fill-opacity="0.9"/>
    <ellipse cx="0" cy="0" rx="28" ry="10" transform="rotate(-26)" fill="#dbeafe" fill-opacity="0.9"/>
    <circle cx="0" cy="0" r="2.5" fill="{vision_blue}"/>
    <circle cx="18" cy="-10" r="1.2" fill="{vision_blue}"/>
    <circle cx="-22" cy="12" r="1" fill="{vision_blue}"/>
    <circle cx="30" cy="14" r="1.5" fill="{vision_blue}"/>
    <circle cx="-14" cy="-14" r="0.8" fill="{vision_blue}"/>
    
    <!-- Single attended patch token outline -->
    <rect class="r" style="animation-delay:0.7s" x="-10" y="-10" width="20" height="20" fill="none" stroke="{vision_blue}" stroke-width="1.2" stroke-dasharray="2 2"/>
  </g>
  
  <!-- Model Badge -->
  <g transform="translate(14, 134)" class="f" style="animation-delay:0.8s">
    <rect width="110" height="24" rx="4" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="10" y="16" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{vision_blue}">DINOv2 EMBEDDINGS</text>
  </g>
  <text class="f" style="animation-delay:0.9s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{vision_blue}">DESI Legacy Survey</text>
"""
    vision_desc = [
        "DINOv2 representations on DESI Legacy",
        "Survey galaxy images, plus a compact",
        "DINO student–teacher model trained",
        "end-to-end on CIFAR-10."
    ]
    build_project_card(
        "vision", "COMPUTER VISION", "Vision Transformers",
        vision_desc, ["PyTorch", "DINOv2", "CIFAR-10"],
        vision_blue, vision_visual, 0.3
    )

    # 4. mazdoor.svg
    mazdoor_visual = f"""
  <text class="f" style="animation-delay:0.55s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">WORK LOG LEDGER</text>
  
  <!-- Ledger Slip -->
  <g transform="translate(14, 38)">
    <rect width="110" height="82" rx="4" fill="{WHITE}" stroke="#dcdcd7" stroke-width="1"/>
    
    <g font-family="{MONO}" font-size="8.5">
      <text x="8" y="18" fill="{INK_SOFT}">Shift 08h</text>
      <text x="102" y="18" text-anchor="end" fill="{GREEN}">₹650</text>
      <line x1="8" y1="24" x2="102" y2="24" stroke="#ebebe6" stroke-width="0.75"/>
      
      <text x="8" y="38" fill="{INK_SOFT}">Shift 08h</text>
      <text x="102" y="38" text-anchor="end" fill="{GREEN}">₹650</text>
      <line x1="8" y1="44" x2="102" y2="44" stroke="#ebebe6" stroke-width="0.75"/>

      <text x="8" y="58" fill="{MUTED}">Overtime 02h</text>
      <text x="102" y="58" text-anchor="end" fill="{GREEN}">₹200</text>
      <line x1="8" y1="64" x2="102" y2="64" stroke="#ebebe6" stroke-width="0.75"/>

      <text x="8" y="74" fill="{MUTED}">Total</text>
      <text x="102" y="74" text-anchor="end" font-weight="600" fill="{INK}">₹1,500</text>
    </g>
  </g>
  
  <!-- Proof Badge -->
  <g transform="translate(14, 134)" class="f" style="animation-delay:0.85s">
    <rect width="110" height="24" rx="4" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1"/>
    <text x="12" y="16" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{GREEN}">TAMPER-EVIDENT</text>
  </g>
  <text class="f" style="animation-delay:0.95s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{GREEN}">&#x2713; 100% Offline Vault</text>
"""
    mazdoor_desc = [
        "Mobile-first offline workflow for daily-wage",
        "workers to log shifts, reconcile wage",
        "payments, and organize tamper-",
        "evident records they choose to share."
    ]
    build_project_card(
        "mazdoor", "CIVIC TECH", "Mazdoor Evidence Kit",
        mazdoor_desc, ["Offline-first", "LocalStorage"],
        GREEN, mazdoor_visual, 0.4
    )


# ---- 4 · activity.svg (Monthly Bars Chart) -------------------------------------
def build_activity():
    w, h = 880, 260
    with open(DATA_FILE) as f:
        data = json.load(f)

    css = font_face() + BASE_CSS
    monthly = data["monthly"][-12:]
    best = max(monthly[:-1] or monthly, key=lambda m: m["total"])
    top = max(best["total"], 1)

    x0, x1, base, maxh, gap = 44, 580, 214, 105, 10
    bw = (x1 - x0 - gap * (len(monthly) - 1)) / len(monthly)
    bars = []
    for i, m in enumerate(monthly):
        partial = i == len(monthly) - 1
        is_best = m is best
        bh = max(4, round(m["total"] / top * maxh))
        x = x0 + i * (bw + gap)
        fill = BLUE if is_best else ("#d4d4ce" if partial else INK)
        label = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
        bars.append(
            f'<rect class="g" style="animation-delay:{0.3 + i * 0.05:.2f}s" x="{x:.1f}" y="{base - bh}" '
            f'width="{bw:.1f}" height="{bh}" rx="3" fill="{fill}"><title>{label}: {m["total"]:,}</title></rect>'
            f'<text class="f" style="animation-delay:{0.3 + i * 0.05:.2f}s" x="{x + bw / 2:.1f}" y="{base + 20}" '
            f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{label}</text>'
        )
        if is_best:
            bars.append(
                f'<text class="p" style="animation-delay:0.9s" x="{x + bw / 2:.1f}" y="{base - bh - 8}" '
                f'text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="600" fill="{BLUE}">{m["total"]:,}</text>'
            )

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    streak_note = "current streak, and the longest" if cs >= ls else f"current streak, longest {ls}"
    total_days = len(data["days"])
    stats = [
        (f'{data["total_contributions"]:,} <tspan font-style="italic">contributions</tspan>', "in the last 12 months"),
        (f'{data["active_days"]}<tspan fill="#8e8e93"> / {total_days}</tspan>', "days with a commit"),
        (f'{cs} <tspan font-style="italic">days</tspan>', streak_note),
    ]
    side = []
    for i, (big, small) in enumerate(stats):
        y = 86 + i * 62
        side.append(
            f'<g class="r" style="animation-delay:{0.5 + i * 0.1:.2f}s">'
            f'<text x="630" y="{y}" font-family="{SERIF}" font-size="30" fill="{INK}">{big}</text>'
            f'<text x="630" y="{y + 19}" font-family="{SANS}" font-size="12.5" fill="{MUTED}">{small}</text></g>'
        )
        if i < 2:
            side.append(f'<line x1="630" y1="{y + 32}" x2="836" y2="{y + 32}" stroke="{BORDER}" stroke-width="1"/>')

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub contribution activity">
<title>GitHub activity in the last year</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
<text class="f" style="animation-delay:0.1s" x="44" y="44" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" style="animation-delay:0.2s" x="42" y="84" font-family="{SERIF}" font-size="38" fill="{INK}">Contribution Activity</text>
{''.join(bars)}
{''.join(side)}
</svg>"""
    write_card("activity.svg", content)


# ---- 5 · Social and Platform Icons ---------------------------------------------
def generate_social_icons():
    def tile_svg(brand, inner_svg):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="42" height="42" viewBox="0 0 42 42" role="img" aria-label="{brand}">
<title>{brand}</title>
<defs>
  <filter id="shadow-{brand}" x="-10%" y="-10%" width="120%" height="120%">
    <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.06"/>
  </filter>
</defs>
<rect width="42" height="42" rx="10" fill="{WHITE}" stroke="{BORDER}" stroke-width="1.2" filter="url(#shadow-{brand})"/>
<g transform="translate(9, 9)">
{inner_svg}
</g>
</svg>"""

    is_dark = WHITE in ["#1e1d1b", "#141416", "#0d1117", "#161b22"]
    github_fill = "#f0ebe1" if is_dark else "#181717"
    leetcode_dark = "#f0ebe1" if is_dark else "#262626"

    linkedin_inner = """<path fill="#0077b5" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>"""

    leetcode_inner = f"""<g>
  <path fill="#ffa116" d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.762-1.823.762s-1.357-.295-1.824-.762L4.57 15.349a2.58 2.58 0 0 1 0-3.647l5.188-5.188a2.58 2.58 0 0 1 3.647 0l2.697 2.608a.748.748 0 0 1-1.058 1.058l-2.697-2.608a1.085 1.085 0 0 0-1.531 0L5.628 12.76a1.085 1.085 0 0 0 0 1.531l5.188 5.189c.423.423 1.108.423 1.531 0l2.697-2.608a.748.748 0 0 1 1.058 1.058z"/>
  <path fill="{leetcode_dark}" d="M20.823 14.283l-5.188 5.188a.748.748 0 0 1-1.058-1.058l5.188-5.189a1.085 1.085 0 0 0 0-1.531l-5.188-5.188a.748.748 0 0 1 1.058-1.058l5.188 5.188a2.58 2.58 0 0 1 0 3.648z"/>
  <path fill="#8a8a8e" d="M8.077 12.75h7.846a.75.75 0 0 0 0-1.5H8.077a.75.75 0 0 0 0 1.5z"/>
</g>"""

    codeforces_inner = """<g transform="translate(0, 1)">
  <rect x="1.5" y="8" width="5.5" height="13" rx="1.5" fill="#1F8ACB"/>
  <rect x="9.25" y="2" width="5.5" height="19" rx="1.5" fill="#FCD239"/>
  <rect x="17" y="5" width="5.5" height="16" rx="1.5" fill="#E34343"/>
</g>"""

    github_inner = f"""<path fill="{github_fill}" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>"""

    icons = {
        "icon-linkedin": ("LinkedIn", linkedin_inner),
        "icon-leetcode": ("LeetCode", leetcode_inner),
        "icon-codeforces": ("Codeforces", codeforces_inner),
        "icon-github": ("GitHub", github_inner),
    }

    for name, (label, svg_code) in icons.items():
        write_card(f"{name}.svg", tile_svg(label, svg_code))

    # Also generate pill badge versions
    pills = [
        ("pill-linkedin", 112, "LinkedIn", linkedin_inner),
        ("pill-leetcode", 114, "LeetCode", leetcode_inner),
        ("pill-codeforces", 126, "Codeforces", codeforces_inner),
        ("pill-github", 128, "Repositories", github_inner)
    ]
    for name, w, label, icon in pills:
        h = 32
        pill_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<title>{label}</title>
<style>
  .lbl {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 500; fill: {INK}; }}
</style>
<rect width="{w}" height="{h}" rx="16" fill="{WHITE}" stroke="{BORDER}" stroke-width="1.2"/>
<g transform="translate(10, 8) scale(0.666)">
  {icon}
</g>
<text x="34" y="20.5" class="lbl">{label}</text>
</svg>"""
        write_card(f"{name}.svg", pill_svg)



# ---- 6 · About Me 4-Card 2x2 Bento Grid ----------------------------------------
def generate_about_cards():
    w, h = 380, 152
    css = font_face() + """
.serif { font-family: 'Instrument Serif', Georgia, serif; }
.sans { font-family: Geist, system-ui, -apple-system, sans-serif; }
.mono { font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace; }
.f { opacity: 0; animation: fade .8s ease-out both; }
.r { opacity: 0; animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.live { animation: pulse 2s ease-in-out infinite; }
"""

    # 1. about-leetcode.svg
    leetcode_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Problem Solving &amp; Algorithms - LeetCode">
<title>Problem Solving &amp; Algorithms — LeetCode</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(20, 18)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.1s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="#ffa116"/>
    <text x="12" y="6" class="mono" font-size="9.5" letter-spacing="1" fill="#ffa116" font-weight="600">01 / PROBLEM SOLVING</text>
  </g>

  <!-- Title -->
  <text x="0" y="30" class="serif r" style="animation-delay:0.2s" font-size="20.5" fill="{INK}">
    Data Structures &amp; LeetCode
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.3s" font-size="11.5" fill="{INK_SOFT}">
    <tspan x="0" y="52">Deconstructing complex problems into optimal time</tspan>
    <tspan x="0" y="69">&amp; space complexity. Active practice across graphs,</tspan>
    <tspan x="0" y="86">trees, dynamic programming, and systems design.</tspan>
  </text>

  <!-- Action: LeetCode Pill -->
  <g transform="translate(0, 106)" class="f" style="animation-delay:0.4s">
    <a href="https://leetcode.com/u/JatinMehra08/" target="_blank">
    <g>
      <rect width="170" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(10, 5) scale(0.666)">
        <path fill="#ffa116" d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.762-1.823.762s-1.357-.295-1.824-.762L4.57 15.349a2.58 2.58 0 0 1 0-3.647l5.188-5.188a2.58 2.58 0 0 1 3.647 0l2.697 2.608a.748.748 0 0 1-1.058 1.058l-2.697-2.608a1.085 1.085 0 0 0-1.531 0L5.628 12.76a1.085 1.085 0 0 0 0 1.531l5.188 5.189c.423.423 1.108.423 1.531 0l2.697-2.608a.748.748 0 0 1 1.058 1.058z"/>
        <path fill="{INK}" d="M20.823 14.283l-5.188 5.188a.748.748 0 0 1-1.058-1.058l5.188-5.189a1.085 1.085 0 0 0 0-1.531l-5.188-5.188a.748.748 0 0 1 1.058-1.058l5.188 5.188a2.58 2.58 0 0 1 0 3.648z"/>
        <path fill="#8a8a8e" d="M8.077 12.75h7.846a.75.75 0 0 0 0-1.5H8.077a.75.75 0 0 0 0 1.5z"/>
      </g>
      <text x="34" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="{INK}">LeetCode Profile</text>
      <text x="148" y="18.5" class="mono" font-size="11" fill="#ffa116">&#8599;</text>
    </g>
    </a>
  </g>
</g>
</svg>"""
    write_card("about-leetcode.svg", leetcode_svg)
    write_card("about-leetcode-v2.svg", leetcode_svg)
    write_card("about-leetcode-v3.svg", leetcode_svg)

    # 2. about-codeforces.svg
    codeforces_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Competitive Programming &amp; Contests - Codeforces">
<title>Competitive Programming &amp; Contests — Codeforces</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(20, 18)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.15s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="#1F8ACB"/>
    <text x="12" y="6" class="mono" font-size="9.5" letter-spacing="1" fill="#1F8ACB" font-weight="600">02 / COMPETITIVE</text>
  </g>

  <!-- Title -->
  <text x="0" y="30" class="serif r" style="animation-delay:0.25s" font-size="20.5" fill="{INK}">
    Contests &amp; Codeforces
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.35s" font-size="11.5" fill="{INK_SOFT}">
    <tspan x="0" y="52">Competing under the clock in rated rounds.</tspan>
    <tspan x="0" y="69">Sharpening mathematical intuition, fast invariants,</tspan>
    <tspan x="0" y="86">and high-speed, bug-free implementations.</tspan>
  </text>

  <!-- Action: Codeforces Pill -->
  <g transform="translate(0, 106)" class="f" style="animation-delay:0.45s">
    <a href="https://codeforces.com/profile/crazyguy96" target="_blank">
    <g>
      <rect width="176" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(11, 5) scale(0.666)">
        <rect x="1.5" y="8" width="5.5" height="13" rx="1.5" fill="#1F8ACB"/>
        <rect x="9.25" y="2" width="5.5" height="19" rx="1.5" fill="#FCD239"/>
        <rect x="17" y="5" width="5.5" height="16" rx="1.5" fill="#E34343"/>
      </g>
      <text x="34" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="{INK}">Codeforces Profile</text>
      <text x="154" y="18.5" class="mono" font-size="11" fill="#1F8ACB">&#8599;</text>
    </g>
    </a>
  </g>
</g>
</svg>"""
    write_card("about-codeforces.svg", codeforces_svg)
    write_card("about-codeforces-v2.svg", codeforces_svg)
    write_card("about-codeforces-v3.svg", codeforces_svg)

    # 3. about-sports.svg
    sports_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Beyond the Screen - Athletics and Team Instincts">
<title>Beyond the Screen — Athletics</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(20, 18)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.2s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="#059669"/>
    <text x="12" y="6" class="mono" font-size="9.5" letter-spacing="1" fill="#059669" font-weight="600">03 / ATHLETICS</text>
  </g>

  <!-- Title -->
  <text x="0" y="30" class="serif r" style="animation-delay:0.3s" font-size="20.5" fill="{INK}">
    Reflexes &amp; Team Rhythm
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.4s" font-size="11.5" fill="{INK_SOFT}">
    <tspan x="0" y="52">Badminton is a big part of my life, alongside</tspan>
    <tspan x="0" y="69">cricket and football. Sports taught me to think fast,</tspan>
    <tspan x="0" y="86">stay calm under pressure, and collaborate in teams.</tspan>
  </text>

  <!-- Sports Badges: Single Symmetric Row -->
  <g transform="translate(0, 106)" class="f" style="animation-delay:0.5s">
    <!-- Badminton -->
    <g>
      <rect width="112" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(9, 4) scale(0.9)">
        <ellipse cx="9" cy="10" rx="5" ry="6" transform="rotate(-30 9 10)" fill="none" stroke="#059669" stroke-width="1.3"/>
        <line x1="6" y1="7" x2="12" y2="13" stroke="#10b981" stroke-width="0.7"/>
        <line x1="6" y1="13" x2="12" y2="7" stroke="#10b981" stroke-width="0.7"/>
        <line x1="6.5" y1="15" x2="2.5" y2="19.5" stroke="#047857" stroke-width="1.4" stroke-linecap="round"/>
        <g transform="translate(14, 1.5)">
          <ellipse cx="2.5" cy="4.5" rx="1.8" ry="1.3" fill="#047857"/>
          <path d="M 2.5 3.5 L 6.5 0.5 M 2.5 4.5 L 7.5 4 M 2.5 5.5 L 6.5 7.5" stroke="#059669" stroke-width="0.9" stroke-linecap="round"/>
        </g>
      </g>
      <text x="33" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="{INK}">Badminton</text>
    </g>

    <!-- Cricket -->
    <g transform="translate(118, 0)">
      <rect width="94" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(9, 5) scale(0.9)">
        <line x1="3" y1="3" x2="6" y2="6" stroke="#92400e" stroke-width="1.6" stroke-linecap="round"/>
        <path d="M 6 6 L 14 14 A 1.2 1.2 0 0 1 12 16 L 4.5 8.5 Z" fill="#d97706" stroke="#b45309" stroke-width="0.8"/>
        <circle cx="14" cy="5.5" r="3" fill="#dc2626"/>
        <path d="M 12.5 4.5 Q 14 5.5 15.5 6.5" fill="none" stroke="#ffffff" stroke-width="0.6" stroke-dasharray="0.8 0.8"/>
      </g>
      <text x="31" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="{INK}">Cricket</text>
    </g>

    <!-- Football -->
    <g transform="translate(218, 0)">
      <rect width="98" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(9, 5) scale(0.9)">
        <circle cx="10" cy="10" r="6.5" fill="#ffffff" stroke="#1e293b" stroke-width="1"/>
        <polygon points="10,7.5 12.5,9.2 11.5,12 8.5,12 7.5,9.2" fill="#1e293b"/>
        <line x1="10" y1="7.5" x2="10" y2="4" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="12.5" y1="9.2" x2="15.5" y2="8" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="11.5" y1="12" x2="14" y2="14.5" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="8.5" y1="12" x2="6" y2="14.5" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="7.5" y1="9.2" x2="4.5" y2="8" stroke="#1e293b" stroke-width="0.75"/>
      </g>
      <text x="31" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="{INK}">Football</text>
    </g>
  </g>
</g>
</svg>"""
    write_card("about-sports.svg", sports_svg)
    write_card("about-athletics.svg", sports_svg)
    write_card("about-athletics-v2.svg", sports_svg)
    write_card("about-athletics-v3.svg", sports_svg)

    # 4. about-work.svg
    work_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Opportunities - Internships in Data Science and AI">
<title>Opportunities — Seeking Internships</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(20, 18)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.25s">
    <circle cx="3.5" cy="3.5" r="3.5" fill="{BLUE}" class="live"/>
    <text x="14" y="7" class="mono" font-size="9.5" letter-spacing="1" fill="{BLUE}" font-weight="600">04 / ACTIVE CANDIDATE</text>
  </g>

  <!-- Title -->
  <text x="0" y="30" class="serif r" style="animation-delay:0.35s" font-size="20.5" fill="{INK}">
    Seeking Internships
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.45s" font-size="11.5" fill="{INK_SOFT}">
    <tspan x="0" y="52">Sophomore @ IIT Guwahati (Data Science &amp; AI).</tspan>
    <tspan x="0" y="69">Looking for Data Science, AI/ML or software</tspan>
    <tspan x="0" y="86">development roles for Summer 2027 or 2028.</tspan>
  </text>

  <!-- Action: LinkedIn Pill Button -->
  <g transform="translate(0, 106)" class="f" style="animation-delay:0.55s">
    <a href="https://www.linkedin.com/in/jatin-mehra-51a675380/" target="_blank">
    <g>
      <rect width="192" height="28" rx="14" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
      <g transform="translate(10, 6) scale(0.666)">
        <path fill="#0077b5" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
      </g>
      <text x="34" y="18.5" class="sans" font-size="12" font-weight="600" fill="{INK}">Connect on LinkedIn</text>
      <text x="170" y="18.5" class="mono" font-size="12" fill="{BLUE}">&#8599;</text>
    </g>
    </a>
  </g>
</g>
</svg>"""
    write_card("about-work.svg", work_svg)
    write_card("about-internships.svg", work_svg)
    write_card("about-internships-v2.svg", work_svg)
    write_card("about-internships-v3.svg", work_svg)

    # Legacy about-code.svg
    write_card("about-code.svg", leetcode_svg)


# ---- 6 · Skills Bento Cards (skills-languages, skills-ml, skills-tools) -------
SKILL_ICONS_DEFS = """
  <!-- Python -->
  <g id="icon-py">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path fill="#387EB8" d="M127.279 29C76.5066 29 79.6772 51.018 79.6772 51.018L79.7338 73.8284H128.185V80.6772H60.4893C60.4893 80.6772 28 76.9926 28 128.222C28 179.452 56.3573 177.636 56.3573 177.636H73.2812V153.863C73.2812 153.863 72.369 125.506 101.186 125.506H149.24C149.24 125.506 176.239 125.942 176.239 99.4123V55.5461C176.239 55.5461 180.338 29 127.279 29ZM100.563 44.339C105.384 44.339 109.28 48.2351 109.28 53.0556C109.28 57.8761 105.384 61.7723 100.563 61.7723C95.7426 61.7723 91.8465 57.8761 91.8465 53.0556C91.8465 48.2351 95.7426 44.339 100.563 44.339Z"/>
    <path fill="#FFC331" d="M128.721 227.958C179.493 227.958 176.323 205.941 176.323 205.941L176.266 183.13H127.815V176.281H195.511C195.511 176.281 228 179.966 228 128.736C228 77.5062 199.643 79.323 199.643 79.323H182.719V103.096C182.719 103.096 183.631 131.453 154.814 131.453H106.76C106.76 131.453 79.7607 131.016 79.7607 157.546V201.412C79.7607 201.412 75.6615 227.958 128.721 227.958ZM155.437 212.619C150.616 212.619 146.72 208.723 146.72 203.903C146.72 199.082 150.616 195.186 155.437 195.186C160.257 195.186 164.154 199.082 164.154 203.903C164.154 208.723 160.257 212.619 155.437 212.619Z"/>
  </g>
  <!-- C++ -->
  <g id="icon-cpp">
    <rect width="256" height="256" fill="#00599C" rx="60"/>
    <path fill="#fff" d="M110.759 210.517C65.1254 210.517 28 173.392 28 127.759C28 82.1254 65.1254 45 110.759 45C140.204 45 167.667 60.8458 182.427 86.3533L146.611 107.079C139.224 94.3111 125.485 86.3793 110.759 86.3793C87.9416 86.3793 69.3793 104.942 69.3793 127.759C69.3793 150.575 87.9416 169.138 110.759 169.138C125.486 169.138 139.225 161.206 146.613 148.436L182.429 169.161C167.669 194.671 140.206 210.517 110.759 210.517Z"/>
    <path fill="#fff" d="M193.517 123.161H184.321V113.965H175.127V123.161H165.931V132.356H175.127V141.552H184.321V132.356H193.517V123.161Z"/>
    <path fill="#fff" d="M228 123.161H218.804V113.965H209.61V123.161H200.414V132.356H209.61V141.552H218.804V132.356H228V123.161Z"/>
  </g>
  <!-- C -->
  <g id="icon-c">
    <rect width="256" height="256" rx="60" fill="#394AAB"/>
    <path d="M134.001 33C169.144 33 199.828 52.0863 216.262 80.4561L216.102 80.183L174.753 103.991C166.607 90.1977 151.672 80.8892 134.54 80.6975L134.001 80.6945C107.875 80.6945 86.6945 101.874 86.6945 127.999C86.6945 136.543 88.9723 144.552 92.9335 151.469C101.088 165.704 116.416 175.306 134.001 175.306C151.693 175.306 167.109 165.582 175.222 151.195L175.025 151.54L216.311 175.458C200.057 203.588 169.794 222.615 135.059 222.994L134.001 223C98.746 223 67.9753 203.796 51.582 175.276C43.5791 161.353 39 145.212 39 127.999C39 75.5334 81.5323 33 134.001 33Z" fill="white"/>
  </g>
  <!-- Bash -->
  <g id="icon-bash">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path d="M60 76 l 44 34 l -44 34" stroke="#47B353" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <line x1="116" y1="144" x2="176" y2="144" stroke="#fff" stroke-width="18" stroke-linecap="round"/>
  </g>
  <!-- HTML5 -->
  <g id="icon-html">
    <rect width="256" height="256" fill="#E14E1D" rx="60"/>
    <path fill="#fff" d="M48 38L56.6098 134.593H167.32L163.605 176.023L127.959 185.661L92.38 176.037L90.0012 149.435H57.9389L62.5236 200.716L127.951 218.888L193.461 200.716L202.244 102.655H85.8241L82.901 69.9448H205.041H205.139L208 38H48Z"/>
    <path fill="#EBEBEB" d="M128 38H48L56.6098 134.593H128V102.655H85.8241L82.901 69.9448H128V38Z"/>
    <path fill="#EBEBEB" d="M128 185.647L127.959 185.661L92.38 176.037L90.0012 149.435H57.9388L62.5236 200.716L127.951 218.888L128 218.874V185.647Z"/>
  </g>
  <!-- CSS3 -->
  <g id="icon-css">
    <rect width="256" height="256" rx="60" fill="#0277BD"/>
    <path d="M53.7527 102.651L56.6155 134.593H128.096V102.651H53.7527Z" fill="#EBEBEB"/>
    <path d="M128.095 38H127.985H48L50.9036 69.9423H128.095V38Z" fill="#EBEBEB"/>
    <path d="M128.095 218.841V185.608L127.955 185.645L92.3813 176.04L90.1072 150.564H72.821H58.0425L62.5175 200.718L127.948 218.882L128.095 218.841Z" fill="#EBEBEB"/>
    <path d="M167.318 134.593L163.61 176.019L127.985 185.635V218.866L193.468 200.718L193.948 195.321L201.454 111.229L202.233 102.651L208 38H127.985V69.9423H172.994L170.088 102.651H127.985V134.593H167.318Z" fill="white"/>
  </g>
  <!-- JavaScript -->
  <g id="icon-js">
    <rect width="256" height="256" rx="60" fill="#F0DB4F"/>
    <path d="M67.3117 213.932L86.9027 202.076C90.6821 208.777 94.1202 214.447 102.367 214.447C110.272 214.447 115.256 211.355 115.256 199.327V117.529H139.314V199.667C139.314 224.584 124.708 235.926 103.398 235.926C84.1533 235.926 72.9819 225.959 67.3113 213.93" fill="#323330"/>
    <path d="M152.381 211.354L171.969 200.013C177.126 208.434 183.828 214.62 195.684 214.62C205.653 214.62 212.009 209.636 212.009 202.762C212.009 194.514 205.479 191.592 194.481 186.782L188.468 184.203C171.111 176.815 159.597 167.535 159.597 147.945C159.597 129.901 173.345 116.153 194.826 116.153C210.12 116.153 221.118 121.481 229.022 135.4L210.291 147.429C206.166 140.04 201.7 137.119 194.826 137.119C187.78 137.119 183.312 141.587 183.312 147.429C183.312 154.646 187.78 157.568 198.09 162.037L204.104 164.614C224.553 173.379 236.067 182.313 236.067 202.418C236.067 224.072 219.055 235.928 196.2 235.928C173.861 235.928 159.426 225.274 152.381 211.354" fill="#323330"/>
  </g>
  <!-- Markdown -->
  <g id="icon-markdown">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path stroke="#fff" stroke-width="10" d="M217 69H39C33.4772 69 29 73.4772 29 79V177C29 182.523 33.4772 187 39 187H217C222.523 187 227 182.523 227 177V79C227 73.4772 222.523 69 217 69Z"/>
    <path fill="#fff" d="M54 162V94H74L94 119L114 94H134V162H114V123L94 148L74 123V162H54ZM179 162L149 129H169V94H189V129H209L179 162Z"/>
  </g>

  <!-- PyTorch -->
  <g id="icon-pytorch">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M180.975 90.4153L167.567 103.824C189.508 125.765 189.508 161.115 167.567 182.65C145.625 204.591 110.275 204.591 88.7404 182.65C66.7991 160.709 66.7991 125.359 88.7404 103.824L123.481 69.0835L128.357 64.2077V38L75.9413 90.4153C46.6862 119.67 46.6862 166.804 75.9413 196.059C105.196 225.314 152.33 225.314 180.975 196.059C210.23 166.6 210.23 119.67 180.975 90.4153Z" fill="#EE4C2C"/>
    <path d="M154.77 87.1705C160.156 87.1705 164.522 82.8045 164.522 77.4188C164.522 72.0331 160.156 67.667 154.77 67.667C149.385 67.667 145.019 72.0331 145.019 77.4188C145.019 82.8045 149.385 87.1705 154.77 87.1705Z" fill="#EE4C2C"/>
  </g>
  <!-- TensorFlow -->
  <g id="icon-tensorflow">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M124.228 229L90.623 208.89V90.31L40 120.459L40.123 75.545L124.228 26V229ZM131.784 26V229L165.393 208.89V151.781L190.763 166.895L190.612 127.833L165.393 112.988V90.31L216 120.459L215.878 75.545L131.784 26Z" fill="#FF6F00"/>
  </g>
  <!-- Scikit-Learn -->
  <g id="icon-sklearn">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M181.405 160.654C205.831 136.23 209.891 100.69 190.472 81.2731C171.056 61.8579 135.518 65.9168 111.094 90.3399C86.6691 114.764 93.7346 161.426 102.028 169.721C108.73 176.423 156.982 185.078 181.405 160.654Z" fill="#F89939"/>
    <path d="M81.1816 125.361C67.0116 111.192 46.3899 108.833 35.1213 120.1C23.8556 131.367 26.211 151.991 40.3838 166.159C54.5567 180.333 81.6323 176.234 86.4412 171.42C90.3327 167.535 95.3558 139.533 81.1816 125.361Z" fill="#3499CD"/>
  </g>
  <!-- OpenCV -->
  <g id="icon-opencv">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M104.028 122.58C95.08 117.414 88.087 109.44 84.1332 99.895C80.1794 90.3496 79.4857 79.7664 82.1598 69.7866C84.8339 59.8069 90.7262 50.9884 98.923 44.6988C107.12 38.4092 117.163 35 127.495 35C137.826 35 147.87 38.4092 156.066 44.6988C164.263 50.9884 170.155 59.8069 172.829 69.7866C175.504 79.7664 174.81 90.3496 170.856 99.895C166.902 109.44 159.909 117.414 150.962 122.58L136.831 98.1043C140.39 96.0492 143.172 92.8769 144.745 89.0795C146.318 85.282 146.594 81.0717 145.53 77.1015C144.466 73.1312 142.122 69.623 138.861 67.1208C135.6 64.6186 131.605 63.2623 127.495 63.2623C123.384 63.2623 119.389 64.6186 116.128 67.1208C112.867 69.623 110.523 73.1312 109.459 77.1015C108.395 81.0717 108.671 85.282 110.244 89.0795C111.817 92.8769 114.599 96.0492 118.159 98.1043L104.028 122.58Z" fill="#FF0101"/>
    <path d="M204.533 133.943C213.481 139.109 220.474 147.083 224.427 156.628C228.381 166.173 229.075 176.756 226.401 186.736C223.727 196.716 217.834 205.534 209.638 211.824C201.441 218.114 191.398 221.523 181.066 221.523C170.734 221.523 160.691 218.114 152.494 211.824C144.297 205.534 138.405 196.716 135.731 186.736C133.057 176.756 133.751 166.173 137.704 156.628C141.658 147.083 148.651 139.109 157.599 133.943L171.73 158.419C168.17 160.474 165.388 163.646 163.815 167.443C162.242 171.241 161.967 175.451 163.03 179.421C164.094 183.392 166.438 186.9 169.699 189.402C172.96 191.904 176.956 193.261 181.066 193.261C185.176 193.261 189.172 191.904 192.433 189.402C195.693 186.9 198.038 183.392 199.101 179.421C200.165 175.451 199.889 171.241 198.316 167.443C196.743 163.646 193.961 160.474 190.402 158.419L204.533 133.943Z" fill="#0101FF"/>
    <path d="M121.868 174.589C121.868 184.921 118.459 194.964 112.169 203.16C105.88 211.357 97.0613 217.25 87.0816 219.924C77.1018 222.598 66.5186 221.904 56.9733 217.95C47.4279 213.996 39.4539 207.003 34.288 198.056C29.1221 189.108 27.053 178.706 28.4016 168.463C29.7502 158.219 34.4411 148.707 41.7467 141.401C49.0524 134.096 58.5646 129.405 68.808 128.056C79.0514 126.708 89.4536 128.777 98.4012 133.943L84.27 158.419C80.7104 156.363 76.5721 155.54 72.497 156.077C68.4219 156.613 64.6376 158.479 61.7312 161.386C58.8248 164.292 56.9586 168.077 56.4221 172.152C55.8856 176.227 56.7088 180.365 58.7639 183.925C60.8191 187.484 63.9914 190.266 67.7888 191.839C71.5862 193.412 75.7965 193.688 79.7668 192.624C83.737 191.561 87.2453 189.216 89.7475 185.955C92.2496 182.695 93.6059 178.699 93.6059 174.589H121.868Z" fill="#01FF01"/>
  </g>
  <!-- NumPy -->
  <g id="icon-numpy">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <g transform="translate(38.4, 38.4) scale(1.4)">
      <path fill="#4DABCF" d="m55.012 26.006-21.38-10.789L10.154 26.93l21.969 11.027Zm9.808 4.951L87.241 42.28 63.982 53.955l-22-11.043Zm29.948-15.581 23.037 11.552L97.2 37.272 74.735 25.938ZM84.853 10.4 64.113 0 43.598 10.24 64.97 21.014ZM68.64 99.702V128l25.122-12.537-.023-28.31ZM93.727 77.27l-.028-28.012-25.06 12.458V89.74Zm30.158-5.246v28.41l-21.43 10.69-.017-28.279zm0-9.935V34.25l-21.47 10.673.016 28.068z"/>
      <path fill="#4c75cf" d="m59.77 61.716-16.918-8.512V89.97s-20.7-44.033-22.612-47.99c-.246-.513-1.263-1.07-1.522-1.209-3.731-1.947-14.603-7.45-14.603-7.45v64.977l15.04 8.063V72.382s20.478 39.346 20.689 39.78c.214.429 2.257 4.57 4.459 6.028 2.92 1.939 15.458 9.477 15.458 9.477z"/>
    </g>
  </g>
  <!-- Pandas -->
  <g id="icon-pandas">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <g transform="translate(48, 38.4) scale(1.4)">
      <path fill="#ffffff" d="M46.236 7.567h13.99v29.047h-13.99Zm0 59.668h13.99V96.28h-13.99Z"/>
      <path fill="#ffca00" d="M46.236 45.092h13.99v13.705h-13.99Z"/>
      <path fill="#ffffff" d="M23.763 31.446h13.989V128h-13.99ZM68.245 91.2h13.99v29.046h-13.99Zm0-59.72h13.99v29.047h-13.99Z"/>
      <path fill="#e70488" d="M68.245 69.011h13.99v13.705h-13.99Z"/>
      <path fill="#ffffff" d="M90.248 0h13.99v96.554h-13.99Z"/>
    </g>
  </g>
  <!-- Jupyter -->
  <g id="icon-jupyter">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <g transform="translate(38.4, 38.4) scale(1.4)">
      <path d="M109.766 7.281a7.691 7.691 0 01-1.09 4.282 7.583 7.583 0 01-3.262 2.949 7.49 7.49 0 01-4.34.62 7.525 7.525 0 01-3.953-1.913A7.642 7.642 0 0195.137 5a7.606 7.606 0 012.629-3.531 7.509 7.509 0 014.136-1.461 7.51 7.51 0 015.422 1.996 7.627 7.627 0 012.438 5.273zm0 0" fill="#989798"/>
      <path d="M65.758 96.79c-20.098 0-37.649-7.364-46.766-18.267a49.95 49.95 0 0018.102 24.254 49.251 49.251 0 0028.676 9.215 49.279 49.279 0 0028.675-9.215 49.917 49.917 0 0018.094-24.254C103.406 89.426 85.855 96.79 65.758 96.79zm0 0M65.75 25.883c20.098 0 37.652 7.367 46.766 18.265a49.95 49.95 0 00-18.102-24.253 49.27 49.27 0 00-28.672-9.22 49.27 49.27 0 00-28.672 9.22A49.909 49.909 0 0018.97 44.148C28.102 33.27 45.652 25.883 65.75 25.883zm0 0" fill="#f37726"/>
      <path d="M38.164 117.984a9.671 9.671 0 01-1.371 5.399 9.5 9.5 0 01-9.59 4.504 9.405 9.405 0 01-4.98-2.418 9.671 9.671 0 01-2.809-4.797 9.73 9.73 0 01.313-5.567 9.624 9.624 0 013.328-4.453 9.466 9.466 0 0112.043.688 9.63 9.63 0 013.066 6.648zm0 0" fill="#989798"/>
      <path d="M21.285 23.418a5.53 5.53 0 01-3.14-.816 5.627 5.627 0 01-2.618-5.672 5.612 5.612 0 011.407-2.95 5.593 5.593 0 012.789-1.664 5.46 5.46 0 013.238.184 5.539 5.539 0 012.586 1.969 5.66 5.66 0 01-.399 7.129 5.557 5.557 0 01-3.867 1.82zm0 0" fill="#989798"/>
    </g>
  </g>
  <!-- FastAPI -->
  <g id="icon-fastapi">
    <rect width="256" height="256" rx="60" fill="#049789"/>
    <path d="M127.5 41C79.743 41 41 79.743 41 127.5C41 175.257 79.743 214 127.5 214C175.257 214 214 175.257 214 127.5C214 79.743 175.257 41 127.5 41ZM122.993 196.839V142.581H92.8306L136.167 58.1615V112.419H165.203L122.993 196.839Z" fill="white"/>
  </g>

  <!-- Git -->
  <g id="icon-git">
    <rect width="256" height="256" fill="#F03C2E" rx="60"/>
    <path fill="#fff" d="M224.225 119.094L136.906 31.775C135.711 30.5787 134.291 29.6298 132.729 28.9824C131.166 28.3349 129.491 28.0017 127.8 28.0017C126.109 28.0017 124.434 28.3349 122.871 28.9824C121.309 29.6298 119.889 30.5787 118.694 31.775L100.569 49.9L123.569 72.9C128.919 71.025 135.044 72.3062 139.306 76.5687C141.335 78.6014 142.752 81.1638 143.394 83.9632C144.036 86.7626 143.878 89.6862 142.937 92.4L165.106 114.569C170.469 112.719 176.656 113.912 180.937 118.206C182.361 119.63 183.49 121.32 184.26 123.18C185.03 125.04 185.426 127.033 185.426 129.046C185.425 131.059 185.029 133.052 184.258 134.912C183.487 136.771 182.358 138.461 180.934 139.884C179.511 141.308 177.821 142.436 175.961 143.206C174.101 143.977 172.108 144.373 170.095 144.372C168.082 144.372 166.088 143.975 164.229 143.205C162.369 142.434 160.679 141.305 159.256 139.881C154.756 135.381 153.644 128.756 155.919 123.212L135.244 102.537V156.944C136.745 157.686 138.116 158.666 139.306 159.844C140.729 161.267 141.858 162.956 142.629 164.816C143.399 166.675 143.795 168.668 143.795 170.681C143.795 172.694 143.399 174.687 142.629 176.546C141.858 178.406 140.729 180.096 139.306 181.519C137.883 182.942 136.193 184.071 134.334 184.841C132.474 185.611 130.481 186.008 128.469 186.008C126.456 186.008 124.463 185.611 122.604 184.841C120.744 184.071 119.054 182.942 117.631 181.519C116.206 180.096 115.076 178.407 114.305 176.548C113.533 174.688 113.136 172.694 113.136 170.681C113.136 168.668 113.533 166.675 114.305 164.815C115.076 162.955 116.206 161.266 117.631 159.844C119.112 158.369 120.756 157.25 122.65 156.5V101.587C120.825 100.837 119.112 99.7312 117.631 98.2437C115.479 96.0943 114.016 93.3526 113.428 90.3684C112.841 87.3841 113.155 84.2924 114.331 81.4875L91.6437 58.8125L31.7687 118.625C30.5716 119.821 29.6219 121.241 28.9739 122.804C28.3259 124.367 27.9924 126.042 27.9924 127.734C27.9924 129.426 28.3259 131.102 28.9739 132.665C29.6219 134.228 30.5716 135.648 31.7687 136.844L119.094 224.156C120.289 225.352 121.709 226.301 123.271 226.949C124.834 227.596 126.509 227.929 128.2 227.929C129.891 227.929 131.566 227.596 133.129 226.949C134.691 226.301 136.111 225.352 137.306 224.156L224.225 137.375C225.422 136.179 226.372 134.759 227.02 133.196C227.668 131.633 228.001 129.958 228.001 128.266C228.001 126.574 227.668 124.898 227.02 123.335C226.372 121.772 225.422 120.352 224.225 119.156"/>
  </g>
  <!-- GitHub -->
  <g id="icon-github">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M128.001 30C72.7791 30 28 74.7708 28 130.001C28 174.184 56.6533 211.668 96.3867 224.891C101.384 225.817 103.219 222.722 103.219 220.081C103.219 217.696 103.126 209.819 103.083 201.463C75.2631 207.512 69.3927 189.664 69.3927 189.664C64.8437 178.105 58.2894 175.032 58.2894 175.032C49.2163 168.825 58.9733 168.953 58.9733 168.953C69.0151 169.658 74.3026 179.258 74.3026 179.258C83.2217 194.546 97.6965 190.126 103.403 187.571C104.301 181.107 106.892 176.696 109.752 174.199C87.5405 171.67 64.1913 163.095 64.1913 124.778C64.1913 113.86 68.0977 104.939 74.4947 97.9362C73.4564 95.4175 70.0335 85.2465 75.4635 71.4722C75.4635 71.4722 83.8609 68.7845 102.971 81.7226C110.948 79.5069 119.502 78.3958 128.001 78.3577C136.499 78.3958 145.061 79.5069 153.052 81.7226C172.139 68.7845 180.525 71.4722 180.525 71.4722C185.968 85.2465 182.544 95.4175 181.505 97.9362C187.917 104.939 191.797 113.86 191.797 124.778C191.797 163.187 168.403 171.644 146.135 174.119C149.722 177.223 152.918 183.308 152.918 192.638C152.918 206.018 152.802 216.787 152.802 220.081C152.802 222.742 154.602 225.86 159.671 224.878C199.383 211.64 228 174.169 228 130.001C228 74.7708 183.227 30 128.001 30Z" fill="white"/>
  </g>
  <!-- VS Code -->
  <g id="icon-vscode">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path fill="#2489CA" d="M33.7158 100.208C33.7158 100.208 28.9814 96.795 34.6627 92.2381L47.8994 80.402C47.8994 80.402 51.6869 76.4172 55.6915 79.8891L177.84 172.368V216.714C177.84 216.714 177.781 223.678 168.844 222.908L33.7158 100.208Z"/>
    <path fill="#1070B3" d="M65.1997 128.792L33.7157 157.415C33.7157 157.415 30.4805 159.822 33.7157 164.123L48.3333 177.418C48.3333 177.418 51.8052 181.147 56.9341 176.905L90.3119 151.596L65.1997 128.792Z"/>
    <path fill="#0877B9" d="M120.474 129.029L178.215 84.9391L177.84 40.83C177.84 40.83 175.374 31.2033 167.148 36.2139L90.312 106.145L120.474 129.029Z"/>
    <path fill="#3C99D4" d="M168.844 222.968C172.198 226.4 176.262 225.276 176.262 225.276L221.259 203.103C227.019 199.177 226.21 194.305 226.21 194.305V61.8982C226.21 56.0788 220.252 54.0667 220.252 54.0667L181.253 35.267C172.731 30 167.148 36.2139 167.148 36.2139C167.148 36.2139 174.328 31.0455 177.84 40.83V215.905C177.84 217.109 177.583 218.292 177.071 219.358C176.045 221.429 173.816 223.362 168.47 222.553L168.844 222.968Z"/>
  </g>
  <!-- Linux -->
  <g id="icon-linux">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path fill="#ECEFF1" d="M85.9493 199.926L110.48 213.546H147.576L182.278 187.491L197.834 146.632L161.935 103.405L151.764 79.1268L102.104 80.9032L102.702 94.5228L93.1291 112.287L78.1713 141.303L75.1797 165.581L85.9493 199.926Z"/>
    <path fill="#263238" d="M187.064 114.656C177.491 101.036 169.713 92.7463 165.525 75.5738C161.337 58.4013 166.722 63.1386 163.132 48.3347C161.337 40.6367 158.345 35.3073 155.354 31.1622C151.764 27.0171 147.576 24.6485 145.182 24.0563C139.798 21.0956 127.233 16.3583 111.677 24.6485C95.5223 32.9387 97.3172 50.7033 100.309 86.8248C100.309 89.1934 99.7105 92.1542 98.5139 94.5228C96.1206 99.8522 91.9324 104.589 88.3425 108.735C84.1543 114.656 79.9661 120.578 76.9746 127.091C69.7948 140.711 63.2134 157.883 65.0083 164.397C67.9999 163.805 105.694 220.652 105.694 221.836C108.087 221.244 118.258 221.244 127.233 221.244C139.798 220.652 146.977 220.06 157.149 222.428C157.149 220.652 156.55 218.875 156.55 217.099C156.55 213.546 157.149 210.585 157.747 206.44C158.345 203.479 158.944 200.519 159.542 196.966C153.559 202.295 142.789 208.217 132.618 209.993C123.643 211.769 108.685 208.809 101.505 199.926C102.104 199.926 103.3 199.926 103.899 199.334C105.694 198.742 107.489 198.15 108.087 196.966C109.882 194.005 108.685 191.044 107.489 189.268C106.292 187.491 97.3173 180.977 93.1291 177.425C88.9409 173.872 86.5476 172.095 84.1544 169.727C84.1544 169.727 80.5645 166.174 79.3678 164.989C78.1712 163.805 77.5729 162.621 76.9746 162.028C75.778 159.068 75.1796 155.515 75.778 150.778C76.3763 144.264 78.7695 138.934 81.7611 133.013C82.9577 130.644 85.9493 125.907 85.9493 125.907C85.9493 125.907 75.778 150.778 81.1628 158.476C81.1628 158.476 81.7611 150.778 84.1544 143.08C85.9493 137.75 88.9409 130.052 92.5307 125.907C96.1206 121.762 105.095 106.366 105.694 96.8914C105.694 92.7463 106.292 88.6012 106.292 85.6405C103.899 83.2718 145.781 77.3503 148.174 83.864C148.772 86.2326 157.149 107.55 161.935 118.801C164.328 124.131 167.32 128.868 169.115 134.789C170.91 141.303 172.106 150.185 172.106 159.068C172.106 160.844 172.106 163.805 171.508 166.766C172.705 166.766 196.039 141.895 168.517 121.17C168.517 121.17 185.269 128.868 185.868 144.264C186.466 156.699 181.081 166.766 179.885 168.542C180.483 168.542 192.449 173.872 193.047 173.872C195.441 173.872 200.227 172.095 200.227 172.095C200.826 170.319 202.62 165.581 202.62 163.805C206.809 150.185 196.637 128.276 187.064 114.656V114.656Z"/>
    <circle cx="111" cy="64" r="11" fill="#ECEFF1"/>
    <circle cx="138" cy="63" r="11" fill="#ECEFF1"/>
    <circle cx="112" cy="65" r="5" fill="#212121"/>
    <circle cx="137" cy="65" r="5" fill="#212121"/>
    <path fill="#FFC107" d="M108 90C104 88 101 85 101 82C101 78 104 77 107 74C108 73 114 67 121 67C127 67 135 72 138 73C143 74 149 75 148 79C148 85 147 86 141 89C137 90 129 97 124 97C121 97 118 97 115 96C114 96 111 93 108 90Z"/>
  </g>
  <!-- Docker -->
  <g id="icon-docker">
    <rect width="256" height="256" fill="#2396ED" rx="60"/>
    <path fill="#fff" d="M141.187 122.123H161.904V103.379H141.187V122.123ZM116.525 122.123H137.241V103.379H116.525V122.123ZM92.3554 122.123H113.072V103.379H92.3554V122.123ZM68.1859 122.123H88.4093V103.379H68.1859V122.123ZM43.5233 122.123H64.2399V103.379H43.5233V122.123ZM68.1859 99.4333H88.4093V80.6896H68.1859V99.4333ZM92.3554 99.4333H113.072V80.6896H92.3554V99.4333ZM116.525 99.4333H137.241V80.6896H116.525V99.4333ZM116.525 76.7436H137.241V58H116.525V76.7436ZM228 113.738C228 113.738 219.121 105.352 200.871 108.312C198.898 94.0075 183.607 85.6222 183.607 85.6222C183.607 85.6222 169.303 102.886 179.661 122.123C176.702 123.603 171.769 125.576 164.37 125.576H28.7257C26.2594 134.948 26.2594 197.097 94.3284 197.097C143.16 197.097 179.661 174.408 196.925 132.974C222.574 134.948 228 113.738 228 113.738Z"/>
  </g>
  <!-- Ubuntu -->
  <g id="icon-ubuntu">
    <rect width="256" height="256" rx="60" fill="#242938"/>
    <path d="M127.5 206.25C170.992 206.25 206.25 170.992 206.25 127.5C206.25 84.0076 170.992 48.75 127.5 48.75C84.0076 48.75 48.75 84.0076 48.75 127.5C48.75 170.992 84.0076 206.25 127.5 206.25Z" fill="#F47421"/>
    <path d="M127.5 165.694C148.594 165.694 165.694 148.594 165.694 127.5C165.694 106.406 148.594 89.3062 127.5 89.3062C106.406 89.3062 89.3062 106.406 89.3062 127.5C89.3062 148.594 106.406 165.694 127.5 165.694Z" stroke="white" stroke-width="8.55"/>
    <path d="M73.9499 142.266C82.1048 142.266 88.7157 135.655 88.7157 127.5C88.7157 119.345 82.1048 112.734 73.9499 112.734C65.795 112.734 59.1841 119.345 59.1841 127.5C59.1841 135.655 65.795 142.266 73.9499 142.266Z" fill="#F47421"/>
    <path d="M73.95 138.013C79.7562 138.013 84.4631 133.306 84.4631 127.5C84.4631 121.694 79.7562 116.987 73.95 116.987C68.1439 116.987 63.437 121.694 63.437 127.5C63.437 133.306 68.1439 138.013 73.95 138.013Z" fill="white"/>
    <path d="M141.487 73.7415C137.41 80.8039 139.83 89.8345 146.892 93.9119C153.954 97.9894 162.985 95.5697 167.062 88.5073C171.14 81.4449 168.72 72.4143 161.658 68.3368C154.595 64.2594 145.565 66.6791 141.487 73.7415Z" fill="#F47421"/>
  </g>
  <!-- Postman -->
  <g id="icon-postman">
    <rect width="256" height="256" rx="60" fill="#FF6C37"/>
    <path d="M169.061 88.6123L118.521 139.153L104.268 124.901C153.971 75.1986 158.882 79.5101 169.061 88.6123Z" fill="#EEEEEE"/>
    <path d="M133.012 153.645L119.239 139.872L169.78 89.3315C183.314 102.984 163.073 125.141 133.012 153.645Z" fill="#EEEEEE"/>
    <path d="M104.508 125.26L114.688 135.44C114.927 135.68 114.927 135.919 114.688 136.159C114.568 136.279 114.568 136.279 114.449 136.279L93.3693 140.83C92.292 140.95 91.3337 140.231 91.0942 139.153C90.9744 138.554 91.214 137.956 91.5733 137.596L103.789 125.38C104.029 125.14 104.388 125.02 104.508 125.26Z" fill="#EEEEEE"/>
    <path d="M195.769 60.5877C188.104 53.1625 175.768 53.4021 168.342 61.1867C160.917 68.9712 161.157 81.1871 168.941 88.6131C175.289 94.7207 184.871 95.7988 192.416 91.2476L178.762 77.5943L195.769 60.5877Z" fill="#EEEEEE"/>
  </g>
  <!-- VIM -->
  <g id="icon-vim">
    <rect width="256" height="256" fill="#242938" rx="60"/>
    <path fill="#019833" d="M135.498 39.4619C128.076 32.03 116.032 32.03 108.61 39.462L33.4081 114.765C26.0001 122.183 26.0001 134.199 33.4081 141.617L108.186 216.495C115.608 223.927 127.652 223.927 135.074 216.495L210.276 141.191C217.684 133.773 217.684 121.757 210.276 114.339L135.498 39.4619Z"/>
    <path fill="#fff" d="M161.769 40.7104L159.083 43.3988V53.2693L161.435 55.6235H173.86V65.1606L91.672 148.576V55.7425H105.331L108.133 52.9365V42.9482L105.546 40.9465H33.6672L31.3158 43.3007V53.5048L33.7069 55.8988H46.2085V216.316C46.2085 222.361 50.6553 227.485 56.6396 228.335V228.335C60.4891 228.883 64.3678 227.553 67.0718 224.759L235 51.2474V43.4001L232.315 40.7117L161.769 40.7104Z"/>
  </g>
"""


def generate_skills_cards():
    w, h = 284, 220
    css = font_face() + BASE_CSS

    # 1. skills-languages.svg
    lang_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Languages - Core and Systems Programming">
<title>Languages</title>
<style>{css}</style>
<defs>
  <clipPath id="card-clip-skills-lang"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".4"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  {SKILL_ICONS_DEFS}
</defs>

<!-- Card Surface -->
<g clip-path="url(#card-clip-skills-lang)">
  <rect width="{w}" height="{h}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
  <rect class="sh" style="animation-delay:1.1s" x="0" y="0" width="100" height="{h}" fill="url(#card-sheen)" transform="translate(-260 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(22, 24)">
  <!-- Category Tag -->
  <g class="f" style="animation-delay:0.1s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{BLUE}"/>
    <text x="12" y="6.5" font-family="{MONO}" font-size="10" letter-spacing="1.2" font-weight="600" fill="{BLUE}">LANGUAGES</text>
  </g>

  <!-- Title -->
  <text class="f" style="animation-delay:0.18s" x="0" y="32" font-family="{SANS}" font-weight="600" font-size="17" fill="{INK}">Core &amp; Systems</text>

  <!-- Row 1 Icons (Python, C++, C, Bash) -->
  <g class="f" style="animation-delay:0.25s">
    <g transform="translate(0, 48) scale(0.1484)"><use href="#icon-py"/></g>
    <g transform="translate(67, 48) scale(0.1484)"><use href="#icon-cpp"/></g>
    <g transform="translate(134, 48) scale(0.1484)"><use href="#icon-c"/></g>
    <g transform="translate(201, 48) scale(0.1484)"><use href="#icon-bash"/></g>
  </g>

  <!-- Row 2 Icons (HTML5, CSS3, JavaScript, Markdown) -->
  <g class="f" style="animation-delay:0.32s">
    <g transform="translate(0, 98) scale(0.1484)"><use href="#icon-html"/></g>
    <g transform="translate(67, 98) scale(0.1484)"><use href="#icon-css"/></g>
    <g transform="translate(134, 98) scale(0.1484)"><use href="#icon-js"/></g>
    <g transform="translate(201, 98) scale(0.1484)"><use href="#icon-markdown"/></g>
  </g>

  <!-- Divider -->
  <line class="f" style="animation-delay:0.4s" x1="0" y1="150" x2="240" y2="150" stroke="#ebebe6" stroke-width="0.8"/>

  <!-- Bottom Readout -->
  <g class="f" style="animation-delay:0.45s" transform="translate(0, 168)">
    <text x="0" y="0" font-family="{MONO}" font-size="9.5" fill="{MUTED}">&#x2713; C · C++ · Python · Web · MD</text>
    <text class="nu" x="240" y="0" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="600" fill="{BLUE}">&#8599;</text>
  </g>
</g>
</svg>"""
    write_card("skills-languages.svg", lang_svg)

    # 2. skills-ml.svg
    ml_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Machine Learning and AI - Models and Frameworks">
<title>Machine Learning &amp; AI</title>
<style>{css}</style>
<defs>
  <clipPath id="card-clip-skills-ml"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".4"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  {SKILL_ICONS_DEFS}
</defs>

<!-- Card Surface -->
<g clip-path="url(#card-clip-skills-ml)">
  <rect width="{w}" height="{h}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
  <rect class="sh" style="animation-delay:1.2s" x="0" y="0" width="100" height="{h}" fill="url(#card-sheen)" transform="translate(-260 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(22, 24)">
  <!-- Category Tag -->
  <g class="f" style="animation-delay:0.15s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{AMBER}"/>
    <text x="12" y="6.5" font-family="{MONO}" font-size="10" letter-spacing="1.2" font-weight="600" fill="{AMBER}">MACHINE LEARNING &amp; AI</text>
  </g>

  <!-- Title -->
  <text class="f" style="animation-delay:0.22s" x="0" y="32" font-family="{SANS}" font-weight="600" font-size="17" fill="{INK}">Models &amp; Frameworks</text>

  <!-- Row 1: PyTorch, TensorFlow, Scikit-Learn, OpenCV -->
  <g class="f" style="animation-delay:0.28s">
    <g transform="translate(0, 48) scale(0.1484)"><use href="#icon-pytorch"/></g>
    <g transform="translate(67, 48) scale(0.1484)"><use href="#icon-tensorflow"/></g>
    <g transform="translate(134, 48) scale(0.1484)"><use href="#icon-sklearn"/></g>
    <g transform="translate(201, 48) scale(0.1484)"><use href="#icon-opencv"/></g>
  </g>

  <!-- Row 2: NumPy, Pandas, Jupyter, FastAPI -->
  <g class="f" style="animation-delay:0.35s">
    <g transform="translate(0, 98) scale(0.1484)"><use href="#icon-numpy"/></g>
    <g transform="translate(67, 98) scale(0.1484)"><use href="#icon-pandas"/></g>
    <g transform="translate(134, 98) scale(0.1484)"><use href="#icon-jupyter"/></g>
    <g transform="translate(201, 98) scale(0.1484)"><use href="#icon-fastapi"/></g>
  </g>

  <!-- Divider -->
  <line class="f" style="animation-delay:0.42s" x1="0" y1="150" x2="240" y2="150" stroke="#ebebe6" stroke-width="0.8"/>

  <!-- Bottom Readout -->
  <g class="f" style="animation-delay:0.48s" transform="translate(0, 168)">
    <text x="0" y="0" font-family="{MONO}" font-size="9.5" fill="{AMBER}">&#x2713; PyTorch · TF · Scikit · NumPy</text>
    <text class="nu" x="240" y="0" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="600" fill="{AMBER}">&#8599;</text>
  </g>
</g>
</svg>"""
    write_card("skills-ml.svg", ml_svg)

    # 3. skills-tools.svg
    tools_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Environment and Tools - Developer Workflow">
<title>Environment &amp; Tools</title>
<style>{css}</style>
<defs>
  <clipPath id="card-clip-skills-tools"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  <linearGradient id="card-sheen" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".4"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  {SKILL_ICONS_DEFS}
</defs>

<!-- Card Surface -->
<g clip-path="url(#card-clip-skills-tools)">
  <rect width="{w}" height="{h}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
  <rect class="sh" style="animation-delay:1.3s" x="0" y="0" width="100" height="{h}" fill="url(#card-sheen)" transform="translate(-260 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<g transform="translate(22, 24)">
  <!-- Category Tag -->
  <g class="f" style="animation-delay:0.2s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{GREEN}"/>
    <text x="12" y="6.5" font-family="{MONO}" font-size="10" letter-spacing="1.2" font-weight="600" fill="{GREEN}">ENVIRONMENT &amp; TOOLS</text>
  </g>

  <!-- Title -->
  <text class="f" style="animation-delay:0.26s" x="0" y="32" font-family="{SANS}" font-weight="600" font-size="17" fill="{INK}">Developer Stack</text>

  <!-- Row 1: Git, GitHub, VS Code, Linux -->
  <g class="f" style="animation-delay:0.32s">
    <g transform="translate(0, 48) scale(0.1484)"><use href="#icon-git"/></g>
    <g transform="translate(67, 48) scale(0.1484)"><use href="#icon-github"/></g>
    <g transform="translate(134, 48) scale(0.1484)"><use href="#icon-vscode"/></g>
    <g transform="translate(201, 48) scale(0.1484)"><use href="#icon-linux"/></g>
  </g>

  <!-- Row 2: Docker, Ubuntu, Postman, VIM -->
  <g class="f" style="animation-delay:0.38s">
    <g transform="translate(0, 98) scale(0.1484)"><use href="#icon-docker"/></g>
    <g transform="translate(67, 98) scale(0.1484)"><use href="#icon-ubuntu"/></g>
    <g transform="translate(134, 98) scale(0.1484)"><use href="#icon-postman"/></g>
    <g transform="translate(201, 98) scale(0.1484)"><use href="#icon-vim"/></g>
  </g>

  <!-- Divider -->
  <line class="f" style="animation-delay:0.45s" x1="0" y1="150" x2="240" y2="150" stroke="#ebebe6" stroke-width="0.8"/>

  <!-- Bottom Readout -->
  <g class="f" style="animation-delay:0.5s" transform="translate(0, 168)">
    <text x="0" y="0" font-family="{MONO}" font-size="9.5" fill="{GREEN}">&#x2713; Git · Linux · Docker · VIM</text>
    <text class="nu" x="240" y="0" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="600" fill="{GREEN}">&#8599;</text>
  </g>
</g>
</svg>"""
    write_card("skills-tools.svg", tools_svg)


if __name__ == "__main__":
    print("generating all cards with Paper & Ink UI/UX...")
    build_hero()
    build_terminal()
    generate_project_cards()
    build_activity()
    generate_social_icons()
    generate_about_cards()
    generate_skills_cards()
    print("complete.")
