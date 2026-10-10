import sys
out = sys.argv[1]
W, H, R = 74.4, 150.0, 12.0          # case back, mm
BLEED = 3.0
CAM = (4.2, 4.2, 39.0, 39.0, 9.5)    # camera cutout x,y,w,h,r
# liquiditylab.net palette
BG, PURPLE, PINK, ORANGE, TEXT, TEXT3 = "#080810", "#832388", "#E3436B", "#F0772F", "#f0f0f8", "#5a5a7a"
FONTS = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@800&amp;family=JetBrains+Mono:wght@700&amp;display=swap');"
GRADS = (f'<linearGradient id="gh" x1="0" x2="1" y1="0" y2="0"><stop stop-color="{PURPLE}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
         f'<linearGradient id="gd" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{PURPLE}"/><stop offset=".52" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
         f'<radialGradient id="r1" cx=".1" cy=".05" r=".6"><stop stop-color="{PINK}" stop-opacity=".16"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="r2" cx=".9" cy=".95" r=".55"><stop stop-color="{ORANGE}" stop-opacity=".12"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
         f'<filter id="bg" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>')

def art():
    cx, by, b = W/2, 62.0, 22.0       # badge centre x, top y, size
    return f'''<defs>{GRADS}</defs>
<rect x="{-BLEED}" y="{-BLEED}" width="{W+2*BLEED}" height="{H+2*BLEED}" fill="{BG}"/>
<rect x="{-BLEED}" y="{-BLEED}" width="{W+2*BLEED}" height="{H+2*BLEED}" fill="url(#r1)"/>
<rect x="{-BLEED}" y="{-BLEED}" width="{W+2*BLEED}" height="{H+2*BLEED}" fill="url(#r2)"/>
<rect x="{cx-b/2}" y="{by}" width="{b}" height="{b}" rx="{b*9/34:.2f}" fill="url(#gh)" opacity=".45" filter="url(#bg)"/>
<rect x="{cx-b/2}" y="{by}" width="{b}" height="{b}" rx="{b*9/34:.2f}" fill="url(#gh)"/>
<text x="{cx}" y="{by+b/2+2.75}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="7.8" fill="#fff">LL</text>
<text x="{cx}" y="{by+b+13}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" letter-spacing="-.17" fill="{TEXT}">Liquidity<tspan fill="url(#gd)">Lab</tspan></text>
<text x="{cx}" y="{H-9}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="2.1" letter-spacing=".5" fill="{TEXT3}">LIQUIDITYLAB.NET</text>'''

cut = (f'M {R} 0 H {W-R} A {R} {R} 0 0 1 {W} {R} V {H-R} A {R} {R} 0 0 1 {W-R} {H} H {R} A {R} {R} 0 0 1 0 {H-R} V {R} A {R} {R} 0 0 1 {R} 0 Z')
x,y,w,h,r = CAM
cam = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'

def svg(kind):
    if kind == "print":
        vb = f"{-BLEED} {-BLEED} {W+2*BLEED} {H+2*BLEED}"; size = (W+2*BLEED, H+2*BLEED)
        body = f'''<g id="artwork">{art()}</g>
<g id="cut-line" fill="none" stroke="#FF00FF" stroke-width=".2" stroke-dasharray="1 .6"><path d="{cut}"/>{cam}</g>
<rect id="camera-knockout" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FF00FF" fill-opacity=".18"/>'''
    else:
        pad = 8; vb = f"{-pad} {-pad} {W+2*pad} {H+2*pad}"; size = (W+2*pad, H+2*pad)
        lens = lambda lx,ly: (f'<circle cx="{lx}" cy="{ly}" r="7.4" fill="#1b1c22"/><circle cx="{lx}" cy="{ly}" r="5.6" fill="#050507" stroke="#2c2e36" stroke-width=".5"/>'
                              f'<circle cx="{lx-1.6}" cy="{ly-1.6}" r="1.1" fill="#3a4a66" opacity=".7"/>')
        body = f'''<defs><clipPath id="c"><path d="{cut}"/></clipPath>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2.5" stdDeviation="3" flood-color="#000" flood-opacity=".55"/></filter>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
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
