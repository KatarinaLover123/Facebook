"""Four detailed LiquidityLab iPhone 15 Pro case variants (liquiditylab.net logo + palette)."""
import math, random, sys, os
W, H, R = 74.4, 150.0, 12.0
BLEED = 3.0
CX, CY, CW, CH, CR = 4.2, 4.2, 39.0, 39.0, 9.5
BG, PURPLE, PINK, ORANGE, TEXT, TEXT2, TEXT3 = "#080810", "#832388", "#E3436B", "#F0772F", "#f0f0f8", "#9898b8", "#5a5a7a"
FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;800;900"
         "&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');")

def mix(t):
    """Brand gradient colour at t in [0,1]."""
    stops = [(0, (0x83, 0x23, 0x88)), (.5, (0xE3, 0x43, 0x6B)), (1, (0xF0, 0x77, 0x2F))]
    t = min(max(t, 0), 1)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            k = (t - a) / (b - a)
            return "#%02x%02x%02x" % tuple(round(x + (y - x) * k) for x, y in zip(ca, cb))

def defs():
    return (f'<linearGradient id="gh" x1="0" x2="1" y1="0" y2="0"><stop stop-color="{PURPLE}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
            f'<linearGradient id="gd" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{PURPLE}"/><stop offset=".52" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
            f'<linearGradient id="gu" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}"><stop stop-color="{PURPLE}"/><stop offset=".52" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
            f'<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>'
            f'<radialGradient id="r1" cx=".1" cy=".05" r=".6"><stop stop-color="{PINK}" stop-opacity=".16"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="r2" cx=".9" cy=".95" r=".55"><stop stop-color="{ORANGE}" stop-opacity=".12"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="hole" cx=".5" cy=".5" r=".5"><stop stop-color="{BG}" stop-opacity=".95"/><stop offset=".6" stop-color="{BG}" stop-opacity=".7"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>')

def full(fill, extra=""):
    return f'<rect x="{-BLEED}" y="{-BLEED}" width="{W+2*BLEED}" height="{H+2*BLEED}" fill="{fill}" {extra}/>'

def logo(cx, by, b, inverted=False, glow=True, word=True, word_y=13):
    rx = b * 9 / 34
    badge = BG if inverted else "url(#gh)"
    ll = "url(#gd)" if inverted else "#fff"
    s = ""
    if glow and not inverted:
        s += f'<rect x="{cx-b/2}" y="{by}" width="{b}" height="{b}" rx="{rx:.2f}" fill="url(#gh)" opacity=".45" filter="url(#blur)"/>'
    s += f'<rect x="{cx-b/2}" y="{by}" width="{b}" height="{b}" rx="{rx:.2f}" fill="{badge}"/>'
    s += f'<text x="{cx}" y="{by+b/2+b*.125}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="{b*.355:.2f}" fill="{ll}">LL</text>'
    if word:
        lab = BG if inverted else "url(#gd)"
        s += (f'<text x="{cx}" y="{by+b+word_y}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" '
              f'letter-spacing="-.17" fill="{TEXT}">Liquidity<tspan fill="{lab}">Lab</tspan></text>')
    return s

def mono(x, y, txt, size=2.0, fill=TEXT3, anchor="middle", ls=.5, weight=700):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="JetBrains Mono" font-weight="{weight}" '
            f'font-size="{size}" letter-spacing="{ls}" fill="{fill}">{txt}</text>')

# ── A · FLOW ── liquidity contour lines flowing under the logo
def flow():
    g = [full(BG), full("url(#r1)"), full("url(#r2)")]
    rnd = random.Random(3)
    ph = [rnd.uniform(0, 6.28) for _ in range(6)]
    n = 46
    for i in range(n):
        base = -6 + i * (H + 12) / n
        pts = []
        for k in range(0, 61):
            x = -BLEED + k * (W + 2 * BLEED) / 60
            y = (base + 3.2 * math.sin(x / 11 + ph[0] + i * .21) + 1.8 * math.sin(x / 5.3 + ph[1] - i * .13)
                 + 4.5 * math.sin(base / 23 + ph[2]) * math.cos(x / 17 + ph[3]))
            pts.append(f"{x:.2f},{y:.2f}")
        op = .18 + .5 * (i / n) ** 1.4
        sw = .16 if i % 5 else .32
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#gu)" stroke-width="{sw}" opacity="{op:.2f}"/>')
    g.append(f'<ellipse cx="{W/2}" cy="83" rx="34" ry="30" fill="url(#hole)"/>')
    g.append(logo(W / 2, 62, 22))
    g.append(mono(W / 2, 104.5, "TRADE LIQUIDITY. NOT NOISE.", 2.1, TEXT2, ls=.45, weight=500))
    g.append(mono(W / 2, H - 8, "LIQUIDITYLAB.NET", 1.9, TEXT2, ls=.6))
    return "".join(g)

# ── B · AURORA ── full-bleed brand gradient, dark inverted badge, giant outline monogram
def aurora():
    g = [full("url(#gu)"),
         f'<radialGradient id="shade" cx=".5" cy=".55" r=".75"><stop stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>',
         full("url(#shade)")]
    # giant cropped monogram as an outline, bleeding off the bottom
    g.append(f'<text x="{W/2}" y="{H-6}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="46" '
             f'fill="none" stroke="#fff" stroke-opacity=".32" stroke-width=".3" letter-spacing="-1">LL</text>')
    # fine diagonal sheen bands
    for i in range(7):
        x = -40 + i * 22
        g.append(f'<path d="M {x} {-BLEED} l 70 {H+2*BLEED}" stroke="#fff" stroke-opacity=".05" stroke-width="{6 if i%2 else 1.2}"/>')
    g.append(f'<rect x="{W/2-12}" y="58.5" width="24" height="24" rx="6.4" fill="#000" opacity=".35" filter="url(#blur)"/>')
    g.append(logo(W / 2, 58, 22, inverted=True))
    g.append(f'<text x="{W/2}" y="{58+22+13}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" letter-spacing="-.17" fill="#fff">Liquidity<tspan fill="{BG}">Lab</tspan></text>')
    g.append(mono(W / 2, 100, "TRADE LIQUIDITY. NOT NOISE.", 2.1, "#fff", ls=.45, weight=500).replace('fill="#fff"', 'fill="#fff" fill-opacity=".85"'))
    return "".join(g)

# ── C · SIGNATURE ── premium frame: gradient hairline, perimeter micro-text, camera ring, edition plate
def signature():
    g = [full(BG), full("url(#r1)"), full("url(#r2)")]
    def open_frame(i):
        r = R - i
        return (f"M {CX+CW+3.5} {i} H {W-R} A {r} {r} 0 0 1 {W-i} {R} V {H-R} A {r} {r} 0 0 1 {W-R} {H-i} "
                f"H {R} A {r} {r} 0 0 1 {i} {H-R} V {CY+CH+3.5}")
    g.append(f'<path id="mt" d="{open_frame(3.6)}" fill="none"/>')
    g.append(f'<path d="{open_frame(4.6)}" fill="none" stroke="url(#gu)" stroke-width=".3"/>')
    o = 1.3
    g.append(f'<rect x="{CX-o}" y="{CY-o}" width="{CW+2*o}" height="{CH+2*o}" rx="{CR+o}" fill="none" stroke="url(#gu)" stroke-width=".45"/>')
    unit = "LIQUIDITYLAB · TRADE LIQUIDITY. NOT NOISE. · "
    g.append(f'<text font-family="JetBrains Mono" font-weight="700" font-size="1.45" letter-spacing=".32" fill="{TEXT2}" fill-opacity=".55">'
             f'<textPath href="#mt">{unit*6}</textPath></text>')
    # corner registration ticks
    for (x, y, dx, dy) in [(W-9, 9, 1, 1), (9, H-9, -1, -1), (W-9, H-9, 1, -1)]:
        g.append(f'<path d="M {x} {y+dy*2.2} V {y} H {x-dx*2.2}" fill="none" stroke="{TEXT3}" stroke-width=".25"/>'.replace(f'H {x-dx*2.2}', f'H {x-dx*-2.2}' if False else f'H {x-dx*2.2}'))
    g.append(logo(W / 2, 60, 22))
    # thin gradient rule + edition plate
    g.append(f'<rect x="{W/2-9}" y="106" width="18" height=".35" fill="url(#gh)"/>')
    g.append(mono(W / 2, 112, "INSTITUTIONAL-STYLE TRADING INTELLIGENCE", 1.55, TEXT3, ls=.28, weight=500))
    g.append(f'<rect x="{W/2-13}" y="{H-22}" width="26" height="8.6" rx="1.6" fill="#fff" fill-opacity=".03" stroke="#fff" stroke-opacity=".12" stroke-width=".2"/>')
    g.append(mono(W / 2 - 11.2, H - 17.6, "EDITION", 1.35, TEXT3, "start", .3))
    g.append(mono(W / 2 + 11.2, H - 17.6, "001 / 500", 1.35, TEXT2, "end", .3))
    g.append(f'<line x1="{W/2-11.2}" y1="{H-16.4}" x2="{W/2+11.2}" y2="{H-16.4}" stroke="#fff" stroke-opacity=".1" stroke-width=".15"/>')
    g.append(mono(W / 2 - 11.2, H - 14.4, "MODEL", 1.35, TEXT3, "start", .3))
    g.append(mono(W / 2 + 11.2, H - 14.4, "IPHONE 15 PRO", 1.35, TEXT2, "end", .3))
    return "".join(g)

# ── D · IGNITE ── particle field converging into the badge (echoes the site's intro animation)
def ignite():
    g = [full(BG), full("url(#r1)"), full("url(#r2)")]
    rnd = random.Random(11)
    cx, cy = W / 2, 73
    for _ in range(2600):
        a = rnd.uniform(0, 2 * math.pi)
        d = 14 + rnd.expovariate(1 / 18)
        x, y = cx + math.cos(a) * d * 1.0, cy + math.sin(a) * d * 1.35
        if not (-BLEED < x < W + BLEED and -BLEED < y < H + BLEED):
            continue
        if CX - 1 < x < CX + CW + 1 and CY - 1 < y < CY + CH + 1:
            continue
        t = (math.sin(a - .8) + 1) / 2
        r = max(.18, .8 - d / 70) * rnd.uniform(.55, 1.15)
        op = max(.12, 1 - d / 85) * rnd.uniform(.6, 1)
        if rnd.random() < .16 and d < 55:   # motion streak toward the centre
            L = rnd.uniform(1.2, 3.4)
            x2, y2 = x + math.cos(a) * L, y + math.sin(a) * L * 1.35
            g.append(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{mix(t)}" stroke-width="{r*.7:.2f}" stroke-linecap="round" opacity="{op*.8:.2f}"/>')
        else:
            g.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{mix(t)}" opacity="{op:.2f}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="url(#hole)"/>')
    for k, rr in enumerate((19, 25)):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="url(#gu)" stroke-width=".18" opacity="{.5-k*.2}" stroke-dasharray="{.6+k} {1.6+k}"/>')
    g.append(logo(cx, cy - 11, 22, word=False))
    g.append(f'<ellipse cx="{W/2}" cy="107" rx="33" ry="9" fill="url(#hole)"/>')
    g.append(f'<text x="{W/2}" y="110" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" letter-spacing="-.17" fill="{TEXT}">Liquidity<tspan fill="url(#gd)">Lab</tspan></text>')
    g.append(mono(W / 2, H - 8, "LIQUIDITYLAB.NET", 1.9, TEXT2, ls=.6))
    return "".join(g)

VARIANTS = {"a-flow": flow, "b-aurora": aurora, "c-signature": signature, "d-ignite": ignite}

cut = f'M {R} 0 H {W-R} A {R} {R} 0 0 1 {W} {R} V {H-R} A {R} {R} 0 0 1 {W-R} {H} H {R} A {R} {R} 0 0 1 0 {H-R} V {R} A {R} {R} 0 0 1 {R} 0 Z'

def svg(art, kind):
    if kind == "print":
        vb, size = f"{-BLEED} {-BLEED} {W+2*BLEED} {H+2*BLEED}", (W + 2 * BLEED, H + 2 * BLEED)
        body = (f'<defs>{defs()}</defs><g id="artwork">{art}</g>'
                f'<g id="cut-line" fill="none" stroke="#FF00FF" stroke-width=".2" stroke-dasharray="1 .6"><path d="{cut}"/>'
                f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{CR}"/></g>'
                f'<rect id="camera-knockout" x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{CR}" fill="#FF00FF" fill-opacity=".18"/>')
    else:
        pad = 8
        vb, size = f"{-pad} {-pad} {W+2*pad} {H+2*pad}", (W + 2 * pad, H + 2 * pad)
        lens = lambda lx, ly: (f'<circle cx="{lx}" cy="{ly}" r="7.4" fill="#1b1c22"/><circle cx="{lx}" cy="{ly}" r="5.6" fill="#050507" stroke="#2c2e36" stroke-width=".5"/>'
                               f'<circle cx="{lx-1.6}" cy="{ly-1.6}" r="1.1" fill="#3a4a66" opacity=".7"/>')
        body = (f'<defs>{defs()}<clipPath id="c"><path d="{cut}"/></clipPath>'
                f'<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2.5" stdDeviation="3" flood-color="#000" flood-opacity=".55"/></filter>'
                f'<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
                f'<rect x="{-pad}" y="{-pad}" width="{W+2*pad}" height="{H+2*pad}" fill="#e9e9ee"/>'
                f'<path d="{cut}" fill="{BG}" filter="url(#sh)"/>'
                f'<g clip-path="url(#c)">{art}'
                f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{CR}" fill="#3b3a38"/>'
                f'<rect x="{CX+1.2}" y="{CY+1.2}" width="{CW-2.4}" height="{CH-2.4}" rx="{CR-1}" fill="#4a4946"/>'
                f'{lens(CX+11,CY+11)}{lens(CX+11,CY+28)}{lens(CX+28,CY+19.5)}'
                f'<circle cx="{CX+28}" cy="{CY+5.2}" r="1.6" fill="#ddd" opacity=".8"/><circle cx="{CX+28}" cy="{CY+33.8}" r="1.2" fill="#111"/>'
                f'<rect x="-1" y="-1" width="{W+2}" height="{H+2}" fill="url(#sheen)"/></g>'
                f'<path d="{cut}" fill="none" stroke="#1d1e26" stroke-width="1.2"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}mm" height="{size[1]}mm" viewBox="{vb}">'
            f'<style>{FONTS}</style>{body}</svg>')

def write(variants, out):
    for name, fn in variants.items():
        art = fn()
        for kind in ("print", "mockup"):
            open(os.path.join(out, f"{name}-{kind}.svg"), "w").write(svg(art, kind))

if __name__ == "__main__":
    write(VARIANTS, sys.argv[1])
