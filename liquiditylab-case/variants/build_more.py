"""Five more LiquidityLab case variants: Carbon, Glass, Monogram, Pulse, Noir (premium)."""
import math, random, sys
from build_variants import (W, H, R, BLEED, CX, CY, CW, CH, CR, BG, PURPLE, PINK, ORANGE, TEXT, TEXT2, TEXT3,
                            full, logo, mono, write)

GOLD = ('<linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">'
        '<stop stop-color="#8a6a2a"/><stop offset=".3" stop-color="#f3d48a"/><stop offset=".55" stop-color="#b8892f"/>'
        '<stop offset=".8" stop-color="#f0d27e"/><stop offset="1" stop-color="#9c7630"/></linearGradient>').format(w=W, h=H)

def wordmark(y, lab="url(#gd)", main=TEXT):
    return (f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" '
            f'letter-spacing="-.17" fill="{main}">Liquidity<tspan fill="{lab}">Lab</tspan></text>')

# ── E · CARBON ── twill carbon-fibre weave, off-centre gradient racing stripes
def carbon():
    s = .9
    g = [f'<defs><linearGradient id="cfh" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#2a2b36"/><stop offset=".5" stop-color="#0b0b11"/><stop offset="1" stop-color="#20212b"/></linearGradient>'
         f'<linearGradient id="cfv" x1="0" x2="1" y1="0" y2="0"><stop stop-color="#24252f"/><stop offset=".5" stop-color="#07070c"/><stop offset="1" stop-color="#1b1c25"/></linearGradient>'
         f'<pattern id="cf" width="{2*s}" height="{2*s}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<rect width="{s}" height="{s}" fill="url(#cfh)"/><rect x="{s}" width="{s}" height="{s}" fill="url(#cfv)"/>'
         f'<rect y="{s}" width="{s}" height="{s}" fill="url(#cfv)"/><rect x="{s}" y="{s}" width="{s}" height="{s}" fill="url(#cfh)"/></pattern>'
         f'<linearGradient id="gv" x1="0" x2="0" y1="0" y2="1"><stop stop-color="{PURPLE}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>'
         f'<radialGradient id="cfl" cx=".3" cy=".25" r=".8"><stop stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>',
         full("url(#cf)"), full("url(#cfl)")]
    for x, w in ((56, 2.6), (60.4, 1.0)):
        g.append(f'<rect x="{x}" y="{-BLEED}" width="{w}" height="{52+BLEED}" fill="url(#gv)"/>')
        g.append(f'<rect x="{x}" y="110" width="{w}" height="{H-110+BLEED}" fill="url(#gv)"/>')
    g.append(f'<ellipse cx="{W/2}" cy="80" rx="30" ry="28" fill="url(#hole)"/>')
    g.append(logo(W / 2, 60, 22))
    g.append(mono(W / 2, 102, "TRADE LIQUIDITY. NOT NOISE.", 2.1, TEXT2, ls=.45, weight=500))
    g.append(mono(9, H - 8, "LL—15P", 1.8, TEXT3, "start", .5))
    g.append(mono(W - 20, H - 8, "LIQUIDITYLAB.NET", 1.8, TEXT2, "end", .5))
    return "".join(g)

# ── F · GLASS ── blurred brand orbs behind a frosted-glass card
def glass():
    orbs = [(14, 30, 26, PURPLE), (64, 78, 24, PINK), (20, 128, 26, ORANGE)]
    o = lambda blur, op: "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}" filter="url(#{blur})"/>' for x, y, r, c in orbs)
    px, py, pw, ph = 9, 52, W - 18, 62
    g = [f'<defs><filter id="ob" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>'
         f'<filter id="ob2" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14"/></filter>'
         f'<clipPath id="card"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="7"/></clipPath>'
         f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".45"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient></defs>',
         full(BG), o("ob", .85),
         f'<g clip-path="url(#card)">{full(BG)}{o("ob2", .7)}<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#fff" fill-opacity=".07"/></g>',
         f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="7" fill="none" stroke="url(#edge)" stroke-width=".3"/>',
         logo(W / 2, py + 9, 20, glow=False, word=False),
         wordmark(py + 41, lab="#fff"),
         f'<rect x="{W/2-8}" y="{py+46}" width="16" height=".3" fill="#fff" opacity=".35"/>',
         mono(W / 2, py + 53, "TRADE LIQUIDITY. NOT NOISE.", 1.9, "#fff", ls=.4, weight=500).replace('fill="#fff"', 'fill="#fff" fill-opacity=".8"'),
         mono(W / 2, H - 8, "LIQUIDITYLAB.NET", 1.9, "#fff", ls=.6).replace('fill="#fff"', 'fill="#fff" fill-opacity=".55"')]
    return "".join(g)

# ── G · MONOGRAM ── tonal luxury LL repeat with a framed centre plate
def monogram():
    g = [full(BG)]
    sx, sy = 9.3, 9.0
    for row in range(-1, 18):
        for col in range(-1, 9):
            x = col * sx + (sx / 2 if row % 2 else 0) + 2
            y = row * sy + 4
            if CX - 3 < x < CX + CW + 3 and CY - 3 < y < CY + CH + 4:
                continue
            if row % 2 == col % 2:
                g.append(f'<text x="{x:.2f}" y="{y+1.2:.2f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="3.4" fill="url(#gu)" opacity=".26">LL</text>')
            else:
                g.append(f'<path d="M {x} {y-1.4} l 1.2 1.4 l -1.2 1.4 l -1.2 -1.4 z" fill="none" stroke="url(#gu)" stroke-width=".22" opacity=".3"/>')
    px, py, pw, ph = 7, 50, W - 14, 66
    g.append(f'<rect x="{px-2}" y="{py-2}" width="{pw+4}" height="{ph+4}" rx="6" fill="{BG}"/>')
    g.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4.6" fill="{BG}" stroke="url(#gu)" stroke-width=".35"/>')
    g.append(f'<rect x="{px+1.4}" y="{py+1.4}" width="{pw-2.8}" height="{ph-2.8}" rx="3.6" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width=".2"/>')
    g.append(logo(W / 2, py + 9, 20, word=False))
    g.append(wordmark(py + 41))
    g.append(mono(W / 2, py + 50, "EST. TRADING INTELLIGENCE", 1.6, TEXT3, ls=.35, weight=500))
    g.append(mono(W / 2, py + 57, "◆  LIQUIDITYLAB.NET  ◆", 1.6, TEXT2, ls=.35, weight=700))
    return "".join(g)

# ── H · PULSE ── badge-shaped rings radiating outwards
def pulse():
    g = [full(BG), full("url(#r1)"), full("url(#r2)")]
    cx, cy = W / 2, 73
    for i in range(1, 22):
        b = 22 + i * 7.2
        op = max(.05, .75 - i * .034)
        sw = .45 if i % 4 == 0 else .18
        dash = 'stroke-dasharray=".5 1.1"' if i % 4 == 2 else ""
        g.append(f'<rect x="{cx-b/2:.2f}" y="{cy-b/2:.2f}" width="{b:.2f}" height="{b:.2f}" rx="{b*9/34:.2f}" '
                 f'fill="none" stroke="url(#gu)" stroke-width="{sw}" opacity="{op:.2f}" {dash}/>')
    g.append(logo(cx, cy - 11, 22, word=False))
    g.append(f'<ellipse cx="{W/2}" cy="{cy+31}" rx="36" ry="10" fill="url(#hole)"/>')
    g.append(wordmark(cy + 30))
    g.append(mono(W / 2, cy + 37, "TRADE LIQUIDITY. NOT NOISE.", 1.9, TEXT2, ls=.4, weight=500))
    g.append(mono(W / 2, H - 8, "LIQUIDITYLAB.NET", 1.9, TEXT2, ls=.6))
    return "".join(g)

# ── I · NOIR ── PREMIUM: matte black, gold-foil guilloche rosette, banknote border band, numbered plate
def noir():
    g = [f'<defs>{GOLD}</defs>', full("#050507"),
         f'<radialGradient id="vig" cx=".5" cy=".48" r=".7"><stop stop-color="#1a1610" stop-opacity=".9"/><stop offset="1" stop-color="#050507" stop-opacity="0"/></radialGradient>',
         full("url(#vig)")]
    cx, cy = W / 2, 73
    # guilloche rosette: overlapping epitrochoid rings
    for j in range(36):
        ph = j * math.pi / 18
        pts = []
        for k in range(0, 721):
            t = k / 720 * 2 * math.pi
            r = 21 + 3.2 * math.sin(12 * t + ph) + 1.4 * math.sin(30 * t - ph * 2)
            pts.append(f"{cx + r*math.cos(t):.2f},{cy + r*math.sin(t):.2f}")
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#gold)" stroke-width=".07" opacity=".75"/>')
    for rr in (14.2, 27.2):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="url(#gold)" stroke-width=".25"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#050507"/>')
    # banknote wave band near the bottom
    for j in range(14):
        pts = []
        for k in range(0, 121):
            x = -BLEED + k * (W + 2 * BLEED) / 120
            y = H - 22 + 2.6 * math.sin(x / 3.1 + j * .45) * math.sin(x / 17 + j * .2)
            pts.append(f"{x:.2f},{y:.2f}")
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#gold)" stroke-width=".07" opacity=".7"/>')
    for y in (H - 26.2, H - 17.8):
        g.append(f'<line x1="{-BLEED}" y1="{y}" x2="{W+BLEED}" y2="{y}" stroke="url(#gold)" stroke-width=".2"/>')
    # gold badge + wordmark
    b = 17
    g.append(f'<rect x="{cx-b/2}" y="{cy-b/2}" width="{b}" height="{b}" rx="{b*9/34:.2f}" fill="url(#gold)"/>')
    g.append(f'<text x="{cx}" y="{cy+b*.125}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="{b*.355:.2f}" fill="#050507">LL</text>')
    g.append(wordmark(cy + 39, lab="url(#gold)", main="#efe6d2"))
    g.append(mono(W / 2, cy + 46, "PREMIUM EDITION", 1.9, "#b8892f", ls=.9, weight=700))
    # hairline frame + camera ring, as on Signature
    i, r = 3.4, R - 3.4
    g.append(f'<path d="M {CX+CW+3.5} {i} H {W-R} A {r} {r} 0 0 1 {W-i} {R} V {H-R} A {r} {r} 0 0 1 {W-R} {H-i} H {R} A {r} {r} 0 0 1 {i} {H-R} V {CY+CH+3.5}" fill="none" stroke="url(#gold)" stroke-width=".25"/>')
    o = 1.3
    g.append(f'<rect x="{CX-o}" y="{CY-o}" width="{CW+2*o}" height="{CH+2*o}" rx="{CR+o}" fill="none" stroke="url(#gold)" stroke-width=".35"/>')
    g.append(mono(W / 2, H - 11.6, "No. 001 / 100", 1.7, "#efe6d2", ls=.5, weight=500).replace('fill="#efe6d2"', 'fill="#efe6d2" fill-opacity=".7"'))
    g.append(mono(W / 2, H - 7.8, "LIQUIDITYLAB.NET", 1.6, "#8a6a2a", ls=.7))
    return "".join(g)

if __name__ == "__main__":
    write({"e-carbon": carbon, "f-glass": glass, "g-monogram": monogram, "h-pulse": pulse, "i-noir-premium": noir}, sys.argv[1])
