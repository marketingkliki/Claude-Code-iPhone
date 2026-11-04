const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const FPS=30,dir=__dirname+'/'+(process.env.FR||'frames');fs.mkdirSync(dir,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:+(process.env.H||1920)}});
await p.addInitScript(()=>{window.__FRAMES__=true});await p.goto('file://'+__dirname+'/'+(process.env.HTML||'render.html'));await p.evaluate(()=>document.fonts.ready);
const N=Math.round(await p.evaluate(()=>DUR)*FPS);
for(let f=0;f<N;f++){await p.evaluate(t=>render(t),f/FPS);await p.screenshot({path:`${dir}/f_${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:94});if(f%150==0)console.log(f,'/',N)}
console.log('DONE',N);await b.close()})();
