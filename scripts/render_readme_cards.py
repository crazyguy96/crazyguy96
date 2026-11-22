#!/usr/bin/env python3
"""
Render the profile README's cards as animated SVGs into cards/.

Design: Inspired by Avi Vashishta / Damir Sokolovsky ("Three Worlds": paper, ink, and vibrant accent tiles;
Instrument Serif, Geist, Geist Mono embedded as base64 WOFF).
"""
import base64
import datetime
import json
import os
import re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "cards")
FONTS = os.path.join(ROOT, "fonts")

# Brand tokens
PAPER = "#f3f3f1"
PAPER_DEEP = "#e2e2de"
INK = "#111111"
INK_SOFT = "#3a3a3c"
MUTED = "#6e6e73"
RULE = "#dcdcd7"
BLUE = "#2f55ff"
GREEN = "#059669"
GOLD = "#ffc81a"
VIOLET = "#7c3aed"
W = 880

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
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(4px)}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
.r{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .9s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.6s ease-in-out infinite}
.n{transform-box:fill-box;animation:nudge 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 1.8s ease-in-out infinite}
@keyframes tilein{0%{opacity:0;transform:translateY(90px) scale(.6) rotate(-9deg)}55%{opacity:1;transform:translateY(-10px) scale(1.05) rotate(2deg)}75%{transform:translateY(3px) scale(.98) rotate(-.8deg)}90%{transform:translateY(-1px) scale(1.01) rotate(.2deg)}100%{opacity:1;transform:none}}
@keyframes slidein{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:none}}
@keyframes arrowin{0%{opacity:0;transform:translateX(-30px)}60%{opacity:1;transform:translateX(6px)}100%{opacity:1;transform:none}}
@keyframes roll{from{transform:translateY(60px)}to{transform:none}}
@keyframes sheen{0%{transform:translateX(-260px) skewX(-20deg)}22%,100%{transform:translateX(420px) skewX(-20deg)}}
@keyframes ring{0%{opacity:.7;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
.ti{opacity:0;transform-box:fill-box;transform-origin:50% 60%;animation:tilein 1.1s cubic-bezier(.2,.8,.2,1) both}
.sl{opacity:0;transform-box:fill-box;animation:slidein .6s cubic-bezier(.2,.7,.2,1) both}
.ai{opacity:0;transform-box:fill-box;animation:arrowin .7s cubic-bezier(.2,.7,.2,1) both}
.ro{transform-box:fill-box;animation:roll .8s cubic-bezier(.15,.8,.2,1) both}
.sh{animation:sheen 5s ease-in-out infinite}
.rg{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both}
@media (prefers-reduced-motion: reduce){.r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro,.rg{animation:none!important;opacity:1!important;transform:none!important}.sh,.rg{display:none}}
"""


def font_face(keys):
    out = []
    for k in keys:
        fam, style, weight, fn = FONT_FILES[k]
        path = os.path.join(FONTS, fn)
        if os.path.exists(path):
            b64 = base64.b64encode(open(path, "rb").read()).decode()
            out.append(
                f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
            )
    return "".join(out)


BOTTOM = 12


def svg(w, h, body, fonts, label, extra_css="", left=0, right=0, bottom=BOTTOM):
    if left:
        body = f'<g transform="translate({left:.3f} 0)">{body}</g>'
    w_total, h_total = w + left + right, h + bottom
    css = font_face(fonts) + BASE_CSS + extra_css
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_total:.3f}" height="{h_total}" viewBox="0 0 {w_total:.3f} {h_total}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
        f"<style>{css}</style>{body}</svg>"
    )


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote cards/{name} ({len(content) // 1024} KB)")


def d(s):
    return f'style="animation-delay:{s:.2f}s"'


def wrap(text, n):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > n:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def text_lines(x, y, lines, lh, attrs):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" {attrs}>{escape(l)}</text>' for i, l in enumerate(lines)
    )


# ---- 1 · hero -----------------------------------------------------------------
def hero():
    h = 400
    # Right-side graphic: Signal oscilloscope & ViT Attention radar in ink lines
    graphic = """
<g transform="translate(560, 54)">
  <rect class="f" style="animation-delay:0.3s" width="270" height="290" rx="12" fill="#eaeae6" stroke="#dcdcd7" stroke-width="1"/>
  
  <!-- Waveform Screen -->
  <g transform="translate(20, 24)">
    <text class="f" style="animation-delay:0.4s" x="0" y="0" font-family="{mono}" font-size="11" fill="{muted}" letter-spacing="0.5">ACOUSTIC SIGNAL [16 kHz]</text>
    <path class="f" style="animation-delay:0.5s" d="M 0 54 L 230 54" stroke="#d5d5cf" stroke-width="1"/>
    <path class="r" style="animation-delay:0.6s" d="M 0 54 C 15 48, 25 60, 40 54 C 55 36, 65 72, 80 54 C 95 20, 105 88, 120 54 C 135 32, 145 76, 160 54 C 175 42, 185 66, 200 54 L 230 54" 
          fill="none" stroke="{blue}" stroke-width="2" stroke-linecap="round"/>
  </g>

  <!-- ViT Galaxy Radar -->
  <g transform="translate(20, 150)">
    <text class="f" style="animation-delay:0.7s" x="0" y="0" font-family="{mono}" font-size="11" fill="{muted}" letter-spacing="0.5">DINOv2 GALAXY ATTN</text>
    <g transform="translate(65, 55)">
      <circle class="f" style="animation-delay:0.8s" cx="0" cy="0" r="42" fill="none" stroke="#d5d5cf" stroke-width="1"/>
      <circle class="f" style="animation-delay:0.85s" cx="0" cy="0" r="24" fill="none" stroke="#d5d5cf" stroke-width="0.8" stroke-dasharray="2 3"/>
      <ellipse class="f" style="animation-delay:0.9s" cx="0" cy="0" rx="36" ry="16" transform="rotate(-30)" fill="none" stroke="{ink_soft}" stroke-width="1.2"/>
      <circle class="p" style="animation-delay:1.0s" cx="0" cy="0" r="3" fill="{blue}"/>
      <circle class="p" style="animation-delay:1.1s" cx="16" cy="-10" r="2" fill="{blue}"/>
      <circle class="p" style="animation-delay:1.15s" cx="-18" cy="12" r="1.8" fill="{blue}"/>
      <rect class="r" style="animation-delay:1.2s" x="-8" y="-8" width="16" height="16" fill="none" stroke="{blue}" stroke-width="1" stroke-dasharray="2 2"/>
    </g>
    <text class="f" style="animation-delay:1.3s" x="145" y="60" font-family="{mono}" font-size="10" fill="{muted}">14×14 patches</text>
    <text class="f" style="animation-delay:1.35s" x="145" y="76" font-family="{mono}" font-size="10" fill="{blue}">0% hallucination</text>
  </g>
</g>
""".format(mono=MONO, muted=MUTED, blue=BLUE, ink_soft=INK_SOFT)

    body = f"""
<defs>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>
    <stop offset=".5" stop-color="{BLUE}"/><stop offset=".58" stop-color="{INK}"/>
    <stop offset="1" stop-color="{INK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
<g class="f" {d(0)}>
  <rect class="live" x="48" y="49" width="8" height="8" rx="2" fill="{BLUE}"/>
  <text x="66" y="57" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">DATA SCIENCE &amp; AI AT IIT GUWAHATI</text>
</g>
<text class="r" {d(0.15)} x="44" y="175" font-family="{SERIF}" font-size="108" letter-spacing="-2.5" fill="{INK}">Jatin</text>
<text class="r" {d(0.30)} x="44" y="270" font-family="{SERIF}" font-style="italic" font-size="108" letter-spacing="-2.5" fill="url(#shine)">Mehra</text>
<g class="r" {d(0.55)}>
  {text_lines(48, 318, ["I work on machine learning for messy, real-world inputs:", "meeting audio, infrastructure reports, and galaxy surveys."], 25, f'font-family="{SANS}" font-size="16.5" fill="{INK_SOFT}"')}
</g>
<g class="f" {d(0.8)}>
  <text x="48" y="374" font-family="{MONO}" font-size="12.5" fill="{INK}">linkedin · leetcode · codeforces · repositories</text>
  <text class="nu" x="382" y="374" font-family="{MONO}" font-size="13" fill="{BLUE}">&#8599;</text>
</g>
{graphic}
"""
    write("hero.svg", svg(W, h, body, ["serif", "serif-i", "sans", "mono"],
                          "Jatin Mehra. Data Science & AI at IIT Guwahati. Machine learning systems for messy, real-world inputs."))


# ---- 2 · world tiles (BUILD, ALGORITHMS, RESEARCH) ---------------------------
TILE_W, TILE_H = 880 / 3 - 8, 210  # 285.33: two 12px gaps


def count_up(num, word, x, y, attrs, begin, dur=1.1, frames=18):
    m = re.match(r"([\d.]+)(.*)", num)
    if not m:
        tail = f' <tspan font-style="italic">{escape(word)}</tspan>'
        return f'<text x="{x}" y="{y}" {attrs}>{escape(num)}{tail}</text>'
    val, suf = float(m.group(1)), m.group(2)
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    tail = f' <tspan font-style="italic">{escape(word)}</tspan>'
    out = []
    for i in range(frames + 1):
        e = 1 - (1 - i / frames) ** 3
        txt = num if i == frames else f"{val * e:.{dec}f}{suf}"
        on = begin + dur * i / frames
        off = "" if i == frames else f'<set attributeName="opacity" to="0" begin="{begin + dur * (i + 1) / frames:.3f}s"/>'
        out.append(f'<text x="{x}" y="{y}" {attrs} opacity="0">{escape(txt)}{tail}'
                   f'<set attributeName="opacity" to="1" begin="{on:.3f}s"/>{off}</text>')
    return "".join(out)


def tile(name, label, color, on, num, word, blurb, delay, pos):
    lines = wrap(blurb, 34)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{150 + i * 20}" font-family="{SANS}" '
        f'font-size="13.5" fill="{on}" opacity=".92">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""
<defs>
  <clipPath id="card-{name}"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <clipPath id="slot-{name}"><rect x="0" y="62" width="{TILE_W}" height="62"/></clipPath>
  <linearGradient id="gl-{name}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card-{name})">
    <rect width="{TILE_W}" height="{TILE_H}" fill="{color}"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60" fill="none" stroke="{on}" stroke-opacity=".5" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90" height="{TILE_H + 40}" fill="url(#gl-{name})" transform="translate(-260 0)"/>
  </g>
  <text class="sl" {d(delay + 0.35)} x="24" y="38" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{on}">{label}</text>
  <g class="ai" {d(delay + 0.5)}><text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="250" y="38" font-family="{MONO}" font-size="14" fill="{on}">&#8594;</text></g>
  <g clip-path="url(#slot-{name})"><g class="ro" {d(delay + 0.45)}>
    {count_up(num, word, 22, 112, f'font-family="{SERIF}" font-size="44" fill="{on}"', delay + 0.45)}
  </g></g>
  {blurb_svg}
</g>
"""
    write(f"{name}.svg", svg(TILE_W, TILE_H, body, ["serif", "serif-i", "sans", "mono"],
                             f"{label}: {num} {word}. {blurb}", left=4 * pos, right=8 - 4 * pos))


# ---- 3 · activity (monthly bars chart) ----------------------------------------
def activity(data):
    h = 320
    monthly = data["monthly"][-12:]
    best = max(monthly[:-1] or monthly, key=lambda m: m["total"])
    top = max(best["total"], 1)
    x0, x1, base, maxh, gap = 40, 600, 268, 130, 10
    bw = (x1 - x0 - gap * (len(monthly) - 1)) / len(monthly)
    bars = []
    for i, m in enumerate(monthly):
        partial = i == len(monthly) - 1
        is_best = m is best
        bh = max(4, round(m["total"] / top * maxh))
        x = x0 + i * (bw + gap)
        fill = BLUE if is_best else ("#c9c9c4" if partial else INK)
        label = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
        bars.append(
            f'<rect class="g" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x:.1f}" y="{base - bh}" '
            f'width="{bw:.1f}" height="{bh}" rx="4" fill="{fill}"><title>{label}: {m["total"]:,}</title></rect>'
            f'<text class="f" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x + bw / 2:.1f}" y="{base + 22}" '
            f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{label}</text>'
        )
        if is_best:
            bars.append(
                f'<text class="p" style="animation-delay:3.2s" x="{x + bw / 2:.1f}" y="{base - bh - 10}" '
                f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{BLUE}">{m["total"]:,}</text>'
            )
    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    streak_note = "current streak, and the longest" if cs >= ls else f"current streak, longest {ls}"
    total_days = len(data["days"])
    stats = [
        (f'{cs} <tspan font-style="italic">days</tspan>', streak_note),
        (f'{data["active_days"]}<tspan fill="#8e8e93"> / {total_days}</tspan>', "days with a commit"),
        (f'{data["best_day"]["count"]}', "on the busiest day"),
    ]
    side = []
    for i, (big, small) in enumerate(stats):
        y = 96 + i * 82
        side.append(
            f'<g class="r" {d(2.6 + i * 0.15)}>'
            f'<text x="650" y="{y}" font-family="{SERIF}" font-size="38" fill="{INK}">{big}</text>'
            f'<text x="650" y="{y + 22}" font-family="{SANS}" font-size="13" fill="{MUTED}">{small}</text></g>'
        )
        if i < 2:
            side.append(f'<rect class="f" {d(2.6)} x="650" y="{y + 40}" width="190" height="1" fill="{RULE}"/>')
    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
<text class="f" {d(1.9)} x="40" y="52" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" {d(2.0)} x="38" y="104" font-family="{SERIF}" font-size="48" fill="{INK}">{data["total_contributions"]:,} <tspan font-style="italic">contributions</tspan></text>
{''.join(bars)}
{''.join(side)}
"""
    write("activity.svg", svg(W, h, body, ["serif", "serif-i", "sans", "mono"],
                              f'{data["total_contributions"]:,} contributions in the last year, {cs}-day streak'))


# ---- 4 · section title --------------------------------------------------------
def section_title(text, italic, theme):
    fg = "#e6edf3" if theme == "dark" else INK
    body = (
        f'<text class="r" {d(3.8)} x="2" y="44" font-family="{SERIF}" font-size="34" fill="{fg}">{escape(text)} '
        f'<tspan font-style="italic">{escape(italic)}</tspan></text>'
    )
    write(f"title-projects-{theme}.svg", svg(W, 58, body, ["serif", "serif-i"], f"{text} {italic}", bottom=0))


# ---- 5 · repo cards (2 per row: width 434, height 176) -----------------------
PAIR_W = 434
PAIR_H = 176

REPOS = [
    ("meeting-assistant", "AI Meeting Assistant",
     "Turns audio into transcripts, minutes, decisions, and action items with evidence-grounding.",
     "Python · Faster-Whisper · Gradio", BLUE),
    ("delay-prediction", "Land Delay Risk Prediction",
     "SIH PS 26017 project classifying infrastructure delay risk with TreeSHAP diagnostics.",
     "Python · LightGBM · SHAP", "#ea580c"),
    ("vision-vit", "Self-Supervised Vision ViT",
     "Probing DINOv2 self-attention maps across DESI Legacy Survey galaxy imagery.",
     "PyTorch · DINOv2 · CIFAR-10", VIOLET),
    ("mazdoor-evidence", "Mazdoor Evidence Kit",
     "Offline-first mobile workflow for daily-wage workers to maintain tamper-evident logs.",
     "HTML · LocalStorage · Civic Tech", GREEN),
]


def repo_card(i, key, name, desc, meta, color):
    delay = 4.0 + i * 0.12
    lines = wrap(desc, 44)
    desc_svg = "".join(
        f'<text x="24" y="{74 + idx * 21}" font-family="{SANS}" font-size="13.5" fill="{INK_SOFT}">{escape(l)}</text>'
        for idx, l in enumerate(lines)
    )
    body = f"""
<rect width="{PAIR_W}" height="{PAIR_H}" rx="14" fill="{PAPER}"/>
<g class="r" {d(delay)}>
  <rect x="24" y="28" width="8" height="8" rx="2" fill="{color}"/>
  <text x="40" y="37" font-family="{SANS}" font-weight="600" font-size="17" fill="{INK}">{escape(name)}</text>
  {desc_svg}
  <text x="24" y="{PAIR_H - 22}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{escape(meta)}</text>
  <text class="nu" x="{PAIR_W - 32}" y="{PAIR_H - 22}" font-family="{MONO}" font-size="12" fill="{color}">&#8599;</text>
</g>
"""
    write(f"repo-{key}.svg", svg(PAIR_W, PAIR_H, body, ["sans", "sans-b", "mono"], f"{name}: {desc}"))


def main():
    print("rendering profile cards...")
    hero()
    tile("build", "BUILD · SYSTEMS", BLUE, "#ffffff", "4", "systems",
         "Speech transcription, delay risk prediction, galaxy vision, and daily wage records.", 0.9, 0)
    tile("algo", "DSA · PROBLEM SOLVING", GREEN, "#ffffff", "LC", "& CF",
         "Algorithmic problem decomposition, clean data structures, and efficient C++ execution.", 1.1, 1)
    tile("research", "RESEARCH · IITG", GOLD, "#111111", "B.Tech", "'25–'29",
         "Self-supervised vision representations on DESI surveys and Bayesian survival statistics.", 1.3, 2)

    with open(DATA) as f:
        data = json.load(f)
    activity(data)

    section_title("Featured Systems &", "Pipelines", "dark")
    section_title("Featured Systems &", "Pipelines", "light")

    for i, (key, name, desc, meta, color) in enumerate(REPOS):
        repo_card(i, key, name, desc, meta, color)

    print("all cards generated successfully.")


if __name__ == "__main__":
    main()
