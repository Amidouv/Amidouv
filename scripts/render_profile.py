#!/usr/bin/env python3
"""Render the profile SVGs from profile/profile.toml.

- assets/hero.svg:   name, role, tagline, a live heartbeat line, and the
                     AI-written "now building" line from profile/now.md
- assets/win-N.svg:  one animated architecture card per win
- assets/skills.svg: skills in four rows plus how I work

Animations are CSS and SMIL only, so they play inside GitHub's <img> sandbox.
Standard library only.
"""

import re
import textwrap
import tomllib
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "profile" / "profile.toml"
NOW = ROOT / "profile" / "now.md"
ASSETS = ROOT / "assets"

W = 880
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
BG = "#0d1117"
BORDER = "#30363d"
FG = "#e6edf3"
DIM = "#8b949e"
GREEN = "#3fb950"


def read_now():
    match = re.search(
        r"<!-- AI-SUMMARY:START -->\n(.*?)\n<!-- AI-SUMMARY:END -->",
        NOW.read_text(),
        re.DOTALL,
    )
    text = match.group(1) if match else ""
    return re.sub(r"[*_`]", "", " ".join(text.split()))


def frame(height, body, label, style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(label)}">
<style>
  text {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .fade {{ opacity: 0; animation: fade .6s ease-out forwards; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
{style}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{height - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
{body}
</svg>
"""


def hero(p):
    height = 256
    # A heartbeat line: flat, then a QRS spike, repeated across the card.
    beat = "l 40 0 l 8 -6 l 6 6 l 10 0 l 6 -34 l 8 58 l 6 -24 l 10 0 l 10 -8 l 10 8 "
    pulse = "M 520 104 " + beat + "l 40 0 " + beat
    now = read_now()
    now_lines = textwrap.wrap(now, 96)[:2]
    now_svg = "".join(
        f'<text x="64" y="{215 + i * 20}" fill="{FG}" class="mono" style="font-size:13px">{escape(line)}</text>'
        for i, line in enumerate(now_lines)
    )
    body = f"""
<defs>
  <linearGradient id="role" x1="0" x2="1"><stop offset="0" stop-color="#79c0ff"/><stop offset=".5" stop-color="#a371f7"/><stop offset="1" stop-color="#3fb950"/></linearGradient>
  <linearGradient id="fadeR" gradientUnits="userSpaceOnUse" x1="520" x2="{W - 30}"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".9"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
</defs>
<path d="{pulse}" fill="none" stroke="url(#fadeR)" stroke-width="2" stroke-linejoin="round" class="ekg" opacity=".9"/>
<text x="40" y="66" fill="{FG}" font-weight="800" style="font-size:44px;letter-spacing:-1px" class="fade">{escape(p['name'])}</text>
<text x="40" y="104" fill="url(#role)" font-weight="700" style="font-size:24px;animation-delay:.25s" class="fade">{escape(p['role'])}</text>
<text x="40" y="136" fill="{DIM}" style="font-size:16px;animation-delay:.5s" class="fade">{escape(p['tagline'])}</text>
<g class="fade" style="animation-delay:.9s">
  <line x1="40" y1="166" x2="{W - 40}" y2="166" stroke="#21262d"/>
  <circle cx="48" cy="210" r="5" fill="{GREEN}" class="blink"/>
  <text x="64" y="192" fill="{DIM}" class="mono" style="font-size:11px;letter-spacing:1px">NOW BUILDING  ·  WRITTEN WEEKLY BY AI ON AMAZON BEDROCK</text>
  {now_svg}
</g>"""
    style = """  .ekg { stroke-dasharray: 700; stroke-dashoffset: 700; animation: draw 4s linear infinite; }
  .blink { animation: blink 1.4s ease-in-out infinite; }
  @keyframes draw { to { stroke-dashoffset: 0; } }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: .2; } }"""
    return frame(height, body, f"{p['name']}, {p['role']}. {p['tagline']} Now building: {now}", style)


def node_box(label):
    w = len(label) * 7.4 + 32
    return w, 30


def edge_path(a, b):
    ax, ay, aw = a["x"], a["y"], a["w"]
    bx, by, bw = b["x"], b["y"], b["w"]
    if abs(ax - bx) < 40:  # vertical
        if by > ay:
            sx, sy, ex, ey = ax, ay + 15, bx, by - 15
        else:
            sx, sy, ex, ey = ax, ay - 15, bx, by + 15
        my = (sy + ey) / 2
        return f"M {sx:.1f} {sy:.1f} C {sx:.1f} {my:.1f} {ex:.1f} {my:.1f} {ex:.1f} {ey:.1f}"
    sx, sy = ax + aw / 2, ay
    ex, ey = bx - bw / 2, by
    mx = (sx + ex) / 2
    return f"M {sx:.1f} {sy:.1f} C {mx:.1f} {sy:.1f} {mx:.1f} {ey:.1f} {ex:.1f} {ey:.1f}"


def win_card(index, win):
    height = 320
    accent = win["accent"]
    nodes = {}
    for nid, label, x, y, color in win["nodes"]:
        w, h = node_box(label)
        nodes[nid] = {"label": label, "x": x, "y": y, "w": w, "h": h, "color": color}

    edges_svg, dots_svg = [], []
    for i, (a, b) in enumerate(win["edges"]):
        d = edge_path(nodes[a], nodes[b])
        delay = 0.6 + 0.15 * i
        edges_svg.append(
            f'<path id="e{index}_{i}" d="{d}" fill="none" stroke="{accent}" stroke-opacity=".35" stroke-width="1.5"/>'
            f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="1.5" class="flow" style="animation-delay:{delay:.2f}s"/>'
        )
        dots_svg.append(
            f'<circle r="3.5" fill="{accent}"><animateMotion dur="2.4s" begin="{delay:.2f}s" repeatCount="indefinite" '
            f'keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#e{index}_{i}"/></animateMotion></circle>'
        )

    nodes_svg = []
    for i, n in enumerate(nodes.values()):
        x, y, w, h = n["x"] - n["w"] / 2, n["y"] - n["h"] / 2, n["w"], n["h"]
        nodes_svg.append(
            f'<g class="fade" style="animation-delay:{0.2 + 0.08 * i:.2f}s">'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="8" fill="#161b22" stroke="{n["color"]}" stroke-opacity=".8"/>'
            f'<circle cx="{x + 12:.1f}" cy="{n["y"]}" r="3" fill="{n["color"]}"/>'
            f'<text x="{x + 22:.1f}" y="{n["y"] + 4.5:.1f}" fill="{FG}" style="font-size:12.5px">{escape(n["label"])}</text>'
            "</g>"
        )

    body = f"""
<rect x="0" y="0" width="5" height="{height}" rx="2" fill="{accent}"/>
<text x="36" y="46" fill="{accent}" class="mono" font-weight="700" style="font-size:14px">{index:02d}</text>
<text x="70" y="47" fill="{FG}" font-weight="700" style="font-size:22px">{escape(win['title'])}</text>
<text x="36" y="76" fill="{accent}" font-weight="600" style="font-size:14.5px">{escape(win['impact'])}</text>
<text x="36" y="98" fill="{DIM}" style="font-size:13px">{escape(win['context'])}</text>
{''.join(edges_svg)}
{''.join(dots_svg)}
{''.join(nodes_svg)}
<text x="36" y="{height - 20}" fill="{DIM}" class="mono" style="font-size:11.5px">{escape(win['tags'])}</text>"""
    style = """  .flow { stroke-dasharray: 600; stroke-dashoffset: 600; animation: flow 1.2s ease-out forwards; }
  @keyframes flow { to { stroke-dashoffset: 0; } }"""
    return frame(height, body, f"Win {index}: {win['title']}. {win['impact']}. {win['tags']}", style)


def skills(p):
    rows = p["skills"]
    top, row_h = 62, 40
    height = top + row_h * len(rows) + 54
    colors = ["#a371f7", "#3fb950", "#ff9900", "#79c0ff"]
    lines = []
    for i, (area, items) in enumerate(rows):
        y = top + i * row_h + 18
        c = colors[i % len(colors)]
        lines.append(
            f'<g class="fade" style="animation-delay:{0.15 * i:.2f}s">'
            f'<circle cx="44" cy="{y - 5}" r="4" fill="{c}"/>'
            f'<text x="60" y="{y}" fill="{FG}" font-weight="700" style="font-size:15px">{escape(area)}</text>'
            f'<text x="210" y="{y}" fill="{DIM}" style="font-size:14px">{escape(items)}</text></g>'
        )
    body = f"""
<text x="36" y="40" fill="{FG}" font-weight="700" style="font-size:18px">Toolbox</text>
{''.join(lines)}
<line x1="36" y1="{height - 46}" x2="{W - 36}" y2="{height - 46}" stroke="#21262d"/>
<text x="36" y="{height - 20}" fill="{FG}" style="font-size:14px"><tspan fill="{DIM}">How I work  </tspan>{escape(p['how_i_work'])}</text>"""
    return frame(height, body, "Toolbox: " + "; ".join(f"{a}: {s}" for a, s in rows))


def main():
    profile = tomllib.loads(PROFILE.read_text())
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    (ASSETS / "hero.svg").write_text(hero(profile))
    for i, win in enumerate(profile["wins"], 1):
        (ASSETS / f"win-{i}.svg").write_text(win_card(i, win))
    (ASSETS / "skills.svg").write_text(skills(profile))


if __name__ == "__main__":
    main()
