#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.theme from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]

# btop color -> palette role. Gradients run low to high.
SIMPLE = {
    "main_bg": "ui.bg",
    "main_fg": "ui.fg",
    "title": "ui.fg",
    "hi_fg": "syn.constant",
    "selected_bg": "ui.bg_visual",
    "selected_fg": "ui.fg",
    "inactive_fg": "syn.comment",
    "proc_misc": "syn.special1",
    "cpu_box": "ui.nontext",
    "mem_box": "ui.nontext",
    "net_box": "ui.nontext",
    "proc_box": "ui.nontext",
    "div_line": "ui.nontext",
}
HEAT = ["diag.ok", "diag.warning", "diag.error"]
GRADIENTS = {
    "temp": HEAT,
    "cpu": HEAT,
    "free": HEAT,
    "cached": ["syn.type", "syn.fun", "syn.keyword"],
    "available": ["syn.string", "syn.identifier", "syn.constant"],
    "used": HEAT,
    "download": ["syn.type", "syn.fun", "syn.keyword"],
    "upload": ["syn.string", "syn.constant", "syn.preproc"],
}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def theme(name, r):
    out = [f"# Theme: Kanagawa {name}", "# https://github.com/kanagawa-community/btop", ""]
    out += [f'theme[{k}]="{r[v]}"' for k, v in SIMPLE.items()]
    for g, rs in GRADIENTS.items():
        out += [f'theme[{g}_{s}]="{r[x]}"' for s, x in zip(("start", "mid", "end"), rs)]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.theme"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v.capitalize(), roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
