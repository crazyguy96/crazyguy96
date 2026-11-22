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
def build_terminal():
    w, h = 880, 150
    css = font_face() + BASE_CSS
    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="AI Meeting Assistant Pipeline Preview">
<title>AI Meeting Assistant Pipeline Preview</title>
<style>{css}</style>
<defs>
  <clipPath id="term-clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>
</defs>
<rect width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>
<line x1="0" y1="36" x2="{w}" y2="36" stroke="{BORDER}" stroke-width="1"/>

<!-- Window Controls -->
<circle cx="24" cy="18" r="4" fill="#d4d4ce"/>
<circle cx="38" cy="18" r="4" fill="#d4d4ce"/>
<circle cx="52" cy="18" r="4" fill="#d4d4ce"/>
<text x="72" y="22" font-family="{MONO}" font-size="11" fill="{MUTED}">jatin@iitg: ~/projects/ai-meeting-assistant (bash)</text>

<!-- Terminal Execution Preview -->
<g transform="translate(24, 64)" font-family="{MONO}" font-size="13">
  <!-- Command -->
  <text x="0" y="0" fill="{BLUE}" font-weight="600">$</text>
  <text x="16" y="0" fill="{INK}">python -m pipeline.transcribe --audio keynote.wav --ground-truth-check</text>

  <!-- Output 1 -->
  <text x="16" y="26" fill="{INK_SOFT}">[Faster-Whisper] Transcribed 42m audio in 8.4s · 0.00% WER</text>
  
  <!-- Output 2 -->
  <text x="16" y="50" fill="{MUTED}">Generated: 14 action items, 4 decisions · Verified against transcript context</text>
</g>
</svg>"""
    write_card("terminal.svg", content)


# ---- 3 · Project Cards (meeting, delay, vision, mazdoor) -----------------------
CARD_W = 434
CARD_H = 186


def build_project_card(filename, category, title, subhead, meta, accent_color, right_svg, delay):
    w, h = CARD_W, CARD_H
    css = font_face() + BASE_CSS
    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)} - {escape(subhead)}">
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
  <rect class="sh" style="animation-delay:{delay + 1.2:.2f}s" x="0" y="0" width="100" height="{h}" fill="url(#card-sheen)" transform="translate(-260 0)"/>
</g>
<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{BORDER}" stroke-width="1"/>

<!-- Left Content -->
<g transform="translate(24, 32)">
  <g class="f" style="animation-delay:{delay:.2f}s">
    <rect x="0" y="0" width="6" height="6" rx="1.5" fill="{accent_color}"/>
    <text x="12" y="6" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{accent_color}">{category}</text>
  </g>
  <text class="r" style="animation-delay:{delay + 0.1:.2f}s" x="0" y="36" font-family="{SANS}" font-weight="600" font-size="19" fill="{INK}" letter-spacing="-0.3">
    {title}
  </text>
  <text class="r" style="animation-delay:{delay + 0.2:.2f}s" x="0" y="62" font-family="{SANS}" font-size="13.5" fill="{INK_SOFT}">
    {subhead}
  </text>
  <text class="r" style="animation-delay:{delay + 0.3:.2f}s" x="0" y="100" font-family="{MONO}" font-size="11" fill="{MUTED}">
    {meta}
  </text>
  <text class="nu" x="228" y="100" font-family="{MONO}" font-size="12" fill="{accent_color}">&#8599;</text>
</g>

<!-- Right Schematic Visual Box -->
<g transform="translate(276, 24)">
  <rect class="f" style="animation-delay:{delay + 0.15:.2f}s" width="134" height="138" rx="10" fill="{PAPER}" stroke="{BORDER}" stroke-width="1"/>
  {right_svg}
</g>
</svg>"""
    write_card(f"{filename}.svg", content)


def generate_project_cards():
    # 1. meeting.svg
    meeting_visual = f"""
  <text class="f" style="animation-delay:0.4s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">SPEECH WAVEFORM</text>
  <path class="r" style="animation-delay:0.5s" d="M 14 44 h 10 l 4 -8 l 6 16 l 7 -22 l 7 28 l 8 -18 l 6 12 l 8 -8 h 26" 
        fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <line class="f" style="animation-delay:0.6s" x1="14" y1="68" x2="100" y2="68" stroke="#d5d5cf" stroke-width="2" stroke-linecap="round"/>
  <line class="f" style="animation-delay:0.65s" x1="14" y1="78" x2="80" y2="78" stroke="#dcdcd7" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Verified check badge -->
  <g transform="translate(14, 98)" class="f" style="animation-delay:0.75s">
    <rect width="106" height="24" rx="4" fill="#e8efff" stroke="#c7d8ff" stroke-width="1"/>
    <path d="M 10 12 l 3 3 l 6 -6" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-linecap="round"/>
    <text x="24" y="15" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{BLUE}">0% HALLUCINATION</text>
  </g>
"""
    build_project_card("meeting", "SPEECH PIPELINE", "AI Meeting Assistant",
                       "Audio to verified action items", "Faster-Whisper · Verification",
                       BLUE, meeting_visual, 0.1)

    # 2. delay.svg
    delay_visual = f"""
  <text class="f" style="animation-delay:0.45s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">SHAP ATTRIBUTION</text>
  
  <g transform="translate(14, 38)" font-family="{MONO}" font-size="8.5">
    <text x="0" y="10" fill="{INK_SOFT}">Clearance</text>
    <rect class="r" style="animation-delay:0.55s" x="50" y="3" width="52" height="8" rx="2" fill="{AMBER}"/>
    
    <text x="0" y="28" fill="{INK_SOFT}">Disputes</text>
    <rect class="r" style="animation-delay:0.65s" x="50" y="21" width="38" height="8" rx="2" fill="{AMBER}" opacity="0.8"/>
    
    <text x="0" y="46" fill="{INK_SOFT}">Buffer</text>
    <rect class="r" style="animation-delay:0.75s" x="50" y="39" width="28" height="8" rx="2" fill="#71717a"/>
    <line x1="50" y1="0" x2="50" y2="52" stroke="#d5d5cf" stroke-width="1"/>
  </g>
  
  <!-- Risk Score -->
  <g transform="translate(14, 102)" class="f" style="animation-delay:0.85s">
    <rect width="106" height="22" rx="4" fill="#fef3c7" stroke="#fde68a" stroke-width="1"/>
    <text x="12" y="15" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{AMBER}">RISK INDEX: 78.4%</text>
  </g>
"""
    build_project_card("delay", "EXPLAINABLE ML", "Land Delay Prediction",
                       "Risk scores & SHAP attribution", "LightGBM · XGBoost · SHAP",
                       AMBER, delay_visual, 0.2)

    # 3. vision.svg
    vision_visual = f"""
  <text class="f" style="animation-delay:0.5s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">ViT ATTENTION MAP</text>
  
  <!-- Astronomical Galaxy Drawing -->
  <g transform="translate(67, 65)">
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
  
  <text class="f" style="animation-delay:0.8s" x="14" y="122" font-family="{MONO}" font-size="8.5" fill="{MUTED}">DINOv2 patch tokens</text>
"""
    build_project_card("vision", "COMPUTER VISION", "Vision Transformers",
                       "DINOv2 on galaxy surveys", "PyTorch · DINOv2 · CIFAR-10",
                       VIOLET, vision_visual, 0.3)

    # 4. mazdoor.svg
    mazdoor_visual = f"""
  <text class="f" style="animation-delay:0.55s" x="14" y="22" font-family="{MONO}" font-size="9" fill="{MUTED}">WORK LOG LEDGER</text>
  
  <!-- Ledger Slip -->
  <g transform="translate(14, 34)">
    <rect width="106" height="70" rx="4" fill="{WHITE}" stroke="#dcdcd7" stroke-width="1"/>
    
    <g font-family="{MONO}" font-size="8.5">
      <text x="8" y="18" fill="{INK_SOFT}">Shift 08h</text>
      <text x="98" y="18" text-anchor="end" fill="{GREEN}">₹650</text>
      <line x1="8" y1="24" x2="98" y2="24" stroke="#ebebe6" stroke-width="0.75"/>
      
      <text x="8" y="38" fill="{INK_SOFT}">Shift 08h</text>
      <text x="98" y="38" text-anchor="end" fill="{GREEN}">₹650</text>
      <line x1="8" y1="44" x2="98" y2="44" stroke="#ebebe6" stroke-width="0.75"/>

      <text x="8" y="58" fill="{MUTED}">Verified</text>
      <text x="98" y="58" text-anchor="end" font-weight="600" fill="{INK}">₹1,300</text>
    </g>
  </g>
  <text class="f" style="animation-delay:0.85s" x="14" y="122" font-family="{MONO}" font-size="8.5" fill="{GREEN}">✓ Tamper-evident proof</text>
"""
    build_project_card("mazdoor", "CIVIC TECH", "Mazdoor Evidence Kit",
                       "Work logs & wage records", "Offline-first · LocalStorage",
                       GREEN, mazdoor_visual, 0.4)


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


if __name__ == "__main__":
    print("generating all cards with Paper & Ink UI/UX...")
    build_hero()
    build_terminal()
    generate_project_cards()
    build_activity()
    print("complete.")
