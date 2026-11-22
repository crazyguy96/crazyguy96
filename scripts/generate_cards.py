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

# Palette tokens: Paper & Ink with focused accents
WHITE = "#ffffff"
PAPER = "#f7f7f5"
BORDER = "#e4e4df"
BORDER_SOFT = "#eeeeea"
INK = "#111111"
INK_SOFT = "#4a4a4e"
MUTED = "#76767c"

# Project accents
BLUE = "#2563eb"
AMBER = "#d97706"
VIOLET = "#7c3aed"
GREEN = "#059669"

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
  <text class="f" style="animation-delay:0.85s" x="240" y="140" text-anchor="end" font-family="{MONO}" font-size="10" fill="{BLUE}">0% hallucination</text>
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
      <tspan fill="{success}" font-weight="600">0.00% WER</tspan>
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


def build_project_card(filename, category, title, desc_lines, tags, repo_slug, accent_color, right_svg, delay):
    w, h = CARD_W, CARD_H
    css = font_face() + BASE_CSS
    
    # Generate description lines
    desc_svg = []
    y_start = 56
    for i, line in enumerate(desc_lines):
        y = y_start + i * 16.5
        desc_svg.append(
            f'<text class="r" style="animation-delay:{delay + 0.12 + i * 0.04:.2f}s" '
            f'x="0" y="{y:.1f}" font-family="{SANS}" font-size="11.5" fill="{INK_SOFT}">{escape(line)}</text>'
        )
    desc_str = "\n    ".join(desc_svg)

    # Generate tag pills
    tags_svg = []
    cur_x = 0
    for j, tag in enumerate(tags):
        tag_w = round(len(tag) * 5.8 + 14)
        tags_svg.append(
            f'<g class="f" style="animation-delay:{delay + 0.3 + j * 0.05:.2f}s" transform="translate({cur_x}, 0)">\n'
            f'      <rect width="{tag_w}" height="19" rx="4" fill="{PAPER}" stroke="{BORDER}" stroke-width="0.8"/>\n'
            f'      <text x="{tag_w / 2:.1f}" y="13" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{INK_SOFT}">{escape(tag)}</text>\n'
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
<g transform="translate(22, 22)">
  <!-- Category Tag -->
  <g class="f" style="animation-delay:{delay:.2f}s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{accent_color}"/>
    <text x="12" y="6" font-family="{MONO}" font-size="10.5" letter-spacing="1" font-weight="600" fill="{accent_color}">{escape(category)}</text>
  </g>
  
  <!-- Title -->
  <text class="r" style="animation-delay:{delay + 0.08:.2f}s" x="0" y="32" font-family="{SANS}" font-weight="600" font-size="18.5" fill="{INK}" letter-spacing="-0.3">
    {escape(title)}
  </text>
  
  <!-- Description (What I worked on) -->
  <g>
    {desc_str}
  </g>

  <!-- Divider -->
  <line class="f" style="animation-delay:{delay + 0.28:.2f}s" x1="0" y1="127" x2="234" y2="127" stroke="#ebebe6" stroke-width="0.8"/>

  <!-- Tech Stack Tag Pills -->
  <g transform="translate(0, 137)">
    {tags_str}
  </g>

  <!-- Repo Action Link -->
  <g transform="translate(0, 175)" class="r" style="animation-delay:{delay + 0.42:.2f}s">
    <text x="0" y="0" font-family="{MONO}" font-size="11" font-weight="600" fill="{accent_color}">{escape(repo_slug)} &#8599;</text>
  </g>
</g>

<!-- Right Schematic Visual Box -->
<g transform="translate(274, 18)">
  <rect class="f" style="animation-delay:{delay + 0.15:.2f}s" width="138" height="190" rx="10" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
  {right_svg}
</g>
</svg>"""
    write_card(f"{filename}.svg", content)


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
    <rect width="110" height="24" rx="4" fill="#e8efff" stroke="#c7d8ff" stroke-width="1"/>
    <path d="M 10 12 l 3 3 l 6 -6" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-linecap="round"/>
    <text x="24" y="15" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{BLUE}">0% HALLUCINATION</text>
  </g>
  <text class="f" style="animation-delay:0.85s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{BLUE}">&#x2713; Transcript Grounded</text>
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
        "AI_Meeting_Assistant", BLUE, meeting_visual, 0.1
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
        "SIH_PS_ID_26017", AMBER, delay_visual, 0.2
    )

    # 3. vision.svg
    vision_visual = f"""
  <text class="f" style="animation-delay:0.5s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">ViT ATTENTION MAP</text>
  
  <!-- Astronomical Galaxy Drawing -->
  <g transform="translate(69, 74)">
    <ellipse cx="0" cy="0" rx="46" ry="19" transform="rotate(-26)" fill="#ede9fe" fill-opacity="0.8"/>
    <ellipse cx="0" cy="0" rx="28" ry="10" transform="rotate(-26)" fill="#ddd6fe" fill-opacity="0.9"/>
    <circle cx="0" cy="0" r="2.5" fill="{VIOLET}"/>
    <circle cx="18" cy="-10" r="1.2" fill="{VIOLET}"/>
    <circle cx="-22" cy="12" r="1" fill="{VIOLET}"/>
    <circle cx="30" cy="14" r="1.5" fill="{VIOLET}"/>
    <circle cx="-14" cy="-14" r="0.8" fill="{VIOLET}"/>
    
    <!-- Single attended patch token outline -->
    <rect class="r" style="animation-delay:0.7s" x="-10" y="-10" width="20" height="20" fill="none" stroke="{VIOLET}" stroke-width="1.2" stroke-dasharray="2 2"/>
  </g>
  
  <!-- Model Badge -->
  <g transform="translate(14, 134)" class="f" style="animation-delay:0.8s">
    <rect width="110" height="24" rx="4" fill="#ede9fe" stroke="#ddd6fe" stroke-width="1"/>
    <text x="10" y="16" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{VIOLET}">DINOv2 EMBEDDINGS</text>
  </g>
  <text class="f" style="animation-delay:0.9s" x="14" y="176" font-family="{MONO}" font-size="8.5" fill="{VIOLET}">DESI Legacy Survey</text>
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
        "Self-Supervised-Vit", VIOLET, vision_visual, 0.3
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
        "Mazdoor-Evidence-Kit", GREEN, mazdoor_visual, 0.4
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
<rect width="42" height="42" rx="10" fill="#ffffff" stroke="#e4e4df" stroke-width="1.2" filter="url(#shadow-{brand})"/>
<g transform="translate(9, 9)">
{inner_svg}
</g>
</svg>"""

    linkedin_inner = """<path fill="#0077b5" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>"""

    leetcode_inner = """<g>
  <path fill="#ffa116" d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.762-1.823.762s-1.357-.295-1.824-.762L4.57 15.349a2.58 2.58 0 0 1 0-3.647l5.188-5.188a2.58 2.58 0 0 1 3.647 0l2.697 2.608a.748.748 0 0 1-1.058 1.058l-2.697-2.608a1.085 1.085 0 0 0-1.531 0L5.628 12.76a1.085 1.085 0 0 0 0 1.531l5.188 5.189c.423.423 1.108.423 1.531 0l2.697-2.608a.748.748 0 0 1 1.058 1.058z"/>
  <path fill="#262626" d="M20.823 14.283l-5.188 5.188a.748.748 0 0 1-1.058-1.058l5.188-5.189a1.085 1.085 0 0 0 0-1.531l-5.188-5.188a.748.748 0 0 1 1.058-1.058l5.188 5.188a2.58 2.58 0 0 1 0 3.648z"/>
  <path fill="#8a8a8e" d="M8.077 12.75h7.846a.75.75 0 0 0 0-1.5H8.077a.75.75 0 0 0 0 1.5z"/>
</g>"""

    codeforces_inner = """<g transform="translate(0, 1)">
  <rect x="1.5" y="8" width="5.5" height="13" rx="1.5" fill="#1F8ACB"/>
  <rect x="9.25" y="2" width="5.5" height="19" rx="1.5" fill="#FCD239"/>
  <rect x="17" y="5" width="5.5" height="16" rx="1.5" fill="#E34343"/>
</g>"""

    github_inner = """<path fill="#181717" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>"""

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
  .lbl {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 500; fill: #111111; }}
</style>
<rect width="{w}" height="{h}" rx="16" fill="#ffffff" stroke="#e4e4df" stroke-width="1.2"/>
<g transform="translate(10, 8) scale(0.666)">
  {icon}
</g>
<text x="34" y="20.5" class="lbl">{label}</text>
</svg>"""
        write_card(f"{name}.svg", pill_svg)



# ---- 6 · About Me 3-Pillar Cards -----------------------------------------------
def generate_about_cards():
    w, h = 286, 216
    css = font_face() + """
.serif { font-family: 'Instrument Serif', Georgia, serif; }
.sans { font-family: Geist, system-ui, -apple-system, sans-serif; }
.mono { font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace; }
.f { opacity: 0; animation: fade .8s ease-out both; }
.r { opacity: 0; animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }
@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.live { animation: pulse 2s ease-in-out infinite; }
"""

    # 1. about-code.svg
    code_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Algorithms &amp; Systems - LeetCode and Codeforces">
<title>Algorithms &amp; Systems</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="#e4e4df" stroke-width="1"/>

<g transform="translate(22, 26)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.1s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="#d97706"/>
    <text x="12" y="6" class="mono" font-size="10" letter-spacing="1" fill="#d97706">01 / ALGORITHMS</text>
  </g>

  <!-- Title -->
  <text x="0" y="36" class="serif r" style="animation-delay:0.2s" font-size="22" fill="#111111">
    Data Structures &amp; Code
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.3s" font-size="12" fill="#4a4a4e">
    <tspan x="0" y="64">Breaking down complex problems</tspan>
    <tspan x="0" y="82">into optimal complexity, then turning</tspan>
    <tspan x="0" y="100">algorithms into working tools.</tspan>
  </text>

  <!-- Badges: LeetCode & Codeforces -->
  <g transform="translate(0, 126)" class="f" style="animation-delay:0.4s">
    <!-- LeetCode Pill -->
    <g>
      <rect width="112" height="28" rx="14" fill="#fcfcfb" stroke="#e4e4df" stroke-width="1"/>
      <g transform="translate(8, 6) scale(0.666)">
        <path fill="#ffa116" d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.762-1.823.762s-1.357-.295-1.824-.762L4.57 15.349a2.58 2.58 0 0 1 0-3.647l5.188-5.188a2.58 2.58 0 0 1 3.647 0l2.697 2.608a.748.748 0 0 1-1.058 1.058l-2.697-2.608a1.085 1.085 0 0 0-1.531 0L5.628 12.76a1.085 1.085 0 0 0 0 1.531l5.188 5.189c.423.423 1.108.423 1.531 0l2.697-2.608a.748.748 0 0 1 1.058 1.058z"/>
        <path fill="#262626" d="M20.823 14.283l-5.188 5.188a.748.748 0 0 1-1.058-1.058l5.188-5.189a1.085 1.085 0 0 0 0-1.531l-5.188-5.188a.748.748 0 0 1 1.058-1.058l5.188 5.188a2.58 2.58 0 0 1 0 3.648z"/>
        <path fill="#8a8a8e" d="M8.077 12.75h7.846a.75.75 0 0 0 0-1.5H8.077a.75.75 0 0 0 0 1.5z"/>
      </g>
      <text x="30" y="18" class="sans" font-size="11.5" font-weight="600" fill="#111111">LeetCode</text>
      <text x="96" y="18" class="mono" font-size="11" fill="#d97706">&#8599;</text>
    </g>

    <!-- Codeforces Pill -->
    <g transform="translate(120, 0)">
      <rect width="122" height="28" rx="14" fill="#fcfcfb" stroke="#e4e4df" stroke-width="1"/>
      <g transform="translate(8, 7) scale(0.666)">
        <rect x="1.5" y="8" width="5.5" height="13" rx="1.5" fill="#1F8ACB"/>
        <rect x="9.25" y="2" width="5.5" height="19" rx="1.5" fill="#FCD239"/>
        <rect x="17" y="5" width="5.5" height="16" rx="1.5" fill="#E34343"/>
      </g>
      <text x="30" y="18" class="sans" font-size="11.5" font-weight="600" fill="#111111">Codeforces</text>
      <text x="106" y="18" class="mono" font-size="11" fill="#1F8ACB">&#8599;</text>
    </g>
  </g>
</g>
</svg>"""
    write_card("about-code.svg", code_svg)

    # 2. about-sports.svg
    sports_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Beyond the Screen - Athletics and Team Instincts">
<title>Beyond the Screen</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="#e4e4df" stroke-width="1"/>

<g transform="translate(22, 22)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.15s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="#059669"/>
    <text x="12" y="6" class="mono" font-size="10" letter-spacing="1" fill="#059669">02 / ATHLETICS</text>
  </g>

  <!-- Title -->
  <text x="0" y="34" class="serif r" style="animation-delay:0.25s" font-size="22" fill="#111111">
    Reflexes &amp; Team Rhythm
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.35s" font-size="12" fill="#4a4a4e">
    <tspan x="0" y="56">Badminton is a big part of my life,</tspan>
    <tspan x="0" y="73">alongside cricket and football. Sports</tspan>
    <tspan x="0" y="90">taught me to think fast and collaborate.</tspan>
  </text>

  <!-- Tier 1: Badminton Hero Badge -->
  <g transform="translate(0, 108)" class="f" style="animation-delay:0.45s">
    <rect width="242" height="28" rx="8" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1"/>
    <!-- Authentic Badminton Racquet & Flying Shuttlecock Vector -->
    <g transform="translate(8, 4)">
      <ellipse cx="9" cy="10" rx="5" ry="6" transform="rotate(-30 9 10)" fill="none" stroke="#059669" stroke-width="1.3"/>
      <line x1="6" y1="7" x2="12" y2="13" stroke="#10b981" stroke-width="0.7"/>
      <line x1="6" y1="13" x2="12" y2="7" stroke="#10b981" stroke-width="0.7"/>
      <line x1="6.5" y1="15" x2="2.5" y2="19.5" stroke="#047857" stroke-width="1.4" stroke-linecap="round"/>
      <g transform="translate(14, 1.5)">
        <ellipse cx="2.5" cy="4.5" rx="1.8" ry="1.3" fill="#047857"/>
        <path d="M 2.5 3.5 L 6.5 0.5 M 2.5 4.5 L 7.5 4 M 2.5 5.5 L 6.5 7.5" stroke="#059669" stroke-width="0.9" stroke-linecap="round"/>
      </g>
    </g>
    <text x="36" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="#047857">Badminton</text>
    <text x="104" y="18.5" class="mono" font-size="10.5" fill="#059669">· Competitive Play</text>
  </g>

  <!-- Tier 2: Cricket & Football Badges -->
  <g transform="translate(0, 142)" class="f" style="animation-delay:0.55s">
    <!-- Cricket Badge -->
    <g>
      <rect width="117" height="28" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1"/>
      <g transform="translate(8, 4)">
        <line x1="3" y1="3" x2="6" y2="6" stroke="#92400e" stroke-width="1.6" stroke-linecap="round"/>
        <path d="M 6 6 L 14 14 A 1.2 1.2 0 0 1 12 16 L 4.5 8.5 Z" fill="#d97706" stroke="#b45309" stroke-width="0.8"/>
        <circle cx="14" cy="5.5" r="3" fill="#dc2626"/>
        <path d="M 12.5 4.5 Q 14 5.5 15.5 6.5" fill="none" stroke="#ffffff" stroke-width="0.6" stroke-dasharray="0.8 0.8"/>
      </g>
      <text x="32" y="18.5" class="sans" font-size="11" font-weight="600" fill="#92400e">Cricket</text>
    </g>

    <!-- Football Badge -->
    <g transform="translate(125, 0)">
      <rect width="117" height="28" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
      <g transform="translate(8, 4)">
        <circle cx="10" cy="10" r="6.5" fill="#ffffff" stroke="#1e293b" stroke-width="1"/>
        <polygon points="10,7.5 12.5,9.2 11.5,12 8.5,12 7.5,9.2" fill="#1e293b"/>
        <line x1="10" y1="7.5" x2="10" y2="4" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="12.5" y1="9.2" x2="15.5" y2="8" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="11.5" y1="12" x2="14" y2="14.5" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="8.5" y1="12" x2="6" y2="14.5" stroke="#1e293b" stroke-width="0.75"/>
        <line x1="7.5" y1="9.2" x2="4.5" y2="8" stroke="#1e293b" stroke-width="0.75"/>
      </g>
      <text x="32" y="18.5" class="sans" font-size="11" font-weight="600" fill="#1e293b">Football</text>
    </g>
  </g>
</g>
</svg>"""
    write_card("about-sports.svg", sports_svg)

    # 3. about-work.svg
    work_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Opportunities - Internships in Data Science and AI">
<title>Opportunities</title>
<style>{css}</style>
<rect width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="#e4e4df" stroke-width="1"/>

<g transform="translate(22, 26)">
  <!-- Tag -->
  <g class="f" style="animation-delay:0.2s">
    <circle cx="3" cy="3" r="3" fill="#059669" class="live"/>
    <text x="14" y="6" class="mono" font-size="10" letter-spacing="1" fill="#059669">03 / ACTIVE CANDIDATE</text>
  </g>

  <!-- Title -->
  <text x="0" y="36" class="serif r" style="animation-delay:0.3s" font-size="22" fill="#111111">
    Seeking Internships
  </text>

  <!-- Body -->
  <text class="sans r" style="animation-delay:0.4s" font-size="12" fill="#4a4a4e">
    <tspan x="0" y="64">Sophomore @ IIT Guwahati (DSAI).</tspan>
    <tspan x="0" y="82">Looking for Data Science, AI/ML or</tspan>
    <tspan x="0" y="100">software development roles.</tspan>
  </text>

  <!-- Action: LinkedIn Pill Button -->
  <g transform="translate(0, 126)" class="f" style="animation-delay:0.5s">
    <rect width="242" height="28" rx="14" fill="#0077b5" stroke="#0077b5" stroke-width="1"/>
    <g transform="translate(14, 6) scale(0.666)">
      <path fill="#ffffff" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
    </g>
    <text x="36" y="18.5" class="sans" font-size="11.5" font-weight="600" fill="#ffffff">Reach out on LinkedIn</text>
    <text x="220" y="18.5" class="mono" font-size="12" fill="#ffffff">&#8599;</text>
  </g>
</g>
</svg>"""
    write_card("about-work.svg", work_svg)


if __name__ == "__main__":
    print("generating all cards with Paper & Ink UI/UX...")
    build_hero()
    build_terminal()
    generate_project_cards()
    build_activity()
    generate_social_icons()
    generate_about_cards()
    print("complete.")
