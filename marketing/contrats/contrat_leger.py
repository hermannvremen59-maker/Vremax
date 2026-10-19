# Version PDF LÉGÈRE d'un contrat HTML (polices standard non embarquées) pour l'envoyer par e-mail.
# Usage : python3 contrat_leger.py contrat.html sortie.pdf logo.png "texte pied de page"
from reportlab import rl_config; rl_config.useA85 = 0
import sys, io, re
from bs4 import BeautifulSoup
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.utils import ImageReader

src, out, logo_p, foot = sys.argv[1:5]
NAVY, GREY, LINE, SOFT = colors.HexColor('#1E2A5E'), colors.HexColor('#55607A'), colors.HexColor('#DCE1EF'), colors.HexColor('#F7F8FC')
INK = colors.HexColor('#1F2A44')
im = Image.open(logo_p).convert('RGBA'); im.thumbnail((90, 90))
bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); b = io.BytesIO(); bg.save(b, 'JPEG', quality=70); b.seek(0)
LOGO = ImageReader(b)

base = dict(fontName='Helvetica', fontSize=9.2, leading=13, textColor=INK)
S = {
 'h1': ParagraphStyle('h1', **{**base, 'fontName': 'Helvetica-Bold', 'fontSize': 13.5, 'leading': 18, 'textColor': NAVY, 'alignment': 1}),
 'ref': ParagraphStyle('ref', **{**base, 'fontSize': 8.6, 'textColor': GREY, 'alignment': 1, 'spaceAfter': 8}),
 'h2': ParagraphStyle('h2', keepWithNext=1, **{**base, 'fontName': 'Helvetica-Bold', 'fontSize': 9.6, 'textColor': NAVY, 'spaceBefore': 9, 'spaceAfter': 4}),
 'h3': ParagraphStyle('h3', keepWithNext=1, **{**base, 'fontName': 'Helvetica-Bold', 'fontSize': 9.2, 'textColor': NAVY, 'spaceBefore': 4, 'spaceAfter': 1}),
 'p': ParagraphStyle('p', **{**base, 'alignment': 4, 'spaceAfter': 4}),
 'c': ParagraphStyle('c', **{**base, 'alignment': 1, 'fontName': 'Helvetica-Bold', 'spaceAfter': 3, 'spaceBefore': 3}),
 'td': ParagraphStyle('td', **{**base, 'fontSize': 8.6, 'leading': 11.5}),
 'th': ParagraphStyle('th', **{**base, 'fontSize': 8.6, 'leading': 11.5, 'fontName': 'Helvetica-Bold', 'textColor': colors.white}),
 'band': ParagraphStyle('band', **{**base, 'fontName': 'Helvetica-Bold', 'fontSize': 10.5, 'textColor': colors.white, 'alignment': 1}),
}

def inline(el):
    h = ''
    for c in el.children:
        if isinstance(c, str):
            h += c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        elif c.name in ('b', 'strong'):
            h += '<b>' + inline(c) + '</b>'
        elif c.name == 'br':
            h += '<br/>'
        elif c.name == 'div':
            h += '<b>' + inline(c) + '</b><br/>'
        else:
            h += inline(c)
    return re.sub(r'\s+', ' ', h).strip()

soup = BeautifulSoup(open(src, encoding='utf-8').read(), 'html.parser')
story = []
W = A4[0] - 40 * mm

def table(el):
    rows = []
    for tr in el.find_all('tr'):
        cells = tr.find_all(['th', 'td'])
        row = [Paragraph(inline(c), S['th'] if c.name == 'th' else S['td']) for c in cells]
        if len(cells) == 1 or (cells and cells[0].get('colspan')):
            row = row + [''] * (3 - len(row))
        rows.append(row)
    n = max(len(r) for r in rows)
    hdr = el.find('tr').get_text(' ')
    widths = {2: [W * .5, W * .5], 3: ([W * .2, W * .16, W * .64] if 'Contenu' in hdr else [W * .3, W * .45, W * .25])}.get(n, [W / n] * n)
    t = Table(rows, colWidths=widths, repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('LINEBELOW', (0, 0), (-1, -1), .5, LINE),
          ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    for i in range(2, len(rows), 2): st.append(('BACKGROUND', (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(st)); return t

def boxed(par):
    t = Table([[par]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SOFT), ('BOX', (0, 0), (-1, -1), .5, LINE),
                           ('LINEBEFORE', (0, 0), (0, -1), 3, NAVY), ('LEFTPADDING', (0, 0), (-1, -1), 9),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return t

def walk(node):
    for el in node.children:
        if isinstance(el, str) or el.name is None: continue
        cls = el.get('class') or []
        if el.name == 'h1': story.append(Paragraph(inline(el), S['h1']))
        elif el.name == 'h2': story.append(Paragraph(inline(el).upper(), S['h2']))
        elif el.name == 'h3': story.append(Paragraph(inline(el), S['h3']))
        elif el.name == 'p':
            st = S['c'] if 'center' in (el.get('style') or '') else S['p']
            story.append(Paragraph(inline(el), st))
        elif el.name in ('ul', 'ol'):
            items = [ListItem(Paragraph(inline(li), S['p']), leftIndent=12) for li in el.find_all('li', recursive=False)]
            story.append(ListFlowable(items, bulletType='1' if el.name == 'ol' else 'bullet', start='1' if el.name == 'ol' else None,
                                      bulletFontSize=8, leftIndent=12, bulletFontName='Helvetica'))
        elif el.name == 'table': story.append(table(el))
        elif el.name == 'div' and 'ref' in cls: story.append(Paragraph(inline(el), S['ref']))
        elif el.name == 'div' and 'band' in cls:
            t = Table([[Paragraph(inline(el.find('b')), S['band'])]], colWidths=[W])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NAVY), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
            story.extend([t, Spacer(1, 6)])
        elif el.name == 'div' and 'party' in cls: story.append(boxed(Paragraph(inline(el), S['p'])))
        elif el.name == 'div' and 'sig' in cls:
            cols = []
            for d in el.find_all('div', recursive=False):
                cols.append(Paragraph(inline(d), S['td']))
            t = Table([cols], colWidths=[W / 2 - 4, W / 2 - 4], rowHeights=[38 * mm])
            t.setStyle(TableStyle([('BOX', (0, 0), (0, 0), .6, LINE), ('BOX', (1, 0), (1, 0), .6, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                   ('TOPPADDING', (0, 0), (-1, -1), 7), ('LEFTPADDING', (0, 0), (-1, -1), 8)]))
            story.append(t)
        elif el.name == 'div':
            sub = []; story_len = len(story); walk(el)
            if 'page-break-inside:avoid' in (el.get('style') or ''):
                grp = story[story_len:]; del story[story_len:]; story.append(KeepTogether(grp))
walk(soup.body)

def page(c, d):
    c.saveState()
    y = A4[1] - 14 * mm
    c.drawImage(LOGO, 20 * mm, y - 11 * mm, 12 * mm, 12 * mm)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 12); c.drawString(34 * mm, y - 4 * mm, 'Digital - Ivoire')
    c.setFillColor(GREY); c.setFont('Helvetica', 6.5); c.drawString(34 * mm, y - 8 * mm, 'COMMUNICATION MARKETING & GESTION')
    c.drawRightString(A4[0] - 20 * mm, y - 4 * mm, "Abidjan, Côte d'Ivoire")
    c.drawRightString(A4[0] - 20 * mm, y - 8 * mm, '+225 05 74 99 96 75 • hello@vremaxx.com • www.vremaxx.com')
    c.setStrokeColor(NAVY); c.setLineWidth(1.5); c.line(20 * mm, y - 13 * mm, A4[0] - 20 * mm, y - 13 * mm)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    c.setFillColor(GREY); c.setFont('Helvetica', 6.8)
    c.drawString(20 * mm, 11 * mm, foot); c.drawCentredString(A4[0] / 2 + 15 * mm, 11 * mm, 'Paraphes : ______ / ______')
    c.drawRightString(A4[0] - 20 * mm, 11 * mm, 'Page %d' % d.page)
    c.restoreState()

doc = BaseDocTemplate(out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=34 * mm, bottomMargin=22 * mm,
                      title='Contrat ' + foot, author='Digital-Ivoire', pageCompression=1)
doc.addPageTemplates([PageTemplate(frames=[Frame(20 * mm, 22 * mm, W, A4[1] - 56 * mm, id='f')], onPage=page)])
doc.build(story); print('ok', out)
