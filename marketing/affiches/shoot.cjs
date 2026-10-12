const { chromium } = require('/home/claude/reel/node_modules/playwright');
const fs=require('fs');const D='/tmp/claude-0/-home-claude-vremax/f9f34287-da94-548e-8d92-9b3107858ebc/scratchpad/k30/';
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1080}});
const only=process.argv.slice(2);
for(const f of fs.readdirSync(D+'render').sort()){ if(only.length&&!only.includes(f.replace('.html','')))continue;
await p.goto('file://'+D+'render/'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(120);
await p.screenshot({path:D+'png/VREMAX_Comptabilite_'+f.replace('.html','.png')});}
await b.close();console.log('done')})();
