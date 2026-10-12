import json, sys, os, html, datetime
S = '/tmp/claude-0/-home-claude-vremax/f9f34287-da94-548e-8d92-9b3107858ebc/scratchpad/k30/'
sys.path.insert(0, S + 'gen')
from data import DAYS
E = html.escape
INK, PAPER, GOLD, JADE, MINT = '#14201A', '#F6F3EC', '#D9B44A', '#0F6B57', '#BFE8D9'
F = '/home/claude/dossier/node_modules/@fontsource/'
FF = ''.join(f"@font-face{{font-family:'Hanken Grotesk';font-weight:{w};src:url(file://{F}hanken-grotesk/files/hanken-grotesk-latin-{w}-normal.woff2)}}\n" for w in (400, 500, 600, 700, 800))
FF += ''.join(f"@font-face{{font-family:'Fraunces';font-weight:{w};src:url(file://{F}fraunces/files/fraunces-latin-{w}-normal.woff2)}}\n" for w in (600, 700))

GOLD = '#3DBE8B'   # accent vert vif (remplace l'ancien doré)
DEEP = '#0A4F40'
def T(bg):
    if bg == 'ink': return dict(bg=INK, fg='#FFFFFF', hl=MINT, sub='#C9D6CF', kick=GOLD, band=JADE, bandfg='#FFFFFF', btn='#FFFFFF', btnfg=JADE, card=PAPER, cardfg=INK, deco=JADE, ext='#05110C', iso=('#1F8A6E', '#0F6B57', '#0A4F40'))
    if bg == 'gold': return dict(bg=JADE, fg='#FFFFFF', hl=MINT, sub='#DFF3EA', kick=MINT, band=INK, bandfg='#FFFFFF', btn=MINT, btnfg=INK, card=PAPER, cardfg=INK, deco=MINT, ext='#063A2E', iso=('#BFE8D9', '#7FCBB0', '#4FA98C'))
    return dict(bg=PAPER, fg=INK, hl=JADE, sub='#3E4B44', kick=JADE, band=INK, bandfg='#FFFFFF', btn=JADE, btnfg='#FFFFFF', card='#FFFFFF', cardfg=INK, deco=JADE, ext='#C9C2B2', iso=('#2E9A7C', '#0F6B57', '#0A4F40'))

def nb(s): return s.replace(' ?', ' ?').replace(' :', ' :').replace(' !', ' !')

def hsize(h, width, base=76):
    longest = max(len(p) for p in h.split('|'))
    for s in (base, 70, 64, 58, 54, 50, 46):
        if longest * s * 0.52 <= width: return s
    return 44

def headline(h, t, size):
    a, _, b = nb(h).partition('|')
    ext = t['ext']
    sh = ', '.join(f'{i}px {i}px 0 {ext}' for i in range(1, 7)) + ', 10px 14px 18px rgba(0,0,0,0.35)'
    return (f'<h1 style="margin: 0; font-family: \'Fraunces\', serif; font-weight: 700; font-size: {size}px; line-height: 1.06; letter-spacing: -0.02em; color: {t["fg"]}; text-shadow: {sh}">{E(a)}'
            + (f'<br><span style="color: {t["hl"]}">{E(b)}</span>' if b else '') + '</h1>')

def header(t, src):
    pill_bg, pill_fg = (INK, GOLD) if t['bg'] == GOLD else (GOLD, INK)
    name = INK if t['bg'] in (GOLD, PAPER) else '#FFFFFF'
    return f'''<div style="display: flex; align-items: center; gap: 13px; flex: none">
<img src="{src('logo')}" alt="Logo VREMAX" style="width: 54px; height: 54px; border-radius: 12px; display: block">
<div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 30px; letter-spacing: 0.2em; color: {name}">VREMAX</div>
<div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 22px; letter-spacing: 0.14em; color: {pill_fg}; background: {pill_bg}; border-radius: 9px; padding: 6px 13px 5px 15px; line-height: 1">COMPTABILITÉ</div>
</div>'''

def kicker(k, t):
    return f'<div style="font-size: 18px; font-weight: 800; letter-spacing: 0.2em; text-transform: uppercase; color: {t["kick"]}">{E(k)}</div>'

def footer(t):
    return f'''<div style="flex: none; height: 92px; margin: 0 -64px; padding: 0 64px; background: {t['band']}; display: flex; align-items: center; justify-content: space-between">
<div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 25px; color: {t['bandfg']}">Demandez votre démonstration</div>
<div style="display: flex; align-items: center; gap: 14px">
<div style="font-size: 19px; font-weight: 800; color: {t['bandfg']}">+225 05 74 99 96 75</div>
<div style="background: {t['btn']}; color: {t['btnfg']}; font-weight: 800; font-size: 20px; border-radius: 30px; padding: 8px 19px">www.vremaxx.com</div>
</div>
</div>'''

def iso_box(x, y, w, d, h, cols, win):
    # boîte isométrique : (x,y) = coin avant-bas ; w = largeur côté droit, d = côté gauche, h = hauteur
    import math
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    R = lambda px, py, l: (px + l * c, py - l * s)
    Lf = lambda px, py, l: (px - l * c, py - l * s)
    A = (x, y); B = R(x, y, w); C = Lf(x, y, d)
    up = lambda p: (p[0], p[1] - h)
    D = (B[0] - d * c, B[1] - d * s)
    top = [up(A), up(B), up(D), up(C)]
    right = [A, B, up(B), up(A)]
    left = [A, C, up(C), up(A)]
    P = lambda pts: ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
    out = f'<polygon points="{P(left)}" fill="{cols[1]}"/><polygon points="{P(right)}" fill="{cols[2]}"/><polygon points="{P(top)}" fill="{cols[0]}"/>'
    # fenêtres
    rows = max(1, int(h // 34))
    for r in range(rows):
        yy = -18 - r * 34
        for k in range(max(1, int(w // 30))):
            l0 = 10 + k * 30
            p1 = R(x, y + yy, l0); p2 = R(x, y + yy, l0 + 14)
            out += f'<polygon points="{P([p1, p2, (p2[0], p2[1]-18), (p1[0], p1[1]-18)])}" fill="{win}" opacity="0.55"/>'
        for k in range(max(1, int(d // 30))):
            l0 = 10 + k * 30
            p1 = Lf(x, y + yy, l0); p2 = Lf(x, y + yy, l0 + 14)
            out += f'<polygon points="{P([p1, p2, (p2[0], p2[1]-18), (p1[0], p1[1]-18)])}" fill="{win}" opacity="0.35"/>'
    return out

def deco(t):
    cols = t['iso']; win = '#FFFFFF' if t['bg'] != PAPER else '#DFF3EA'
    boxes = iso_box(230, 470, 110, 90, 330, cols, win) + iso_box(360, 520, 90, 80, 230, cols, win) + iso_box(120, 560, 80, 70, 170, cols, win)
    return f'<svg aria-hidden="true" viewBox="0 0 480 600" style="position: absolute; right: -40px; top: -40px; width: 480px; height: 600px; opacity: {0.22 if t["bg"] != PAPER else 0.18}">{boxes}</svg>'

def textblock(d, t, w, gap=14):
    s = hsize(d['h'], w)
    sub = f'<p style="margin: 0; font-size: 23px; line-height: 1.42; color: {t["sub"]}; max-width: {w}px">{E(nb(d["s"]))}</p>' if d.get('s') else ''
    return f'<div style="display: flex; flex-direction: column; gap: {gap}px; flex: none">{kicker(d["k"], t)}{headline(d["h"], t, s)}{sub}</div>'

def board(d, src, photos):
    t = T(d['bg']); L = d['L']
    if L == 'shot':
        pos = d.get('pos', 'left top')
        inner = textblock(d, t, 952) + f'''
<div style="flex: 1; min-height: 0; margin: 6px 20px -8px; background: #0B110E; border-radius: 18px 18px 0 0; padding: 10px 10px 0; box-sizing: border-box; transform: perspective(1400px) rotateX(14deg) rotateY(-10deg); transform-origin: 50% 100%; box-shadow: 8px 8px 0 #05110C, 14px 14px 0 rgba(5,17,12,0.6), 30px 40px 60px rgba(0,0,0,0.45)">
<img src="{src(d['img'])}" alt="Capture de VREMAX Comptabilité : {E(d['k'])}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; border-radius: 10px 10px 0 0; display: block">
</div>'''
    elif L == 'doc':
        inner = textblock(d, t, 952) + f'''
<div style="flex: 1; min-height: 0; display: flex; justify-content: center; margin-bottom: -8px">
<img src="{src(d['img'])}" alt="Document généré par VREMAX Comptabilité" style="height: 100%; width: 860px; object-fit: cover; object-position: top; border-radius: 12px 12px 0 0; display: block; box-shadow: 10px 10px 0 rgba(0,0,0,0.25), 30px 40px 60px rgba(0,0,0,0.45); transform: perspective(1400px) rotateX(12deg) rotateY(12deg) rotateZ(-2deg); transform-origin: 50% 100%">
</div>'''
    elif L == 'compare':
        li = lambda xs, mark, col: ''.join(f'<div style="display: flex; gap: 12px; align-items: flex-start"><div style="flex: none; width: 30px; height: 30px; border-radius: 50%; background: {col}; color: #FFFFFF; font-weight: 800; font-size: 18px; display: flex; align-items: center; justify-content: center">{mark}</div><div style="font-size: 21px; line-height: 1.3; font-weight: 600">{E(x)}</div></div>' for x in xs)
        inner = textblock(d, t, 952) + f'''
<div style="flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; padding-bottom: 30px">
<div style="background: #FFFFFF; border: 2px solid #E3C9C4; border-radius: 22px; padding: 26px; display: flex; flex-direction: column; gap: 16px; color: {INK}"><div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 28px; color: #9B3B2E">Aujourd'hui</div>{li(d['left'], '✕', '#B54A3A')}</div>
<div style="background: {INK}; border-radius: 22px; padding: 26px; display: flex; flex-direction: column; gap: 16px; color: #FFFFFF"><div style="font-family: 'Fraunces', serif; font-weight: 700; font-size: 28px; color: {GOLD}">Avec VREMAX</div>{li(d['right'], '✓', JADE)}</div>
</div>'''
    elif L == 'formula':
        parts = d['parts']; OP = d.get("op", "\u2212")
        chips = ''
        for i, p in enumerate(parts):
            if i: chips += f'<div style="font-family: \'Fraunces\', serif; font-size: 60px; font-weight: 700; color: {GOLD}; line-height: 1">{OP}</div>'
            chips += f'<div style="background: {t["card"]}; color: {t["cardfg"]}; border-radius: 18px; padding: 22px 26px; font-size: 26px; font-weight: 800; text-align: center; flex: 1; box-shadow: 0 8px 0 rgba(0,0,0,0.3), 0 18px 26px rgba(0,0,0,0.25)">{E(p)}</div>'
        inner = textblock(d, t, 952) + f'''
<div style="flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; gap: 22px; padding-bottom: 20px">
<div style="display: flex; align-items: center; gap: 16px">{chips}</div>
<div style="font-family: 'Fraunces', serif; font-size: 60px; font-weight: 700; color: {GOLD}; line-height: 1; text-align: center">=</div>
<div style="background: {GOLD}; color: {INK}; border-radius: 22px; padding: 28px; box-shadow: 0 10px 0 #0A4F40, 0 22px 30px rgba(0,0,0,0.3); font-family: 'Fraunces', serif; font-size: 40px; font-weight: 700; text-align: center">{E(d['result'])}</div>
</div>'''
    elif L == 'steps':
        st = ''.join(f'<div style="display: flex; gap: 18px; align-items: center"><div style="flex: none; width: 52px; height: 52px; border-radius: 50%; background: {INK}; color: {GOLD}; font-family: \'Fraunces\', serif; font-weight: 700; font-size: 26px; display: flex; align-items: center; justify-content: center">{i}</div><div style="font-size: 25px; font-weight: 700; color: {INK}">{E(x)}</div></div>' for i, x in enumerate(d['steps'], 1))
        inner = textblock(d, t, 952) + f'''
<div style="flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; gap: 18px; padding-bottom: 10px">{st}
<div style="margin-top: 10px; align-self: flex-start; background: {GOLD}; color: {INK}; font-family: 'Fraunces', serif; font-weight: 700; font-size: 44px; border-radius: 16px; padding: 12px 26px">+225 05 74 99 96 75</div>
</div>'''
    elif L == 'photo':
        key = d['photo']
        s_ = hsize(d['h'], 470, 70)
        sub = f'<p style="margin: 0; font-size: 22px; line-height: 1.42; color: {t["sub"]}">{E(nb(d["s"]))}</p>'
        text = f'''<div style="flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; gap: 16px; width: 470px; position: relative; z-index: 2; padding-bottom: 40px">
{kicker(d['k'], t)}{headline(d['h'], t, s_)}{sub}</div>'''
        ring = GOLD if t['bg'] != JADE else MINT
        if key.startswith('f'):
            art = f'''<div style="position: absolute; right: 50px; top: 150px; width: 470px; height: 700px; border-radius: 28px; background: {ring}; transform: perspective(1400px) rotateY(-14deg) rotateX(4deg) translate(22px, 22px); opacity: 0.9"></div>
<div style="position: absolute; right: 64px; top: 140px; width: 470px; height: 700px; border-radius: 28px; overflow: hidden; transform: perspective(1400px) rotateY(-14deg) rotateX(4deg); box-shadow: 30px 40px 60px rgba(0,0,0,0.45)"><img src="{src(key)}" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>'''
        else:
            art = f'''<div style="position: absolute; right: -90px; bottom: 60px; width: 640px; height: 640px; border-radius: 50%; background: {ring}; box-shadow: inset -30px -40px 0 rgba(0,0,0,0.18), 0 40px 70px rgba(0,0,0,0.35)"></div>
<img src="{src(key)}" alt="" style="position: absolute; right: -50px; bottom: 92px; height: 740px; max-width: 560px; object-fit: contain; object-position: right bottom; display: block; filter: drop-shadow(18px 24px 0 rgba(0,0,0,0.18)) drop-shadow(0 30px 40px rgba(0,0,0,0.35))">'''
        return shell(t, src, text, extra=art)
    else:  # statement
        s = min(hsize(d['h'], 952, 84) + 4, 88)
        extra = ''
        if d.get('chips'):
            extra = '<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 10px">' + ''.join(f'<span style="background: {t["card"]}; color: {t["cardfg"]}; font-weight: 700; font-size: 22px; border-radius: 30px; padding: 11px 22px; box-shadow: 0 6px 0 rgba(0,0,0,0.28), 0 14px 20px rgba(0,0,0,0.18)">{E(c)}</span>' for c in d['chips']) + '</div>'
        if d.get('pills'):
            extra = '<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 10px">' + ''.join(f'<span style="background: {GOLD if i < 4 else t["card"]}; color: {INK}; font-weight: 800; font-size: 24px; border-radius: 30px; padding: 12px 24px; box-shadow: 0 6px 0 rgba(0,0,0,0.3), 0 14px 20px rgba(0,0,0,0.2)">{E(c)}</span>' for i, c in enumerate(d['pills'])) + '</div>'
        inner = f'''<div style="flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; gap: 22px; padding-bottom: 20px">
{kicker(d['k'], t)}{headline(d['h'], t, s)}
<p style="margin: 0; font-size: 26px; line-height: 1.42; color: {t['sub']}; max-width: 900px">{E(nb(d['s']))}</p>{extra}</div>'''
    return shell(t, src, inner)

def shell(t, src, inner, extra=''):
    return f'''<div style="width: 1080px; height: 1080px; position: relative; overflow: hidden; background: {t['bg']}; font-family: 'Hanken Grotesk', sans-serif; color: {t['fg']}">
{deco(t)}{extra}
<div style="position: absolute; inset: 0; box-sizing: border-box; padding: 48px 64px 0; display: flex; flex-direction: column; gap: 24px">
{header(t, src)}
{inner}
{footer(t)}
</div>
</div>'''

if __name__ == '__main__':
    A = S + 'assets/'
    photos = {f[:-4]: 1 for f in os.listdir(A) if f.startswith('p') and f.endswith('.png')}
    def lsrc(k):
        for ext in ('.png', '.jpg'):
            if os.path.exists(A + k + ext): return 'file://' + A + k + ext
        return ''
    only = sys.argv[1:]
    for i, d in enumerate(DAYS):
        n = i + 1
        if only and str(n) not in only: continue
        body = board(d, lsrc, photos)
        open(f'{S}render/Jour{n:02d}.html', 'w').write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{FF}body{{margin:0}}</style></head><body>{body}</body></html>')
    print('ok')
