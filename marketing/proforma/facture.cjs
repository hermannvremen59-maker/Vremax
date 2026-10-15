// Génère une FACTURE Digital-Ivoire (style maison, même charte que make.cjs) en PDF à partir d'un JSON.
// Usage : node facture.cjs spec.json sortie.pdf [signature.png]
// spec : numero, date, client{nom,activite,email}, objet, lignes[[designation,detail,montant|texte]],
//        total, acompte{montant,date}, conditions[], notes[]
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(process.argv[3] || 'facture.pdf');
const sig = process.argv[4] && fs.existsSync(process.argv[4]) ? 'file://' + path.resolve(process.argv[4]) : '';
const logo = 'file://' + (process.env.LOGO || path.join(__dirname, 'logo-digital-ivoire.png'));
const E = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const F = n => Math.round(n).toLocaleString('fr-FR').replace(/[  ]/g, ' ') + ' F';
const total = spec.total, ac = spec.acompte ? spec.acompte.montant : 0, reste = total - ac;
const rows = spec.lignes.map(r => `<tr><td><b>${E(r[0])}</b>${r[1] ? `<div class="d">${E(r[1])}</div>` : ''}</td><td class="r">${typeof r[2] === 'number' ? F(r[2]) : E(r[2])}</td></tr>`).join('');
const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@page{size:A4;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:Arial,'Liberation Sans',Helvetica,sans-serif;color:#1F2A44;font-size:12px}
.pg{width:210mm;height:296mm;overflow:hidden;padding:30px 46px 20px;display:flex;flex-direction:column}
.hd{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:12px;border-bottom:3px solid #1E2A5E}
.id{display:flex;gap:14px;align-items:flex-start}.id img{width:64px;height:64px;border-radius:50%}
.co{font-size:21px;font-weight:700;color:#1E2A5E}.tg{font-size:9.5px;letter-spacing:.14em;color:#55607A;margin:4px 0 3px}
.ad{font-size:10px;color:#55607A;line-height:1.5}
.nb{background:#1E2A5E;color:#fff;border-radius:8px;padding:10px 14px;text-align:right}
.nb .t{font-weight:700;font-size:16px;letter-spacing:.08em}.nb div{font-size:10.5px;line-height:1.6}
.band{margin-top:14px;background:#1E2A5E;color:#fff;border-radius:10px;padding:16px 18px}
.band .h{font-size:19px;font-weight:700}.band .s{font-size:11.5px;color:#C9D1EC;margin-top:5px}
.two{display:flex;gap:18px;margin-top:14px}.two>div{flex:1}
.lb{font-size:9.5px;font-weight:700;letter-spacing:.14em;color:#D93A2B;margin-bottom:5px}
.bx{border:1px solid #DCE1EF;border-left:4px solid #1E2A5E;border-radius:6px;padding:9px 12px;line-height:1.55;background:#F7F8FC;min-height:60px}
.sec{margin-top:16px;font-size:11px;font-weight:700;letter-spacing:.12em;color:#D93A2B;border-bottom:1px solid #DCE1EF;padding-bottom:5px}
table{width:100%;border-collapse:collapse;margin-top:10px}th{background:#1E2A5E;color:#fff;text-align:left;font-size:10.5px;padding:8px 10px}
td{padding:8px 10px;border-bottom:1px solid #DCE1EF;font-size:11.5px;vertical-align:top}tr:nth-child(even) td{background:#F7F8FC}.r{text-align:right;white-space:nowrap}
.d{font-size:10.5px;color:#55607A;margin-top:3px;line-height:1.45}
.tot{margin-top:14px;margin-left:auto;width:330px;border:1px solid #DCE1EF;border-radius:8px;overflow:hidden}
.tot div{display:flex;justify-content:space-between;padding:8px 14px;font-size:12px;border-bottom:1px solid #DCE1EF}
.tot .ac{color:#1E9E5B}.tot .rs{background:#D93A2B;color:#fff;font-size:15px;font-weight:700;border-bottom:none}
.cond{margin-top:16px;line-height:1.6;font-size:11px}.cond ul{margin:4px 0 0;padding-left:16px}
.sg{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;padding-top:14px}
.nt{font-size:9.5px;color:#7A849C;font-style:italic;max-width:300px;line-height:1.5}
.sgn{text-align:center;font-size:10.5px;color:#1E2A5E}.sgn img{height:74px;display:block;margin:0 auto -6px}
.sgn .ln{border-top:1px solid #1E2A5E;padding-top:4px;min-width:200px}
.ft{text-align:center;font-size:9.5px;color:#7A849C;border-top:1px solid #DCE1EF;margin-top:10px;padding-top:6px}.ft b{color:#1E2A5E}
</style></head><body><div class="pg">
<div class="hd"><div class="id"><img src="${logo}"><div><div class="co">Digital - Ivoire</div><div class="tg">COMMUNICATION MARKETING &amp; GESTION</div>
<div class="ad">Abidjan, Côte d'Ivoire<br>Tél : +225 05 74 99 96 75 • hello@vremaxx.com • www.vremaxx.com</div></div></div>
<div class="nb"><div class="t">FACTURE</div><div>N° ${E(spec.numero)}</div><div>Abidjan, le ${E(spec.date)}</div></div></div>
<div class="band"><div class="h">${E(spec.titre)}</div>${spec.sous_titre ? `<div class="s">${E(spec.sous_titre)}</div>` : ''}</div>
<div class="two"><div><div class="lb">FACTURÉ À</div><div class="bx"><b>${E(spec.client.nom)}</b>${spec.client.activite ? `<br>${E(spec.client.activite)}` : ''}${spec.client.email ? `<br>${E(spec.client.email)}` : ''}</div></div>
<div><div class="lb">OBJET</div><div class="bx">${E(spec.objet)}</div></div></div>
<div class="sec">DÉTAIL DE LA FACTURE</div>
<table><tr><th>Désignation</th><th class="r">Montant</th></tr>${rows}</table>
<div class="tot"><div><span>Total à payer</span><b>${F(total)}</b></div>
${ac ? `<div class="ac"><span>Acompte reçu le ${E(spec.acompte.date)}</span><b>− ${F(ac)}</b></div>` : ''}
<div class="rs"><span>Reste à payer</span><span>${F(reste)}</span></div></div>
<div class="cond"><div class="lb">CONDITIONS</div><ul>${(spec.conditions || []).map(c => `<li>${E(c)}</li>`).join('')}</ul></div>
<div class="sg"><div class="nt">Montants en francs CFA (XOF).${(spec.notes || []).map(n => ' ' + E(n)).join('')}</div>
<div class="sgn">${sig ? `<img src="${sig}">` : ''}<div class="ln">Vremen Hermann — Digital-Ivoire<br>+225 05 74 99 96 75</div></div></div>
<div class="ft"><b>Digital-Ivoire</b> — Facture ${E(spec.numero)} — ${E(spec.client.nom)}</div>
</div></body></html>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage();
  const tmp = path.join(path.dirname(out), '.facture_tmp.html');
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp);
  await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await b.close(); fs.unlinkSync(tmp); console.log('ok', out);
})();
