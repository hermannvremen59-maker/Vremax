# Email pro VREMAX (HTML + texte), à l'image de la marque.
# Usage : python3 make_email.py spec.json sortie_prefix
# spec.json :
#   "titre"        : accroche du bandeau (courte, 4 à 9 mots), ex. "Votre gestion locative tourne toute seule."
#   "paragraphes"  : 2 ou 3 paragraphes courts (sans "Bonjour," ni signature : le modèle les ajoute)
#   "automatismes" : 3 ou 4 éléments [["Libellé court", "ce qui se fait tout seul, une ligne"], ...]
#                    = ce que VREMAX automatise pour CE prospect (uniquement des fonctions réelles)
#   "appel"        : phrase d'action (encadré), optionnelle
#   "bouton"       : texte du bouton (défaut "Découvrir VREMAX"), lien fixe https://www.vremaxx.com
#   "stop"         : true pour un premier email (ligne STOP), false pour une réponse / relance
# Produit <prefix>.html (htmlBody) et <prefix>.txt (body). Pièce jointe inline obligatoire :
#   {"filename":"logo-vremax.png","mimeType":"image/png","inline":true,"content":<base64 de logo-vremax-96.png>}
import json, sys, html
spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
E = html.escape
INK, JADE, JADE_D, MINT, PAPER, SOFT = '#14201A', '#0F6B57', '#0A5042', '#7FD9B3', '#F6F3EC', '#E4EFE8'
titre = spec.get('titre') or "Votre gestion, enfin automatisée."
P = spec.get('paragraphes', [])
auto = spec.get('automatismes') or []
appel = spec.get('appel'); bouton = spec.get('bouton') or 'Découvrir VREMAX'; stop = spec.get('stop', True)
FONT = "Arial,Helvetica,sans-serif"; SERIF = "Georgia,'Times New Roman',serif"

paras = ''.join(f'<p style="margin:0 0 16px">{E(p)}</p>' for p in P)
auto_h = ''
if auto:
    rows = ''.join(f'''<tr><td style="padding:9px 0;vertical-align:top;width:34px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="width:24px;height:24px;background:{JADE};border-radius:12px;color:#FFFFFF;font-size:13px;font-weight:bold;text-align:center;line-height:24px">&#10003;</td></tr></table></td>
<td style="padding:9px 0;vertical-align:top;font-size:14px;line-height:1.5;color:{INK}"><b>{E(a)}</b><br><span style="color:#3E4B44">{E(b)}</span></td></tr>''' for a, b in auto)
    auto_h = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 20px;background:{PAPER};border-radius:12px"><tr><td style="padding:18px 20px 10px">
<div style="font-size:11px;font-weight:bold;letter-spacing:2px;color:{JADE};text-transform:uppercase;margin-bottom:4px">Ce que VREMAX fait tout seul pour vous</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{rows}</table></td></tr></table>'''
appel_h = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 22px"><tr><td style="background:{SOFT};border-left:4px solid {JADE};border-radius:0 8px 8px 0;padding:14px 18px;color:{JADE_D};font-size:15px;font-weight:bold;line-height:1.5">{E(appel)}</td></tr></table>''' if appel else ''
# Pas de balise <a> : Gmail affiche un avertissement de redirection sur les liens HTML.
# On écrit l'adresse en texte ; Gmail la rend cliquable lui-même (testé : ouverture directe).
btn = f'''<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto 8px"><tr><td align="center" bgcolor="{JADE}" style="border-radius:28px;background:{JADE};padding:14px 30px;font-family:{FONT};font-size:15px;font-weight:bold;color:#FFFFFF">
{E(bouton)} &nbsp;&rarr;&nbsp; <span style="color:#FFFFFF">www.vremaxx.com</span></td></tr></table>
<p style="margin:0 0 6px;text-align:center;font-size:12px;color:#6B776F">ou répondez simplement à cet email</p>'''
stop_h = f'<p style="margin:10px 0 0;font-size:11px;color:#8FA197;line-height:1.5">Si vous ne souhaitez plus recevoir de message de ma part, répondez simplement STOP.</p>' if stop else ''

h = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:{PAPER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}"><tr><td align="center" style="padding:22px 10px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#FFFFFF;border-radius:14px;overflow:hidden;font-family:{FONT};color:{INK};box-shadow:0 6px 24px rgba(20,32,26,.08)">
<tr><td style="background:{INK};padding:18px 26px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="vertical-align:middle;width:46px"><img src="cid:logo-vremax.png" width="42" height="42" alt="VREMAX" style="display:block;border-radius:10px"></td>
<td style="vertical-align:middle;padding-left:12px;color:#FFFFFF;font-family:{SERIF};font-size:21px;font-weight:bold;letter-spacing:5px">VREMAX</td>
<td align="right" style="vertical-align:middle"><span style="display:inline-block;background:#3DBE8B;color:{INK};font-size:10px;font-weight:bold;letter-spacing:2px;padding:6px 10px;border-radius:6px">AUTOMATISATION</span></td>
</tr></table></td></tr>
<tr><td style="background:{JADE};padding:28px 26px 26px">
<div style="font-size:11px;font-weight:bold;letter-spacing:2px;color:{MINT};text-transform:uppercase;margin-bottom:10px">La gestion qui travaille pour vous</div>
<div style="font-family:{SERIF};font-size:27px;line-height:1.2;font-weight:bold;color:#FFFFFF">{E(titre)}</div>
</td></tr>
<tr><td style="padding:28px 28px 6px;font-size:15px;line-height:1.65">
<p style="margin:0 0 16px">Bonjour,</p>{paras}{auto_h}{appel_h}{btn}
</td></tr>
<tr><td style="padding:18px 28px 24px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #DDE5E0"><tr><td style="padding-top:16px;font-size:14px;line-height:1.55">
<p style="margin:0 0 10px">Bien cordialement,</p>
<b style="font-size:15px;color:{INK}">Hermann VREMEN</b><br><span style="color:{JADE}">Fondateur, VREMAX &middot; Digital-Ivoire</span><br>
<span style="color:#3E4B44">+225 05 74 99 96 75 &nbsp;&middot;&nbsp; hello&#8288;@vremaxx&#8288;.com</span></td></tr></table></td></tr>
<tr><td style="background:{INK};padding:16px 28px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="color:{MINT};font-family:{SERIF};font-size:14px;font-weight:bold">Moins de saisie. Plus de contrôle.</td>
<td align="right" style="color:#9FB3A8;font-size:11px">Abidjan, Côte d&#39;Ivoire</td></tr></table>
{stop_h}</td></tr>
</table></td></tr></table></body></html>'''

t = 'Bonjour,\n\n' + '\n\n'.join(P)
if auto:
    t += '\n\nCe que VREMAX fait tout seul pour vous :\n' + '\n'.join(f'- {a} : {b}' for a, b in auto)
if appel: t += f'\n\n{appel}'
t += '\n\nDécouvrir VREMAX : www.vremaxx.com\n\nBien cordialement,\n\nHermann VREMEN\nFondateur, VREMAX - Digital-Ivoire\n+225 05 74 99 96 75'
if stop: t += '\n\nSi vous ne souhaitez plus recevoir de message de ma part, répondez simplement STOP.'
open(out + '.html', 'w', encoding='utf-8').write(h); open(out + '.txt', 'w', encoding='utf-8').write(t)
print('ok', out + '.html', out + '.txt')
