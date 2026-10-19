// Rend un contrat HTML en PDF avec l'en-tête Digital-Ivoire sur chaque page.
// Usage : node render.cjs contrat.html sortie.pdf
const fs=require('fs'),path=require('path');
const {chromium}=require(path.join(__dirname,'../proforma/node_modules/playwright'));
const [,,src,out]=process.argv;
const logo='data:image/png;base64,'+fs.readFileSync(path.join(__dirname,'logo_s.png')).toString('base64');
const header=`<div style="width:100%;margin:0 20mm;font-family:Arial,sans-serif;display:flex;align-items:center;gap:10px;border-bottom:2px solid #1E2A5E;padding-bottom:6px;-webkit-print-color-adjust:exact">
<img src="${logo}" style="width:40px;height:40px;border-radius:50%">
<div style="flex:1"><div style="font-size:14px;font-weight:700;color:#1E2A5E">Digital - Ivoire</div>
<div style="font-size:7px;letter-spacing:.14em;color:#55607A">COMMUNICATION MARKETING &amp; GESTION</div></div>
<div style="font-size:7.5px;color:#55607A;text-align:right;line-height:1.5">Abidjan, Côte d'Ivoire<br>+225 05 74 99 96 75 • hello@vremaxx.com • www.vremaxx.com</div></div>`;
const footer=`<div style="width:100%;margin:0 20mm;font-family:Arial,sans-serif;font-size:7.5px;color:#7A849C;display:flex;justify-content:space-between;border-top:1px solid #DCE1EF;padding-top:4px">
<span>Contrat CTR-2026-0155 — Digital-Ivoire / Financial Performance-CI</span><span>Paraphes : ______ / ______</span><span>Page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.resolve(src));
await p.pdf({path:out,format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:header,footerTemplate:footer,margin:{top:'34mm',bottom:'22mm',left:'20mm',right:'20mm'}});
await b.close();console.log('ok',out)})();
