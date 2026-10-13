# Email pro VREMAX (HTML + texte) — usage :
#   python3 make_email.py spec.json sortie_prefix
# spec.json : {"paragraphes": ["...", "..."], "points": ["...", "..."] (optionnel, liste à puces après le 2e paragraphe),
#              "appel": "phrase d'action finale (optionnel)", "stop": true/false (ligne STOP pour un premier email)}
# Produit <prefix>.html (htmlBody), <prefix>.txt (body texte) et rappelle la pièce jointe inline :
#   attachments=[{"filename":"logo-vremax.png","mimeType":"image/png","inline":true,"content":<base64 de logo-vremax-96.png>}]
# Le HTML référence l'image par cid:logo-vremax.png. Un seul lien, propre : le site s'affiche simplement « www.vremaxx.com ». L'email est écrit
# avec un caractère invisible pour ne pas devenir un lien.
import json, sys, html
spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
E = html.escape
SITE_H = '<a href="https://www.vremaxx.com" style="color:#0F6B57;text-decoration:none">www.vremaxx.com</a>'
MAIL_H = 'hello&#8288;@vremaxx&#8288;.com'
P = spec['paragraphes']; pts = spec.get('points') or []; appel = spec.get('appel'); stop = spec.get('stop', True)
ps = ''.join(f'<p style="margin:0 0 14px">{E(p)}</p>' for p in P[:2])
if pts:
    ps += '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 14px">' + ''.join(
        f'<tr><td style="vertical-align:top;padding:3px 10px 3px 0;color:#0F6B57;font-weight:bold">&#8226;</td><td style="padding:3px 0">{E(x)}</td></tr>' for x in pts) + '</table>'
ps += ''.join(f'<p style="margin:0 0 14px">{E(p)}</p>' for p in P[2:])
if appel:
    ps += f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:6px 0 18px"><tr><td style="background:#E4EFE8;border-left:4px solid #0F6B57;padding:12px 16px;color:#0A5042;font-weight:bold">{E(appel)}</td></tr></table>'
stop_h = '<p style="margin:14px 0 0;font-size:11px;color:#8A948E">Si vous ne souhaitez plus recevoir de message de ma part, répondez simplement STOP.</p>' if stop else ''
h = f'''<!doctype html><html lang="fr"><body style="margin:0;padding:0;background:#F6F3EC">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F6F3EC"><tr><td align="center" style="padding:20px 10px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#FFFFFF;border-radius:10px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#14201A">
<tr><td style="background:#14201A;padding:16px 24px"><table role="presentation" cellpadding="0" cellspacing="0"><tr>
<td style="vertical-align:middle"><img src="cid:logo-vremax.png" width="40" height="40" alt="VREMAX" style="display:block;border-radius:8px"></td>
<td style="vertical-align:middle;padding-left:12px;color:#FFFFFF;font-family:Georgia,serif;font-size:20px;font-weight:bold;letter-spacing:4px">VREMAX</td>
<td style="vertical-align:middle;padding-left:12px;color:#7FD9B3;font-size:12px">Digital-Ivoire &middot; Abidjan</td></tr></table></td></tr>
<tr><td style="height:4px;background:#0F6B57;font-size:0;line-height:0">&nbsp;</td></tr>
<tr><td style="padding:26px 28px 8px;font-size:15px;line-height:1.6"><p style="margin:0 0 14px">Bonjour,</p>{ps}
<p style="margin:0 0 4px">Bien cordialement,</p></td></tr>
<tr><td style="padding:6px 28px 24px"><table role="presentation" cellpadding="0" cellspacing="0" style="border-top:1px solid #DDE5E0;padding-top:12px;width:100%"><tr><td style="padding-top:12px;font-size:14px;line-height:1.5">
<b style="color:#14201A">Hermann VREMEN</b><br><span style="color:#0F6B57">Fondateur, VREMAX (Digital-Ivoire)</span><br>
<span style="color:#3E4B44">+225 05 74 99 96 75<br>{MAIL_H}<br>{SITE_H}</span></td></tr></table>{stop_h}</td></tr>
</table></td></tr></table></body></html>'''
t = 'Bonjour,\n\n' + '\n\n'.join(P[:2]) + ('\n\n' + '\n'.join('- ' + x for x in pts) if pts else '') + \
    ''.join('\n\n' + p for p in P[2:]) + (f'\n\n{appel}' if appel else '') + \
    '\n\nBien cordialement,\n\nHermann VREMEN\nFondateur, VREMAX (Digital-Ivoire)\n+225 05 74 99 96 75' + \
    ('\n\nSi vous ne souhaitez plus recevoir de message de ma part, répondez simplement STOP.' if stop else '')
open(out + '.html', 'w', encoding='utf-8').write(h); open(out + '.txt', 'w', encoding='utf-8').write(t)
print('ok', out + '.html', out + '.txt')
