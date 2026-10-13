// Génère une proforma / estimation Digital-Ivoire (style maison) en PDF à partir d'un JSON.
// Usage : node make.cjs spec.json sortie.pdf [signature.png]
// Prérequis (une fois, dans ce dossier) : PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm i
// La signature + cachet n'est PAS dans le dépôt : la récupérer depuis le doc projet
// "claude/digital-ivoire-signature-b64.txt" (base64 PNG) et passer le chemin en 3e argument.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(process.argv[3] || 'proforma.pdf');
const sig = process.argv[4] && fs.existsSync(process.argv[4]) ? 'file://' + path.resolve(process.argv[4]) : '';
const logo = 'file://' + path.join(__dirname, 'logo-digital-ivoire.png');
const E = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const F = n => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' F';
const isEst = spec.type === 'estimation';
const docLabel = isEst ? 'ESTIMATION' : 'PROFORMA';

const opts = (spec.formules || []).map((f, i, a) => {
  const reco = f.recommande || (a.length > 1 && i === a.length - 1);
  return `<div class="op${reco ? ' reco' : ''}">
  <div class="oh"><div class="ok">${reco ? 'RECOMMANDÉ' : 'FORMULE ' + String.fromCharCode(65 + i)}</div><div class="on">${E(f.nom)}</div></div>
  <div class="ob"><div class="opx">${F(f.prix)}</div><div class="os">${E(f.sous_titre || 'Mise en place')}</div>
  <ul>${(f.lignes || []).map(l => `<li>${E(l)}</li>`).join('')}</ul></div></div>`;
}).join('');

const rows = (spec.lignes_tableau || (spec.formules || []).flatMap(f => [
  [f.nom + ' — mise en place', 'Paramétrage, reprise des données, formation', F(f.prix)],
  ...(f.abonnement_an ? [[f.nom + ' — abonnement annuel', 'Hébergement, maintenance, mises à jour', F(f.abonnement_an) + ' / an']] : [])
])).map(r => `<tr><td>${E(r[0])}</td><td>${E(r[1])}</td><td class="r"><b>${E(r[2])}</b></td></tr>`).join('');

const estim = isEst && spec.fourchette ? `
<div class="est"><div class="el">Budget estimé</div><div class="ev">${F(spec.fourchette.min)} à ${F(spec.fourchette.max)}</div>
<div class="en">Fourchette indicative établie à partir des informations transmises. Le montant définitif sera fixé dans la proforma remise après la rencontre et l'analyse détaillée de votre organisation.</div></div>
<table><tr><th>Poste</th><th>Contenu</th></tr>${(spec.fourchette.postes || []).map(p => Array.isArray(p) ? `<tr><td>${E(p[0])}</td><td>${E(p[1])}</td></tr>` : `<tr><td colspan="2">${E(p)}</td></tr>`).join('')}</table>` : '';

const reco = spec.recommandation ? `<div class="rb"><b>Notre recommandation :</b> ${E(spec.recommandation)}</div>` : '';
const intro = spec.intro ? `<div class="in">${E(spec.intro)}</div>` : '';

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@page{size:A4;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:Arial,'Liberation Sans',Helvetica,sans-serif;color:#1F2A44;font-size:12px}
.pg{width:210mm;height:296mm;overflow:hidden;padding:30px 46px 20px;display:flex;flex-direction:column}
.hd{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:12px;border-bottom:3px solid #1E2A5E}
.id{display:flex;gap:14px;align-items:flex-start}.id img{width:64px;height:64px;border-radius:50%}
.co{font-size:21px;font-weight:700;color:#1E2A5E}.tg{font-size:9.5px;letter-spacing:.14em;color:#55607A;margin:4px 0 3px}
.ad{font-size:10px;color:#55607A;line-height:1.5}
.nb{background:#1E2A5E;color:#fff;border-radius:8px;padding:10px 14px;text-align:right}
.nb .t{font-weight:700;font-size:14px;letter-spacing:.06em}.nb div{font-size:10.5px;line-height:1.6}
.band{margin-top:14px;background:#1E2A5E;color:#fff;border-radius:10px;padding:16px 18px}
.band .h{font-size:19px;font-weight:700}.band .s{font-size:11.5px;color:#C9D1EC;margin-top:5px}
.two{display:flex;gap:18px;margin-top:12px}.two>div{flex:1}
.lb{font-size:9.5px;font-weight:700;letter-spacing:.14em;color:#D93A2B;margin-bottom:5px}
.bx{border:1px solid #DCE1EF;border-left:4px solid #1E2A5E;border-radius:6px;padding:9px 12px;line-height:1.55;background:#F7F8FC;min-height:56px}
.in{margin-top:14px;border:1px solid #C9D1EC;background:#F3F5FB;border-radius:8px;padding:10px 14px;line-height:1.55}
.sec{margin-top:12px;font-size:11px;font-weight:700;letter-spacing:.12em;color:#D93A2B;border-bottom:1px solid #DCE1EF;padding-bottom:5px}
.ops{display:flex;gap:12px;margin-top:10px}
.op{flex:1;border:1px solid #DCE1EF;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.op.reco{border:2px solid #D93A2B}
.oh{background:#F3F5FB;padding:9px 12px}.op.reco .oh{background:#1E2A5E;color:#fff}
.ok{font-size:9px;font-weight:700;letter-spacing:.14em;color:#D93A2B}.op.reco .ok{color:#C9D1EC}
.on{font-size:15px;font-weight:700;margin-top:3px}
.ob{padding:10px 12px}.opx{font-size:20px;font-weight:700;color:#1E2A5E}.op.reco .opx{color:#D93A2B}
.os{font-size:10px;color:#55607A;margin:2px 0 6px}
.ob ul{margin:0;padding:0;list-style:none}.ob li{padding-left:15px;position:relative;line-height:1.5;font-size:11px}
.ob li:before{content:'\\2713';position:absolute;left:0;color:#1E9E5B;font-weight:700}
.rb{margin-top:12px;background:#1E2A5E;color:#fff;border-radius:8px;padding:10px 14px;line-height:1.5}.rb b{color:#F5A623}
table{width:100%;border-collapse:collapse;margin-top:10px}th{background:#1E2A5E;color:#fff;text-align:left;font-size:10.5px;padding:7px 10px}
td{padding:5px 10px;border-bottom:1px solid #DCE1EF;font-size:11px}tr:nth-child(even) td{background:#F7F8FC}.r{text-align:right}
.est{margin-top:10px;border:2px solid #D93A2B;border-radius:10px;padding:12px 14px}
.el{font-size:9.5px;font-weight:700;letter-spacing:.14em;color:#D93A2B}.ev{font-size:22px;font-weight:700;color:#1E2A5E;margin:4px 0 6px}
.en{font-size:10.5px;color:#55607A;line-height:1.5}
.cond{display:flex;gap:18px;margin-top:10px}.cond>div{flex:1;line-height:1.55;font-size:11px}
.cond ul{margin:4px 0 0;padding-left:16px}
.sg{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;padding-top:14px}
.nt{font-size:9.5px;color:#7A849C;font-style:italic;max-width:300px;line-height:1.5}
.sgn{text-align:center;font-size:10.5px;color:#1E2A5E}.sgn img{height:74px;display:block;margin:0 auto -6px}
.sgn .ln{border-top:1px solid #1E2A5E;padding-top:4px;min-width:200px}
.ft{text-align:center;font-size:9.5px;color:#7A849C;border-top:1px solid #DCE1EF;margin-top:10px;padding-top:6px}.ft b{color:#1E2A5E}
</style></head><body><div class="pg">
<div class="hd"><div class="id"><img src="${logo}"><div><div class="co">Digital - Ivoire</div><div class="tg">COMMUNICATION MARKETING &amp; GESTION</div>
<div class="ad">Abidjan, Côte d'Ivoire<br>Tél : +225 05 74 99 96 75 • hello@vremaxx.com • www.vremaxx.com</div></div></div>
<div class="nb"><div class="t">${docLabel}</div><div>N° ${E(spec.numero)}</div><div>Abidjan, le ${E(spec.date)}</div></div></div>
<div class="band"><div class="h">${E(spec.titre || spec.objet)}</div>${spec.sous_titre ? `<div class="s">${E(spec.sous_titre)}</div>` : ''}</div>
<div class="two"><div><div class="lb">CLIENT</div><div class="bx"><b>${E(spec.client.nom)}</b>${spec.client.activite ? `<br>${E(spec.client.activite)}` : ''}${spec.client.ville ? `<br>${E(spec.client.ville)}` : ''}${spec.client.contact ? `<br>${E(spec.client.contact)}` : ''}${spec.client.email ? `<br>${E(spec.client.email)}` : ''}</div></div>
<div><div class="lb">OBJET</div><div class="bx">${E(spec.objet)}</div></div></div>
${intro}
${isEst ? `<div class="sec">1 — ESTIMATION BUDGÉTAIRE</div>${estim}` : `<div class="sec">1 — NOS FORMULES</div><div class="ops">${opts}</div>${reco}<div class="sec">2 — DÉTAIL</div><table><tr><th>Élément</th><th>Détail</th><th class="r">Coût</th></tr>${rows}</table>`}
<div class="cond"><div><div class="lb">CONDITIONS</div><ul>
<li>Paiement : ${E(spec.paiement || '70 % à la commande, 30 % à la livraison.')}</li>
<li>Inclus : paramétrage selon vos règles, reprise de vos données, formation de vos équipes.</li>
<li>Accès sur ordinateur, tablette et téléphone.</li>${(spec.notes || []).map(n => `<li>${E(n)}</li>`).join('')}</ul></div>
<div><div class="lb">PROCHAINE ÉTAPE</div>${E(spec.prochaine_etape || (isEst ? "Une rencontre avec notre équipe, sur place ou en visio, pour analyser votre organisation en détail. Vous recevez ensuite la proforma définitive." : "Dès votre accord et le règlement de l'acompte, nous lançons le paramétrage. Notre équipe peut aussi venir vous présenter la solution avant de démarrer."))}</div></div>
<div class="sg"><div class="nt">${isEst ? 'Estimation' : 'Proforma'} valable ${E(spec.validite_jours || 30)} jours. Montants en francs CFA (XOF).</div>
<div class="sgn">${sig ? `<img src="${sig}">` : ''}<div class="ln">Vremen Hermann — Digital-Ivoire<br>+225 05 74 99 96 75</div></div></div>
<div class="ft"><b>Digital-Ivoire</b> — ${docLabel === 'PROFORMA' ? 'Proforma' : 'Estimation'} ${E(spec.client.nom)}</div>
</div></body></html>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage();
  const tmp = path.join(path.dirname(out), '.proforma_tmp.html');
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp);
  await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await b.close(); fs.unlinkSync(tmp); console.log('ok', out);
})();
