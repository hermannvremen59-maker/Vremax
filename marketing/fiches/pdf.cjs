const {chromium}=require('/home/claude/reel/node_modules/playwright');
const fs=require('fs'),path=require('path');
const D=path.join(__dirname,'out');
(async()=>{
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});
  for(const f of fs.readdirSync(D).filter(x=>x.endsWith('.html'))){
    await p.goto('file://'+path.join(D,f)); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(200);
    const n=f.replace('.html','');
    await p.pdf({path:path.join(D,'VREMAX_'+n+'.pdf'),format:'A4',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
    await p.screenshot({path:path.join(D,n+'.png')});
  }
  await b.close(); console.log('done');
})();
