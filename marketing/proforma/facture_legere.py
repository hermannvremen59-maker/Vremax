# Facture Digital-Ivoire en PDF LÉGER (polices standard non embarquées, images réduites),
# même charte que facture.cjs — pour l'envoyer en pièce jointe d'e-mail.
# Usage : python3 facture_legere.py spec.json sortie.pdf logo.png signature.png
import json, sys, io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image

spec = json.load(open(sys.argv[1], encoding='utf-8'))
out, logo_p, sig_p = sys.argv[2], sys.argv[3], sys.argv[4]
W, H = A4
NAVY, RED, GREY, LINE, SOFT, GREEN = '#1E2A5E', '#D93A2B', '#55607A', '#DCE1EF', '#F7F8FC', '#1E9E5B'
def F(n): return f"{round(n):,}".replace(',', ' ') + ' F'

def img(path, size, jpeg=False):
    im = Image.open(path).convert('RGBA'); im.thumbnail(size)
    if jpeg:
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); b = io.BytesIO(); bg.save(b, 'JPEG', quality=55)
    else:
        b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    b.seek(0); return ImageReader(b)

c = canvas.Canvas(out, pagesize=A4, pageCompression=1)
c.setTitle(f"Facture {spec['numero']} — {spec['client']['nom']}"); c.setAuthor('Digital-Ivoire')
M = 40; y = H - 36
def rrect(x, y, w, h, r, fill=None, stroke=None):
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)
def txt(x, y, s, size=9, bold=False, color='#1F2A44', font=None, right=False, italic=False):
    c.setFillColor(color); f = font or ('Helvetica-Bold' if bold else 'Helvetica-Oblique' if italic else 'Helvetica'); c.setFont(f, size)
    (c.drawRightString if right else c.drawString)(x, y, s)

# en-tête
c.saveState(); pth=c.beginPath(); pth.circle(M+25, y-25, 25); c.clipPath(pth, stroke=0, fill=0); c.drawImage(img(logo_p, (100, 100), jpeg=True), M, y - 50, 50, 50); c.restoreState()
txt(M + 60, y - 14, 'Digital - Ivoire', 16, True, NAVY)
txt(M + 60, y - 27, 'COMMUNICATION MARKETING & GESTION', 7, color=GREY)
txt(M + 60, y - 39, "Abidjan, Côte d'Ivoire", 7.5, color=GREY)
txt(M + 60, y - 49, 'Tél : +225 05 74 99 96 75  •  hello@vremaxx.com  •  www.vremaxx.com', 7.5, color=GREY)
rrect(W - M - 150, y - 56, 150, 58, 6, fill=NAVY)
txt(W - M - 12, y - 18, 'FACTURE', 13, True, 'white', right=True)
txt(W - M - 12, y - 33, f"N° {spec['numero']}", 8.5, color='white', right=True)
txt(W - M - 12, y - 46, f"Abidjan, le {spec['date']}", 8.5, color='white', right=True)
y -= 66; c.setStrokeColor(NAVY); c.setLineWidth(2.5); c.line(M, y, W - M, y)
# bandeau
y -= 58; rrect(M, y, W - 2 * M, 48, 8, fill=NAVY)
txt(M + 14, y + 27, spec['titre'], 15, True, 'white'); txt(M + 14, y + 12, spec.get('sous_titre', ''), 9, color='#C9D1EC')
# client / objet
y -= 22; colw = (W - 2 * M - 14) / 2
txt(M, y, 'FACTURÉ À', 7.5, True, RED); txt(M + colw + 14, y, 'OBJET', 7.5, True, RED)
y -= 58
for i, x in enumerate((M, M + colw + 14)):
    rrect(x, y, colw, 52, 4, fill=SOFT, stroke=LINE); c.setFillColor(NAVY); c.rect(x, y, 3, 52, fill=1, stroke=0)
cl = spec['client']
txt(M + 10, y + 38, cl['nom'], 9.5, True); txt(M + 10, y + 25, cl.get('activite', ''), 9); txt(M + 10, y + 12, cl.get('email', ''), 9)
from reportlab.lib.utils import simpleSplit
for k, line in enumerate(simpleSplit(spec['objet'], 'Helvetica', 9, colw - 20)[:3]):
    txt(M + colw + 24, y + 38 - k * 13, line, 9)
# tableau
y -= 26; txt(M, y, 'DÉTAIL DE LA FACTURE', 8.5, True, RED); c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(M, y - 5, W - M, y - 5)
y -= 30; c.setFillColor(NAVY); c.rect(M, y, W - 2 * M, 20, fill=1, stroke=0)
txt(M + 10, y + 6.5, 'Désignation', 8.5, True, 'white'); txt(W - M - 10, y + 6.5, 'Montant', 8.5, True, 'white', right=True)
for i, (a, b, m) in enumerate(spec['lignes']):
    y -= 36
    if i % 2: c.setFillColor(SOFT); c.rect(M, y, W - 2 * M, 36, fill=1, stroke=0)
    txt(M + 10, y + 21, a, 9.5, True); txt(M + 10, y + 8, b, 8, color=GREY)
    txt(W - M - 10, y + 21, F(m) if isinstance(m, (int, float)) else m, 9.5, right=True)
    c.setStrokeColor(LINE); c.line(M, y, W - M, y)
# totaux
tot, ac = spec['total'], spec.get('acompte', {}).get('montant', 0)
bw, bx = 250, W - M - 250; y -= 18
rows = [('Total à payer', F(tot), '#1F2A44')]
if ac: rows.append((f"Acompte reçu le {spec['acompte']['date']}", '- ' + F(ac), GREEN))
for lab, val, col in rows:
    y -= 24; rrect(bx, y, bw, 24, 0, fill='white', stroke=LINE); txt(bx + 12, y + 8, lab, 9.5, color=col); txt(bx + bw - 12, y + 8, val, 9.5, True, col, right=True)
y -= 30; rrect(bx, y, bw, 30, 5, fill=RED); txt(bx + 12, y + 10, 'Reste à payer', 12, True, 'white'); txt(bx + bw - 12, y + 10, F(tot - ac), 12, True, 'white', right=True)
# conditions
y -= 30; txt(M, y, 'CONDITIONS', 7.5, True, RED)
for cnd in spec.get('conditions', []):
    y -= 14; txt(M + 6, y, '•  ' + cnd, 9)
# signature + pied
c.drawImage(img(sig_p, (240, 240), jpeg=True), W - M - 190, 92, 150, 77)
c.setStrokeColor(NAVY); c.setLineWidth(0.8); c.line(W - M - 200, 88, W - M - 30, 88)
c.setFillColor(NAVY); c.setFont('Helvetica', 8.5); c.drawCentredString(W - M - 115, 76, 'Vremen Hermann — Digital-Ivoire'); c.drawCentredString(W - M - 115, 65, '+225 05 74 99 96 75')
txt(M, 76, 'Montants en francs CFA (XOF).', 7.5, italic=True, color='#7A849C')
c.setStrokeColor(LINE); c.line(M, 52, W - M, 52)
c.setFillColor('#7A849C'); c.setFont('Helvetica', 7.5); c.drawCentredString(W / 2, 40, f"Digital-Ivoire — Facture {spec['numero']} — {cl['nom']}")
c.showPage(); c.save(); print('ok', out)
