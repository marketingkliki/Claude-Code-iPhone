const {chromium}=require('playwright');
(async()=>{const ts=process.argv.slice(2).map(Number);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.addInitScript(()=>{window.__FRAMES__=true});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+__dirname+'/render.html');await p.evaluate(()=>document.fonts.ready);
for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${__dirname}/shots/s_${t.toFixed(2)}.png`})}
if(errs.length)console.log('ERR',errs.join('\n'));await b.close()})();
