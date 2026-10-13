// Génère une proforma VREMAX en PDF à partir d'un fichier JSON.
// Usage : node make.cjs spec.json sortie.pdf
// Prérequis (une fois, dans ce dossier) : npm i  (playwright + polices)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = process.argv[3] || 'proforma.pdf';
const NM = path.join(__dirname, 'node_modules', '@fontsource');
const font = (fam, dir, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(file://${NM}/${dir}/files/${dir}-latin-${w}-normal.woff2)}`;
const FF = [400, 500, 600, 700, 800].map(w => font('Hanken Grotesk', 'hanken-grotesk', w)).join('') + [600, 700].map(w => font('Fraunces', 'fraunces', w)).join('');
const E = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const F = n => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' F';
const logo = fs.existsSync(path.join(__dirname, 'logo.png')) ? 'file://' + path.join(__dirname, 'logo.png') : '';

// spec : { numero, date, validite_jours, client:{nom, ville?, contact?, email?}, objet,
//          type:"modules"|"estimation", formules:[{nom, lignes:[...], prix, abonnement_an?}],
//          fourchette?:{min,max, postes:[...]}, paiement, notes:[...] }
const formules = (spec.formules || []).map(f => `
  <div class="fo"><div class="fn">${E(f.nom)}</div>
  <ul>${(f.lignes || []).map(l => `<li>${E(l)}</li>`).join('')}</ul>
  <div class="fp">${F(f.prix)}<span>mise en place</span></div>
  ${f.abonnement_an ? `<div class="fa">+ ${F(f.abonnement_an)} / an : hébergement, maintenance, mises à jour</div>` : ''}</div>`).join('');
const estim = spec.fourchette ? `
  <div class="es"><div class="el">Estimation budgétaire indicative</div>
  <div class="ev">${F(spec.fourchette.min)} à ${F(spec.fourchette.max)}</div>
  <ul>${(spec.fourchette.postes || []).map(l => `<li>${E(l)}</li>`).join('')}</ul>
  <div class="en">Fourchette établie sur la base des informations transmises. Le montant définitif est fixé dans la proforma remise après la rencontre et l'analyse de votre organisation.</div></div>` : '';
const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>${FF}
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Hanken Grotesk';color:#14201A}
.pg{width:210mm;min-height:297mm;background:#fff;display:flex;flex-direction:column}
.hd{background:#14201A;color:#fff;padding:26px 44px;display:flex;justify-content:space-between;align-items:center}
.br{display:flex;align-items:center;gap:12px}.br img{width:40px;height:40px;border-radius:9px}
.bn{font-family:Fraunces;font-weight:700;font-size:22px;letter-spacing:.2em}.bs{font-size:11px;color:#C9D6CF;margin-top:2px}
.dt{text-align:right}.dt .t{font-family:Fraunces;font-weight:700;font-size:24px;color:#7FD9B3}.dt div{font-size:12px;line-height:1.6}
.bd{padding:26px 44px;flex:1;display:flex;flex-direction:column;gap:18px}
.row{display:flex;gap:16px}.box{flex:1;background:#F6F3EC;border-radius:10px;padding:12px 14px;font-size:12.5px;line-height:1.55}
.lb{font-size:10px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#0F6B57;margin-bottom:4px}
.ob{font-family:Fraunces;font-weight:700;font-size:19px}
.fos{display:flex;gap:16px}.fo{flex:1;border:1.5px solid #0F6B57;border-radius:12px;padding:14px 16px;display:flex;flex-direction:column}
.fn{font-family:Fraunces;font-weight:700;font-size:17px;color:#0F6B57;margin-bottom:6px}
.fo ul,.es ul{margin:0 0 10px;padding-left:17px;font-size:12px;line-height:1.6}
.fp{margin-top:auto;font-family:Fraunces;font-weight:700;font-size:24px}.fp span{font-family:'Hanken Grotesk';font-size:11px;font-weight:600;color:#3E4B44;margin-left:6px}
.fa{font-size:11.5px;color:#3E4B44;margin-top:4px}
.es{border:1.5px solid #0F6B57;border-radius:12px;padding:16px}.el{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#0F6B57}
.ev{font-family:Fraunces;font-weight:700;font-size:28px;margin:6px 0 10px}.en{font-size:11.5px;color:#3E4B44}
.cd{font-size:12px;line-height:1.6}.cd li{margin-bottom:2px}
.ft{background:#0F6B57;color:#fff;padding:14px 44px;display:flex;justify-content:space-between;font-size:11.5px;font-weight:600}
</style></head><body><div class="pg">
<div class="hd"><div class="br">${logo ? `<img src="${logo}">` : ''}<div><div class="bn">VREMAX</div><div class="bs">Digital-Ivoire · Abidjan, Cocody Riviera Akouédo</div></div></div>
<div class="dt"><div class="t">${spec.type === 'estimation' ? 'ESTIMATION' : 'PROFORMA'}</div><div>N° ${E(spec.numero)}</div><div>Date : ${E(spec.date)}</div><div>Validité : ${E(spec.validite_jours || 30)} jours</div></div></div>
<div class="bd">
<div class="row"><div class="box"><div class="lb">Client</div><b>${E(spec.client.nom)}</b>${spec.client.ville ? `<br>${E(spec.client.ville)}` : ''}${spec.client.contact ? `<br>${E(spec.client.contact)}` : ''}${spec.client.email ? `<br>${E(spec.client.email)}` : ''}</div>
<div class="box"><div class="lb">Émetteur</div><b>Digital-Ivoire — VREMAX</b><br>+225 05 74 99 96 75<br>hello@vremaxx.com · www.vremaxx.com</div></div>
<div><div class="lb">Objet</div><div class="ob">${E(spec.objet)}</div></div>
${formules ? `<div class="fos">${formules}</div>` : ''}${estim}
<div class="cd"><div class="lb">Conditions</div><ul>
<li>Paiement : ${E(spec.paiement || '70 % à la commande, 30 % à la livraison.')}</li>
<li>Inclus : paramétrage selon vos règles, reprise de vos données existantes, formation de vos équipes.</li>
<li>Accès sur ordinateur, tablette et téléphone, depuis le navigateur.</li>
${(spec.notes || []).map(n => `<li>${E(n)}</li>`).join('')}
<li>Montants en francs CFA.</li></ul></div>
</div>
<div class="ft"><div>Notre équipe se déplace pour vous présenter la solution.</div><div>+225 05 74 99 96 75 · hello@vremaxx.com</div></div>
</div></body></html>`;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage();
  const tmp = path.join(path.dirname(path.resolve(out)), '.proforma_tmp.html');
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await b.close(); fs.unlinkSync(tmp); console.log('ok', out);
})();
