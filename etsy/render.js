// node render.js jobs.json : renders each HTML job to a JPEG with Playwright
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();
const p=await b.newPage({viewport:{width:2000,height:1600}});
for(const j of jobs){await p.setViewportSize({width:j.w||2000,height:j.h||1600});await p.setContent(j.html,{waitUntil:'load'});
await p.waitForTimeout(80);await p.screenshot({path:j.out,type:'jpeg',quality:88});}
await b.close();console.log('rendered',jobs.length)})();
