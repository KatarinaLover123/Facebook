import random, math, sys
out = sys.argv[1]
W, H, R = 74.4, 150.0, 12.0          # case back, mm
BLEED = 3.0
CAM = (4.2, 4.2, 39.0, 39.0, 9.5)    # camera cutout x,y,w,h,r
BG, PANEL, BULL, BEAR, AMBER, TEXT, DIM = "#080810","#0A0A11","#44BBA8","#F5505F","#F5AC6F","#F2F4F9","#565B6B"
FONTS = "@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap');"

def candles():
    random.seed(7)
    n, x0, x1, top, bot = 22, 5.0, 69.4, 98.0, 136.0
    # price path: drift down into equal lows, sweep below, then reclaim and rally
    p, path = 50.0, []
    script = [-1,-2,1,-2,-1,1,-2,0,1,-1,0,-6,5,3,2,-1,3,2,-1,3,2,3]
    for s in script:
        o = p; c = p + s*1.6 + random.uniform(-.4,.4)
        hi = max(o,c)+random.uniform(.5,1.8); lo = min(o,c)-random.uniform(.5,1.8)
        path.append((o,hi,lo,c)); p = c
    lows = [b[2] for b in path]; highs=[b[1] for b in path]
    mn, mx = min(lows), max(highs)
    Y = lambda v: bot - (v-mn)/(mx-mn)*(bot-top)
    step = (x1-x0)/n; bw = step*0.56
    g = []
    eq = Y(min(lows[:11]))  # equal-lows pool before the sweep bar
    g.append(f'<line x1="{x0}" y1="{eq:.2f}" x2="{x0+step*12}" y2="{eq:.2f}" stroke="{AMBER}" stroke-width=".35" stroke-dasharray="1.2 .9"/>')
    g.append(f'<text x="{x0}" y="{eq+3.0:.2f}" font-family="IBM Plex Mono" font-weight="500" font-size="1.9" letter-spacing=".35" fill="{AMBER}">SELL-SIDE LIQUIDITY</text>')
    for i,(o,hi,lo,c) in enumerate(path):
        cx = x0 + step*(i+.5); col = BULL if c>=o else BEAR
        g.append(f'<line x1="{cx:.2f}" y1="{Y(hi):.2f}" x2="{cx:.2f}" y2="{Y(lo):.2f}" stroke="{col}" stroke-width=".32"/>')
        yt, yb = Y(max(o,c)), Y(min(o,c))
        g.append(f'<rect x="{cx-bw/2:.2f}" y="{yt:.2f}" width="{bw:.2f}" height="{max(yb-yt,.4):.2f}" fill="{col}"/>')
    sx = x0 + step*11.5; sy = Y(path[11][2])
    g.append(f'<rect x="{sx-step*.55:.2f}" y="{Y(path[11][1])-1.2:.2f}" width="{step*1.1:.2f}" height="{sy-Y(path[11][1])+2.4:.2f}" rx=".6" fill="none" stroke="{AMBER}" stroke-width=".3" opacity=".9"/>')
    g.append(f'<text x="{sx+step*.8:.2f}" y="{sy+2.2:.2f}" font-family="IBM Plex Mono" font-weight="500" font-size="1.9" letter-spacing=".35" fill="{AMBER}">SWEPT</text>')
    return "\n".join(g)

def logo(cx, cy, s):
    # droplet (liquidity) holding three candles (lab / market structure)
    d = (f"M {cx} {cy-11*s} C {cx+3*s} {cy-6.5*s} {cx+8.5*s} {cy-1.5*s} {cx+8.5*s} {cy+3.5*s} "
         f"A {8.5*s} {8.5*s} 0 0 1 {cx-8.5*s} {cy+3.5*s} C {cx-8.5*s} {cy-1.5*s} {cx-3*s} {cy-6.5*s} {cx} {cy-11*s} Z")
    c = [(-3.6,2.0,6.2,BULL,-0.5,8.6),(0,-1.2,4.4,BEAR,-2.6,5.6),(3.6,-3.6,9.4,BULL,-5.2,7.4)]
    parts = [f'<path d="{d}" fill="none" stroke="{TEXT}" stroke-width="{.75*s}" stroke-linejoin="round"/>']
    for dx, top, h, col, wt, wb in c:
        x = cx+dx*s
        parts.append(f'<line x1="{x}" y1="{cy+wt*s}" x2="{x}" y2="{cy+wb*s}" stroke="{col}" stroke-width="{.45*s}"/>')
        parts.append(f'<rect x="{x-1.1*s}" y="{cy+top*s}" width="{2.2*s}" height="{h*s*.62}" rx="{.25*s}" fill="{col}"/>')
    return "\n".join(parts)

def art():
    g = [f'<rect x="{-BLEED}" y="{-BLEED}" width="{W+2*BLEED}" height="{H+2*BLEED}" fill="{BG}"/>']
    for x in range(0, 80, 6): g.append(f'<line x1="{x}" y1="-3" x2="{x}" y2="153" stroke="#fff" stroke-opacity=".05" stroke-width=".15"/>')
    for y in range(0, 156, 6): g.append(f'<line x1="-3" y1="{y}" x2="78" y2="{y}" stroke="#fff" stroke-opacity=".05" stroke-width=".15"/>')
    g.append(f'<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BULL}" stop-opacity=".22"/><stop offset="1" stop-color="{BULL}" stop-opacity="0"/></radialGradient>')
    g.append(f'<circle cx="{W/2}" cy="72" r="26" fill="url(#glow)"/>')
    # identity strip beside the camera
    g.append(f'<text x="{W-4.5}" y="10" text-anchor="end" font-family="IBM Plex Mono" font-weight="500" font-size="2.1" letter-spacing=".5" fill="{DIM}">XAUUSD · 4H</text>')
    g.append(f'<rect x="{W-4.5-12}" y="12.4" width="12" height=".6" fill="{BULL}"/>')
    g.append(logo(W/2, 69, 1.15))
    g.append(f'<text x="{W/2}" y="90" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="9.4" letter-spacing=".5">'
             f'<tspan fill="{TEXT}">LIQUIDITY</tspan><tspan fill="{BULL}">LAB</tspan></text>')
    g.append(candles())
    # full-bleed accent bar + footer
    g.append(f'<rect x="{-BLEED}" y="141.2" width="{W+2*BLEED}" height="1.1" fill="{BULL}"/>')
    g.append(f'<text x="{W/2}" y="147" text-anchor="middle" font-family="IBM Plex Mono" font-weight="500" font-size="1.9" letter-spacing=".6" fill="{DIM}">READ THE LIQUIDITY</text>')
    return "\n".join(g)

cut = (f'M {R} 0 H {W-R} A {R} {R} 0 0 1 {W} {R} V {H-R} A {R} {R} 0 0 1 {W-R} {H} H {R} A {R} {R} 0 0 1 0 {H-R} V {R} A {R} {R} 0 0 1 {R} 0 Z')
x,y,w,h,r = CAM
cam = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'

def svg(kind):
    if kind == "print":
        vb = f"{-BLEED} {-BLEED} {W+2*BLEED} {H+2*BLEED}"; size = (W+2*BLEED, H+2*BLEED)
        body = f'''{art()}
<g id="cut-line" fill="none" stroke="#FF00FF" stroke-width=".2" stroke-dasharray="1 .6"><path d="{cut}"/>{cam}</g>
<rect id="camera-knockout" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FF00FF" fill-opacity=".18"/>'''
    else:
        pad = 8; vb = f"{-pad} {-pad} {W+2*pad} {H+2*pad}"; size = (W+2*pad, H+2*pad)
        lens = lambda lx,ly: (f'<circle cx="{lx}" cy="{ly}" r="7.4" fill="#1b1c22"/><circle cx="{lx}" cy="{ly}" r="5.6" fill="#050507" stroke="#2c2e36" stroke-width=".5"/>'
                              f'<circle cx="{lx-1.6}" cy="{ly-1.6}" r="1.1" fill="#3a4a66" opacity=".7"/>')
        body = f'''<defs><clipPath id="c"><path d="{cut}"/></clipPath>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2.5" stdDeviation="3" flood-color="#000" flood-opacity=".55"/></filter>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<rect x="{-pad}" y="{-pad}" width="{W+2*pad}" height="{H+2*pad}" fill="#e9e9ee"/>
<path d="{cut}" fill="{BG}" filter="url(#sh)"/>
<g clip-path="url(#c)">{art()}
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#3b3a38"/>
<rect x="{x+1.2}" y="{y+1.2}" width="{w-2.4}" height="{h-2.4}" rx="{r-1}" fill="#4a4946"/>
{lens(x+11,y+11)}{lens(x+11,y+28)}{lens(x+28,y+19.5)}
<circle cx="{x+28}" cy="{y+5.2}" r="1.6" fill="#ddd" opacity=".8"/><circle cx="{x+28}" cy="{y+33.8}" r="1.2" fill="#111"/>
<rect x="{-1}" y="{-1}" width="{W+2}" height="{H+2}" fill="url(#sheen)"/></g>
<path d="{cut}" fill="none" stroke="#1d1e26" stroke-width="1.2"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}mm" height="{size[1]}mm" viewBox="{vb}">
<style>{FONTS}</style>
{body}
</svg>'''

open(f"{out}/liquiditylab-iphone15pro-print.svg","w").write(svg("print"))
open(f"{out}/liquiditylab-iphone15pro-mockup.svg","w").write(svg("mockup"))
