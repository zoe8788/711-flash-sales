import { chromium } from 'playwright';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--headless=new']});
const p=await b.newPage({viewport:{width:1300,height:2600}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/flash-sales/?c=miffy-2611',{waitUntil:'load'});await p.waitForTimeout(2000);
await p.screenshot({path:'/home/claude/crops/m11_page.png'});console.log(errs);await b.close();
