#!/usr/bin/env python3
"""
Generate 4 preview sets of REAL profile SVG cards with different color palettes:
Combining Greige/Beige, Grey, Black, Dark Pink, and Yellow.
All fonts (Instrument Serif, Geist, Geist Mono) and layouts remain 100% IDENTICAL.
macOS Terminal card remains untouched.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

import generate_cards as gc

PREVIEW_BASE = os.path.expanduser("~/.gemini/antigravity/brain/e783699c-ef1e-42bc-9a95-a5a1f8b56063/palette_previews")

PALETTES = [
    {
        "id": "option_1_studio_greige",
        "name": "Option 1: Studio Greige (Light Stone Paper)",
        "desc": "Warm oatmeal greige (#ece7de) base, carbon black text (#141414), dark rose (#be123c) & saffron yellow (#ca8a04) accents.",
        "badge": "Editorial Stone",
        "bg_type": "light",
        "tokens": {
            "WHITE": "#ece7de",
            "PAPER": "#e2ddd4",
            "BORDER": "#d6d0c4",
            "BORDER_SOFT": "#ded8cd",
            "INK": "#141414",
            "INK_SOFT": "#3f3d39",
            "MUTED": "#706b62",
            "BLUE": "#be123c",    # Hero accent & Languages -> Dark Rose
            "AMBER": "#ca8a04",   # ML & Meeting -> Warm Saffron Yellow
            "VIOLET": "#be123c",  # Vision -> Dark Rose
            "GREEN": "#141414",   # Tools -> Pitch Carbon Black
        }
    },
    {
        "id": "option_2_dark_greige",
        "name": "Option 2: Dark Charcoal Greige (Warm Dark Mode)",
        "desc": "Deep warm charcoal-greige (#1e1d1b) base, warm sand beige text (#f0ebe1), vivid dark rose (#fb7185) & electric canary (#facc15).",
        "badge": "Warm Synthwave Dark",
        "bg_type": "dark",
        "tokens": {
            "WHITE": "#1e1d1b",
            "PAPER": "#282623",
            "BORDER": "#383530",
            "BORDER_SOFT": "#2e2b26",
            "INK": "#f0ebe1",
            "INK_SOFT": "#c4bcad",
            "MUTED": "#8a8376",
            "BLUE": "#fb7185",    # Dark Rose
            "AMBER": "#facc15",   # Electric Canary Yellow
            "VIOLET": "#fb7185",  # Dark Rose
            "GREEN": "#facc15",   # Canary Yellow
        }
    },
    {
        "id": "option_3_bauhaus_linen",
        "name": "Option 3: Bauhaus Sand Linen (Warm Sandstone)",
        "desc": "Sandstone linen (#f4efe6) base, deep carbon (#111111) text, bold dark rose (#e11d48) & bauhaus canary (#eab308).",
        "badge": "Bauhaus Sandstone",
        "bg_type": "light",
        "tokens": {
            "WHITE": "#f4efe6",
            "PAPER": "#e8e2d7",
            "BORDER": "#dad3c5",
            "BORDER_SOFT": "#e2dcd0",
            "INK": "#111111",
            "INK_SOFT": "#45423d",
            "MUTED": "#757169",
            "BLUE": "#e11d48",    # Bold Dark Rose
            "AMBER": "#eab308",   # Bauhaus Canary Yellow
            "VIOLET": "#e11d48",  # Bold Dark Rose
            "GREEN": "#111111",   # Deep Carbon
        }
    },
    {
        "id": "option_4_titanium_concrete",
        "name": "Option 4: Titanium Concrete Greige (Industrial Muted)",
        "desc": "Cool-warm concrete greige (#e5e2da), graphite ink (#18181b), magenta noir (#c026d3) & tuscan gold (#ca8a04).",
        "badge": "Modern Titanium",
        "bg_type": "light",
        "tokens": {
            "WHITE": "#e5e2da",
            "PAPER": "#d9d5cc",
            "BORDER": "#cbc6bb",
            "BORDER_SOFT": "#d3cec4",
            "INK": "#18181b",
            "INK_SOFT": "#3f3f46",
            "MUTED": "#71717a",
            "BLUE": "#c026d3",    # Magenta Dark Pink
            "AMBER": "#ca8a04",   # Tuscan Gold
            "VIOLET": "#c026d3",  # Magenta Dark Pink
            "GREEN": "#18181b",   # Graphite
        }
    }
]

def main():
    os.makedirs(PREVIEW_BASE, exist_ok=True)
    
    # Original untouched terminal card
    terminal_src = os.path.join(ROOT, "cards", "terminal.svg")
    
    for p in PALETTES:
        out_dir = os.path.join(PREVIEW_BASE, p["id"])
        os.makedirs(out_dir, exist_ok=True)
        gc.OUT_DIR = out_dir
        
        # Apply tokens to generate_cards module
        for k, v in p["tokens"].items():
            setattr(gc, k, v)
            
        print(f"\nGenerating real SVGs for {p['name']} in {out_dir}...")
        gc.build_hero()
        # Copy untouched terminal
        shutil.copy(terminal_src, os.path.join(out_dir, "terminal.svg"))
        gc.generate_project_cards()
        gc.generate_about_cards()
        gc.generate_skills_cards()
        gc.build_activity()
        gc.generate_social_icons()

    print("\nAll 4 palette SVG sets successfully generated.")

if __name__ == "__main__":
    main()
