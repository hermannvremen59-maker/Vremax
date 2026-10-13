// Accord d'apporteur d'affaires Digital-Ivoire (à compléter et signer). Usage : node accord.cjs sortie.pdf
const fs=require('fs'),path=require('path');
const {chromium}=require(process.env.PW||'playwright');
const out=path.resolve(process.argv[2]||'accord.pdf');
const logo='file://'+path.join(__dirname,'..','proforma','logo-digital-ivoire.png');
const art=[
['1. Objet',"L'Apporteur présente à Digital-Ivoire des entreprises ou organisations susceptibles d'acquérir ses logiciels et services (modules VREMAX, logiciels et applications sur mesure). Digital-Ivoire mène seule la relation commerciale, la proposition, la réalisation et l'encaissement."],
['2. Enregistrement du client',"L'Apporteur signale chaque client par écrit (hello@vremaxx.com ou WhatsApp au +225 05 74 99 96 75) avec le nom de l'organisation et un contact. Digital-Ivoire confirme par écrit sous 48 heures. Le client n'est pas enregistré s'il est déjà client de Digital-Ivoire ou déjà en discussion avec elle. Un client enregistré est protégé au nom de l'Apporteur pendant 12 mois."],
['3. Commission',"10 % du montant de mise en place effectivement encaissé par Digital-Ivoire auprès du client enregistré, hors abonnements, hébergement, matériel et frais de tiers. La commission est versée dans les 7 jours suivant chaque encaissement, au prorata des sommes reçues, par Mobile Money ou virement. Aucune commission n'est due sur une somme non encaissée."],
['4. Rôle de l\'Apporteur',"L'Apporteur agit en toute indépendance. Il ne peut ni engager Digital-Ivoire, ni annoncer un prix, une remise ou un délai, ni signer ou encaisser en son nom. Il présente Digital-Ivoire de façon loyale, sans promesse de fonctionnalité."],
['5. Confidentialité',"Chaque partie garde confidentielles les informations reçues de l'autre et des clients, pendant la durée de l'accord et deux ans après."],
['6. Durée',"Un an à compter de la signature, renouvelable automatiquement. Chaque partie peut y mettre fin par écrit avec un préavis de 30 jours. Les commissions sur les clients enregistrés avant la fin de l'accord restent dues selon l'article 3."],
['7. Obligations fiscales',"L'Apporteur déclare lui-même les commissions perçues selon son statut."]];
const f=l=>`<div class="fl"><span>${l}</span><i></i></div>`;
const html=`<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Arial,'Liberation Sans',sans-serif;color:#1F2A44;font-size:11.3px}
.pg{width:210mm;height:296mm;overflow:hidden;padding:28px 46px 20px;display:flex;flex-direction:column}
.hd{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:10px;border-bottom:3px solid #1E2A5E}
.id{display:flex;gap:14px}.id img{width:58px;height:58px;border-radius:50%}
.co{font-size:20px;font-weight:700;color:#1E2A5E}.tg{font-size:9px;letter-spacing:.14em;color:#55607A;margin:4px 0 3px}.ad{font-size:9.5px;color:#55607A;line-height:1.5}
.nb{background:#1E2A5E;color:#fff;border-radius:8px;padding:9px 13px;text-align:right;font-size:10px;line-height:1.6}.nb b{font-size:13px;letter-spacing:.05em}
.band{margin-top:12px;background:#1E2A5E;color:#fff;border-radius:10px;padding:13px 16px}.band .h{font-size:18px;font-weight:700}.band .s{font-size:11px;color:#C9D1EC;margin-top:4px}
.lb{font-size:9.5px;font-weight:700;letter-spacing:.14em;color:#D93A2B;margin:12px 0 5px}
.two{display:flex;gap:16px}.two>div{flex:1;border:1px solid #DCE1EF;border-left:4px solid #1E2A5E;border-radius:6px;padding:8px 12px;background:#F7F8FC;line-height:1.5}
.fl{display:flex;gap:6px;align-items:flex-end;margin:5px 0}.fl span{white-space:nowrap}.fl i{flex:1;border-bottom:1px dotted #55607A;height:12px}
.a{margin-top:7px;line-height:1.45}.a b{color:#1E2A5E}
.end{margin-top:auto}.sg{display:flex;gap:20px}.sg>div{flex:1;border:1px solid #DCE1EF;border-radius:8px;padding:9px 12px;height:150px;font-size:10.5px}
.sg b{color:#1E2A5E}.ft{text-align:center;font-size:9px;color:#7A849C;border-top:1px solid #DCE1EF;margin-top:10px;padding-top:6px}
</style></head><body><div class="pg">
<div class="hd"><div class="id"><img src="${logo}"><div><div class="co">Digital - Ivoire</div><div class="tg">COMMUNICATION MARKETING &amp; GESTION</div>
<div class="ad">Abidjan, Côte d'Ivoire<br>Tél : +225 05 74 99 96 75 • hello@vremaxx.com • www.vremaxx.com</div></div></div>
<div class="nb"><b>ACCORD</b><br>N° AP-2026-____<br>Abidjan, le ____ / ____ / 2026</div></div>
<div class="band"><div class="h">Accord d'apporteur d'affaires</div><div class="s">Programme partenaires Digital-Ivoire / VREMAX</div></div>
<div class="lb">ENTRE LES PARTIES</div>
<div class="two"><div><b>Digital-Ivoire</b>, Abidjan, représentée par Vremen Hermann, fondateur,<br>ci-après « Digital-Ivoire ».</div>
<div>${f('Nom / raison sociale :')}${f('Activité :')}${f('Ville :')}${f('Téléphone :')}${f('Email :')}${f('Paiement (Mobile Money / virement) :')}ci-après « l'Apporteur ».</div></div>
<div class="lb">CONDITIONS</div>
${art.map(a=>`<div class="a"><b>${a[0]}.</b> ${a[1]}</div>`).join('').replace(/\.\./g,'.')}
<div class="end"><div class="lb">SIGNATURES</div>
<div class="sg"><div><b>Pour Digital-Ivoire</b><br>Vremen Hermann, fondateur<br>Signature et cachet :</div><div><b>L'Apporteur</b><br>Nom :<br>Signature, précédée de « Lu et approuvé » :</div></div>
</div><div class="ft">Accord établi en deux exemplaires, un pour chaque partie.</div>
</div></body></html>`;
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage();
const t=path.join(path.dirname(out),'.accord_tmp.html');fs.writeFileSync(t,html);await p.goto('file://'+t);
await p.pdf({path:out,format:'A4',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
await p.setViewportSize({width:794,height:1123});await p.screenshot({path:out.replace('.pdf','.png')});
await b.close();fs.unlinkSync(t);console.log('ok')})();
