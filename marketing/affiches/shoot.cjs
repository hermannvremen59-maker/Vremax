const { chromium } = require('playwright');
const fs=require('fs');const D=process.env.AFF_S||__dirname+'/';
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1080}});
const only=process.argv.slice(2);
for(const f of fs.readdirSync(D+'render').sort()){ if(only.length&&!only.includes(f.replace('.html','')))continue;
await p.goto('file://'+D+'render/'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(120);
await p.screenshot({path:D+'png/'+f.replace('.html','.png')});}
await b.close();console.log('done')})();
