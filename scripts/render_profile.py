#!/usr/bin/env python3
"""Render the profile SVGs from profile/profile.toml.

- assets/terminal.svg: an animated terminal running `kubectl describe engineer`
- assets/trace.svg: an animated OpenTelemetry-style trace, idea to production

The `--now` line comes from the AI-SUMMARY block in profile/now.md, which
scripts/update_readme.py rewrites every week. Standard library only.
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

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
FS = 15  # font size
CW = FS * 0.6  # approximate monospace char width
LH = 24  # line height
WIDTH = 880

BG = "#0d1117"
FG = "#e6edf3"
DIM = "#8b949e"
GREEN = "#3fb950"
BLUE = "#79c0ff"
PURPLE = "#d2a8ff"
ORANGE = "#ffa657"


def read_now():
    match = re.search(
        r"<!-- AI-SUMMARY:START -->\n(.*?)\n<!-- AI-SUMMARY:END -->",
        NOW.read_text(),
        re.DOTALL,
    )
    text = match.group(1) if match else ""
    return re.sub(r"[*_`]", "", " ".join(text.split()))


def span(text, color=FG, bold=False):
    weight = ' font-weight="700"' if bold else ""
    return f'<tspan fill="{color}"{weight}>{escape(text)}</tspan>'


def terminal(p):
    # Each entry: (kind, list of (text, color, bold)). "cmd" lines are typed out.
    lines = []

    def cmd(text):
        lines.append(("cmd", [("$ ", GREEN, True), (text, FG, False)]))

    def out(*parts):
        lines.append(("out", list(parts)))

    def kv(key, value, color=FG):
        out(("  " + f"{key}:".ljust(10), BLUE, False), (value, color, False))

    cmd(f"kubectl describe engineer {p['handle']}")
    kv("Name", p["name"], FG)
    kv("Role", p["role"], FG)
    kv("Focus", p["focus"], FG)
    out(("  " + "Status:".ljust(10), BLUE, False), ("● Running", GREEN, True), (f"  {p['status']}", DIM, False))
    out(("", FG, False))
    cmd("kubectl get skills")
    out(("  " + "NAME".ljust(14) + "STACK", DIM, False))
    for name, stack in p["skills"].items():
        out(("  " + name.ljust(14), PURPLE, False), (stack, FG, False))
    if p.get("wins"):
        out(("", FG, False))
        cmd("cat wins.log")
        for win in p["wins"]:
            out(("  ✔ ", GREEN, True), (win, FG, False))
    now = read_now()
    if now:
        out(("", FG, False))
        cmd(f"{p['handle']} --now")
        for chunk in textwrap.wrap(now, 86):
            out(("  " + chunk, ORANGE, False))
    lines.append(("cursor", []))

    top = 64
    height = top + LH * (len(lines) - 1) + 22
    body = []
    t = 0.4  # animation clock, seconds
    for i, (kind, parts) in enumerate(lines):
        y = top + i * LH
        if kind == "cursor":
            body.append(
                f'<text x="24" y="{y}" class="ln" style="animation-delay:{t:.2f}s">{span("$ ", GREEN, True)}</text>'
                f'<rect x="{24 + 2 * CW:.1f}" y="{y - FS + 2}" width="{CW:.1f}" height="{FS + 2}" fill="{FG}" class="cur" style="animation-delay:{t:.2f}s"/>'
            )
            continue
        content = "".join(span(*part) for part in parts)
        if kind == "cmd":
            chars = sum(len(part[0]) for part in parts)
            dur = max(0.5, chars * 0.035)
            width = chars * CW + 10
            body.append(
                f'<text x="24" y="{y}">{content}</text>'
                f'<rect x="22" y="{y - FS - 2}" width="{width:.0f}" height="{LH}" fill="{BG}" '
                f'style="animation:type {dur:.2f}s steps({chars}) {t:.2f}s both;--w:{width:.0f}px"/>'
            )
            t += dur + 0.25
        else:
            body.append(f'<text x="24" y="{y}" class="ln" style="animation-delay:{t:.2f}s">{content}</text>')
            t += 0.12

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{escape(p['name'])}: {escape(p['role'])}">
<style>
  text {{ font-family: {FONT}; font-size: {FS}px; white-space: pre; }}
  .ln {{ opacity: 0; animation: show .01s forwards; }}
  .cur {{ opacity: 0; animation: blink 1s step-end infinite; }}
  @keyframes show {{ to {{ opacity: 1; }} }}
  @keyframes type {{ to {{ transform: translateX(var(--w)); }} }}
  @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
</style>
<rect width="{WIDTH}" height="{height}" rx="12" fill="{BG}" stroke="#30363d"/>
<circle cx="24" cy="22" r="6" fill="#ff5f57"/><circle cx="44" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>
<text x="{WIDTH / 2}" y="27" text-anchor="middle" fill="{DIM}" style="font-size:13px">{escape(p['handle'])}@prod: ~</text>
<line x1="0" y1="40" x2="{WIDTH}" y2="40" stroke="#21262d"/>
{chr(10).join(body)}
</svg>
"""


def trace(p):
    spans = p["trace"]
    left, label_w, right = 24, 300, 24
    track_x = left + label_w
    track_w = WIDTH - track_x - right
    row_h = 34
    top = 78
    height = top + row_h * len(spans) + 30
    colors = [BLUE, PURPLE, PURPLE, GREEN, ORANGE, "#56d4dd", GREEN, "#ff7b72"]

    rows = []
    for i, (name, detail, start, end) in enumerate(spans):
        y = top + i * row_h
        x = track_x + track_w * start / 100
        w = max(4, track_w * (end - start) / 100)
        delay = 0.3 + 0.35 * i
        color = colors[i % len(colors)]
        indent = 0 if i == 0 else 14
        rows.append(
            f'<g class="row" style="animation-delay:{delay:.2f}s">'
            f'<text x="{left + indent}" y="{y + 5}" fill="{FG}">{escape(name)}</text>'
            f'<text x="{left + indent}" y="{y + 21}" fill="{DIM}" style="font-size:12px">{escape(detail)}</text>'
            f'<rect x="{x:.1f}" y="{y - 6}" width="{w:.1f}" height="16" rx="4" fill="{color}" class="bar" style="animation-delay:{delay:.2f}s"/>'
            "</g>"
        )
    ticks = "".join(
        f'<line x1="{track_x + track_w * k / 4:.1f}" y1="{top - 22}" x2="{track_x + track_w * k / 4:.1f}" y2="{height - 42}" stroke="#21262d"/>'
        for k in range(5)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="How I ship: a trace from idea to production">
<style>
  text {{ font-family: {FONT}; font-size: 14px; }}
  .row {{ opacity: 0; animation: show .4s ease-out forwards; }}
  .bar {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow .7s cubic-bezier(.2,.8,.2,1) forwards; }}
  .pulse {{ animation: pulse 1.6s ease-in-out infinite; }}
  @keyframes show {{ to {{ opacity: 1; }} }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
</style>
<rect width="{WIDTH}" height="{height}" rx="12" fill="{BG}" stroke="#30363d"/>
<text x="{left}" y="34" fill="{FG}" font-weight="700" style="font-size:15px">trace · idea → production</text>
<text x="{WIDTH - right}" y="34" text-anchor="end" fill="{DIM}" style="font-size:13px">service <tspan fill="{FG}">{escape(p['handle'])}-platform</tspan>   status <tspan fill="{GREEN}" class="pulse">● OK</tspan></text>
{ticks}
{chr(10).join(rows)}
<text x="{left}" y="{height - 16}" fill="{DIM}" style="font-size:12px">every span instrumented with OpenTelemetry · every deploy GitOps · every incident summarised by AI</text>
</svg>
"""


def main():
    profile = tomllib.loads(PROFILE.read_text())
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "terminal.svg").write_text(terminal(profile))
    (ASSETS / "trace.svg").write_text(trace(profile))


if __name__ == "__main__":
    main()
