#!/usr/bin/env python3
"""Generate the meta-ability radar SVG (assets/meta-abilities.svg).

Edit the values in AXES and re-run to refresh the chart:

    python3 assets/generate_radar.py
"""
import math

W, H = 780, 512
CX, CY, R = 390, 280, 156
BG, CARD_BORDER = "#0d1117", "#30363d"
GRID, MUTED, TEXT, BLUE, PURPLE = "#263041", "#484f58", "#e6edf3", "#58a6ff", "#bc8cff"
FONT = "SF Pro Display, Segoe UI, Helvetica Neue, Arial, PingFang SC, sans-serif"
RINGS = (20, 40, 60, 80, 100)

# (label, value 0-100) — clockwise from the top
AXES = [
    ("AI &amp; Tools", 40),   # AI 与数字工具
    ("Finance",        30),   # 赚钱与资产管理
    ("Rule",           20),   # 法律、规则与维权
    ("Expression",     40),   # 沟通写作、销售与谈判
    ("Health",         30),   # 健康管理与应急
]


def axis_point(i, v):
    a = math.radians(-90 + i * 72)
    r = R * v / 100.0
    return CX + r * math.cos(a), CY + r * math.sin(a)


def ring_path(v):
    pts = [axis_point(i, v) for i in range(5)]
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{coords}" fill="none" stroke="{GRID}" stroke-width="1"/>'


p = []

# card + defs
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
p.append(f'''<defs>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0.28"/>
  <stop offset="1" stop-color="{PURPLE}" stop-opacity="0.10"/>
</linearGradient>
<linearGradient id="gs" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{BLUE}"/>
  <stop offset="1" stop-color="{PURPLE}"/>
</linearGradient>
</defs>''')
p.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{CARD_BORDER}" stroke-width="1"/>')

# title
p.append(f'<text x="{CX}" y="44" text-anchor="middle" font-size="13" letter-spacing="4" fill="{MUTED}">META-ABILITY RADAR</text>')
p.append(f'<text x="{CX}" y="72" text-anchor="middle" font-size="21" font-weight="700" fill="{TEXT}">Current Levels</text>')

# rings + axis lines + ring scale numbers
for v in RINGS:
    p.append(ring_path(v))
for i in range(5):
    x, y = axis_point(i, 100)
    p.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
for v in RINGS:
    y = CY - R * v / 100.0
    p.append(f'<text x="{CX + 8}" y="{y + 4:.1f}" font-size="9.5" fill="{MUTED}">{v}</text>')

# data polygon
coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in (axis_point(i, v) for i, (_, v) in enumerate(AXES)))
p.append(f'<polygon points="{coords}" fill="url(#gl)" stroke="url(#gs)" stroke-width="2.5" stroke-linejoin="round"/>')
for i, (_, v) in enumerate(AXES):
    x, y = axis_point(i, v)
    p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{BG}" stroke="{BLUE}" stroke-width="2.2"/>')

# axis labels
for i, (label, v) in enumerate(AXES):
    x, y = axis_point(i, 100)
    c, s = math.cos(math.radians(-90 + i * 72)), math.sin(math.radians(-90 + i * 72))
    if s < -0.7:            # top
        lx, anchor, ny, vy = x, "middle", y - 26, y - 10
    elif s > 0.7:           # bottom
        lx, anchor, ny, vy = x, "middle", y + 30, y + 46
    elif c > 0:             # right side
        lx, anchor, ny, vy = x + 14, "start", y - 2, y + 15
    else:                   # left side
        lx, anchor, ny, vy = x - 14, "end", y - 2, y + 15
    p.append(f'<text x="{lx:.1f}" y="{ny:.1f}" text-anchor="{anchor}" font-size="16" font-weight="600" fill="{TEXT}">{label}</text>')
    p.append(f'<text x="{lx:.1f}" y="{vy:.1f}" text-anchor="{anchor}" font-size="13" font-weight="700" fill="{BLUE}">{v}%</text>')

p.append(f'<text x="{CX}" y="{H - 20}" text-anchor="middle" font-size="11" fill="{MUTED}">honest self-assessment · Oct 2026 · scale 0–100</text>')
p.append('</svg>')

out = "\n".join(p) + "\n"
with open("meta-abilities.svg", "w", encoding="utf-8") as f:
    f.write(out)
print("written:", out[:80], "...")
