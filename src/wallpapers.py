#!/usr/bin/env python3
"""Generate original Nordic-mountain wallpapers as SVG: aurora, twin moons, snowy peaks, a dragon."""
import random, sys

W, H = 2560, 1600

def ridge(seed, base, rough, peaks):
    """Midpoint-displacement mountain line, returned as a list of (x, y)."""
    rnd = random.Random(seed)
    pts = {0: base + rnd.uniform(-rough, rough), W: base + rnd.uniform(-rough, rough)}
    for px, py in peaks:
        pts[px] = py
    step = W
    amp = rough
    while step > 8:
        xs = sorted(pts)
        for a, b in zip(xs, xs[1:]):
            if b - a > step / 2:
                m = (a + b) // 2
                if m not in pts:
                    pts[m] = (pts[a] + pts[b]) / 2 + rnd.uniform(-amp, amp)
        step //= 2
        amp *= 0.55
    return sorted(pts.items())

def poly(pts, fill, extra=""):
    d = "M0,%d " % H + " ".join(f"L{x},{y:.1f}" for x, y in pts) + f" L{W},{H} Z"
    return f'<path d="{d}" fill="{fill}" {extra}/>'

def snowcap(pts, line, fill, seed=0):
    """Snow from the ridge top down to a jagged snow line, clipped to the mountain."""
    d = "M0,%d " % H + " ".join(f"L{x},{y:.1f}" for x, y in pts) + f" L{W},{H} Z"
    rnd = random.Random(seed + line)
    snow_line = []
    y = line
    for x in range(0, W + 24, 24):
        y = line + rnd.uniform(-70, 70) * 0.35 + (y - line) * 0.75
        snow_line.append((x, y + rnd.uniform(-6, 30) * (1.6 if rnd.random() < 0.25 else 0.6)))
    sd = "M0,0 L%d,0 " % W + " ".join(f"L{x},{y:.1f}" for x, y in reversed(snow_line)) + " Z"
    return (f'<clipPath id="cap{line}"><path d="{d}"/></clipPath>'
            f'<path d="{sd}" fill="{fill}" clip-path="url(#cap{line})"/>')

def stars(seed, n):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.6)
        r = rnd.choice([0.8, 1, 1.2, 1.6, 2.2])
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#eaf2ff" opacity="{rnd.uniform(0.3, 0.95):.2f}"/>')
    return "".join(out)

def snowfall(seed, n):
    rnd = random.Random(seed)
    return "".join(
        f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.uniform(1.5, 4.5):.1f}" '
        f'fill="#ffffff" opacity="{rnd.uniform(0.25, 0.8):.2f}"/>' for _ in range(n))

def dragon(x, y, s, color):
    # Simple original silhouette: long neck, horned head, swept wings, tail.
    return f'''<g transform="translate({x},{y}) scale({s})" fill="{color}">
  <path d="M0,0 C40,-10 80,-12 120,-4 C150,2 175,-6 200,-20 L214,-30 L206,-14 L228,-18 L204,-4
           C180,6 150,14 120,14 C80,16 40,12 0,8 C-40,4 -90,10 -140,30 C-170,42 -200,40 -220,30
           C-190,32 -160,22 -130,6 C-90,-8 -40,-6 0,0Z"/>
  <path d="M40,0 C20,-60 -30,-130 -120,-170 C-80,-130 -70,-110 -75,-90 C-110,-110 -150,-115 -190,-110
           C-150,-90 -125,-75 -115,-55 C-150,-60 -185,-50 -210,-35 C-150,-30 -80,-20 -20,4Z"/>
  <path d="M60,2 C90,-40 140,-90 210,-120 C180,-85 172,-65 176,-50 C200,-60 230,-60 260,-50
           C225,-38 205,-25 196,-10 C150,-8 100,-2 70,10Z" opacity="0.85"/>
</g>'''

def svg(variant):
    font = "Cinzel"
    if variant == "aurora":
        sky = [("0", "#050a18"), ("0.45", "#0d1d36"), ("0.8", "#243a55"), ("1", "#3b5166")]
        layers = ["#1b2a3e", "#14202f", "#0e1723", "#080e16"]
        snow = ["#b9c9dc", "#8fa3ba", "#6b7f96"]
        title, sub = "FUS · RO · DAH", "THE SKY ABOVE · THE VOICE WITHIN"
        fog = "#9fb6d0"
    else:
        sky = [("0", "#24324a"), ("0.25", "#5a6a86"), ("0.45", "#e0a878"), ("0.6", "#f6d29a"), ("1", "#f0d6a8")]
        layers = ["#5b6a80", "#46546a", "#323e50", "#1c2532"]
        snow = ["#eef2f7", "#d4dde8", "#aab8c8"]
        title, sub = "THE THROAT OF THE WORLD", "WHERE THE DRAGONS RETURN"
        fog = "#e8dccb"

    back = ridge(1, H * 0.55, 160, [(W * 0.38, H * 0.22), (W * 0.62, H * 0.33)])
    mid = ridge(2, H * 0.66, 120, [(W * 0.18, H * 0.45), (W * 0.8, H * 0.47)])
    near = ridge(3, H * 0.78, 90, [(W * 0.08, H * 0.66), (W * 0.55, H * 0.72)])
    front = ridge(4, H * 0.9, 50, [])

    aurora = ""
    if variant == "aurora":
        aurora = f'''
<g filter="url(#blur40)" opacity="0.75">
  <path d="M-100,520 C300,300 700,600 1100,380 C1500,160 1900,460 2700,260 L2700,420 C1900,620 1500,320 1100,540 C700,760 300,460 -100,680Z" fill="url(#aur1)"/>
  <path d="M-100,360 C400,200 800,420 1300,260 C1800,100 2200,300 2700,160 L2700,240 C2200,380 1800,180 1300,340 C800,500 400,280 -100,440Z" fill="url(#aur2)"/>
</g>'''
        moons = f'''
<circle cx="{W*0.78}" cy="{H*0.17}" r="120" fill="url(#masser)"/>
<circle cx="{W*0.78}" cy="{H*0.17}" r="220" fill="url(#moonglow)"/>
<circle cx="{W*0.88}" cy="{H*0.28}" r="38" fill="#e6ecf5"/>
<circle cx="{W*0.88}" cy="{H*0.28}" r="90" fill="url(#moonglow)"/>'''
        star_layer = stars(7, 420)
        drag = dragon(W * 0.3, H * 0.27, 0.9, "#05080f")
    else:
        moons = f'''<circle cx="{W*0.5}" cy="{H*0.4}" r="700" fill="url(#sunglow)"/>
<circle cx="{W*0.5}" cy="{H*0.4}" r="80" fill="#fff4dc" opacity="0.9"/>'''
        star_layer = ""
        aurora = ""
        drag = dragon(W * 0.7, H * 0.2, 1.1, "#1a2230") + dragon(W * 0.22, H * 0.33, 0.45, "#2a3446")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in sky)}</linearGradient>
  <linearGradient id="aur1" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1de9b6" stop-opacity="0"/><stop offset="0.3" stop-color="#2bffa8"/>
    <stop offset="0.7" stop-color="#3fd7ff"/><stop offset="1" stop-color="#8a6bff" stop-opacity="0.2"/></linearGradient>
  <linearGradient id="aur2" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6bffcf" stop-opacity="0.1"/><stop offset="0.5" stop-color="#7affd6"/>
    <stop offset="1" stop-color="#2bb6ff" stop-opacity="0"/></linearGradient>
  <radialGradient id="masser" cx="40%" cy="40%"><stop offset="0" stop-color="#f3d9c4"/><stop offset="1" stop-color="#b98a76"/></radialGradient>
  <radialGradient id="moonglow"><stop offset="0" stop-color="#ffffff" stop-opacity="0.25"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
  <radialGradient id="sunglow"><stop offset="0" stop-color="#fff1d0" stop-opacity="0.85"/><stop offset="1" stop-color="#fff1d0" stop-opacity="0"/></radialGradient>
  <linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{fog}" stop-opacity="0"/><stop offset="1" stop-color="{fog}" stop-opacity="0.45"/></linearGradient>
  <filter id="blur40"><feGaussianBlur stdDeviation="40"/></filter>
  <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="txt"><feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000" flood-opacity="0.7"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{star_layer}
{aurora}
{moons}
{drag}
{poly(back, layers[0])}{snowcap(back, int(H*0.40), snow[0])}
<rect y="{H*0.45}" width="{W}" height="{H*0.25}" fill="url(#fog)"/>
{poly(mid, layers[1])}{snowcap(mid, int(H*0.55), snow[1])}
<rect y="{H*0.58}" width="{W}" height="{H*0.2}" fill="url(#fog)"/>
{poly(near, layers[2])}{snowcap(near, int(H*0.71), snow[2])}
{poly(front, layers[3])}
<g filter="url(#blur6)">{snowfall(11, 60)}</g>
{snowfall(12, 140)}
<g filter="url(#txt)">
  <text x="{W/2}" y="{H*0.86}" text-anchor="middle" font-family="{font}" font-weight="700" font-size="{96 if len(title) < 16 else 70}" letter-spacing="{24 if len(title) < 16 else 14}" fill="#e9eef5">{title}</text>
  <line x1="{W/2-520}" y1="{H*0.885}" x2="{W/2+520}" y2="{H*0.885}" stroke="#c9a66b" stroke-width="2"/>
  <text x="{W/2}" y="{H*0.925}" text-anchor="middle" font-family="{font}" font-weight="400" font-size="34" letter-spacing="12" fill="#c9a66b">{sub}</text>
</g>
</svg>'''

if __name__ == "__main__":
    print(svg(sys.argv[1]))

