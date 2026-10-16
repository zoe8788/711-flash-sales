"""Rebuild the published site from _source/.
Usage (from the repo root):  python3 _source/build.py
Writes index.html, d3.min.js, data/, img/, dm/ into the repo root."""
import json,base64,os,shutil,re,hashlib
SRC=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(SRC)
OUT=ROOT
d3js=open(os.path.join(ROOT,'d3.min.js'),'rb').read() if os.path.exists(os.path.join(ROOT,'d3.min.js')) else None
for d in ('img','dm','data'):
    shutil.rmtree(os.path.join(OUT,d),ignore_errors=True);os.makedirs(os.path.join(OUT,d))
H=os.path.join(SRC,'data')+'/'
def save(src,folder):
    m=re.match(r'data:image/(\w+);base64,(.*)',src,re.S)
    raw=base64.b64decode(m.group(2));ext='jpg' if m.group(1) in('jpeg','jpg') else m.group(1)
    name=hashlib.sha1(raw).hexdigest()[:16]+'.'+ext
    open(f'{OUT}/{folder}/{name}','wb').write(raw);return f'{folder}/{name}'
camps=json.load(open(H+'flash_sales_campaigns.json'))
prods=json.load(open(H+'flash_sales_products.json'))
pimg=[dict(r,src=save(r['src'],'img')) for r in json.load(open(H+'flash_sales_prodimg.json'))]
dm=[dict(r,src=save(r['src'],'dm')) for r in json.load(open(H+'flash_sales_dm.json'))]
data={'campaigns':camps,'products':prods,'prodimg':pimg,'dmimg':dm}
json.dump(data,open(OUT+'/data/data.json','w'),ensure_ascii=False)
params={'campaign':'miffy-2503'}

page=open(os.path.join(SRC,'page.html')).read()
page=page.replace("/^data:image\\//.test(r.src)","/^(data:image\\/|dm\\/|img\\/)/.test(r.src)").replace("/^data:image\\//.test(m.src)","/^(data:image\\/|dm\\/|img\\/)/.test(m.src)")
tokens='''<style>
:root{--color-fg:#1f1e1b;--color-fg-muted:#6b6862;--color-bg:#ffffff;--color-panel:#f7f6f3;--color-border-line:#e4e1da;
--color-ok:#1f7a4d;--color-warn:#a8650a;--color-bad:#c0392b;
--cds-border:#e4e1da;--cds-chart-axis:#b5b1a8;--cds-chart-grid:#ecebe6;--cds-chart-muted:#c9c6bf;--cds-chart-reference:#8a867d;
--cds-surface-popover:#ffffff;--cds-text-secondary:#6b6862;--cds-shadow-popover:0 6px 24px rgba(0,0,0,.14);
--cds-font-size-caption:.8125rem;--cds-font-size-body:.9375rem;--cds-font-size-heading:1.0625rem;--cds-font-size-title:1.5rem;--cds-font-weight-medium:600;
--cds-gap-xs:.25rem;--cds-gap-sm:.5rem;--cds-gap-md:1rem;--cds-gap-lg:1.5rem;--cds-gap-xl:2rem;
--cds-pad-xs:.25rem;--cds-pad-sm:.5rem;--cds-pad-md:.75rem;--cds-pad-lg:1.25rem;--cds-pad-xl:2rem;--cds-radius:10px;--cds-dur-slow:.3s;
--font-anthropic-sans:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;--font-anthropic-serif:"Noto Serif TC","PingFang TC",Georgia,serif}
@media (prefers-color-scheme:dark){:root{--color-fg:#ecebe6;--color-fg-muted:#a8a49b;--color-bg:#1b1a18;--color-panel:#24231f;--color-border-line:#3a3833;
--color-ok:#5cc28d;--color-warn:#e3a54a;--color-bad:#ef7564;--cds-border:#3a3833;--cds-chart-axis:#6b6862;--cds-chart-grid:#2f2d29;--cds-chart-muted:#55524b;--cds-chart-reference:#9a968c;
--cds-surface-popover:#2a2925;--cds-text-secondary:#a8a49b}}
html,body{margin:0;background:var(--color-bg);color:var(--color-fg);font-family:var(--font-anthropic-sans)}
#dash-root{max-width:1400px;margin:0 auto;padding:24px clamp(16px,3vw,40px) 48px;box-sizing:border-box}
.dash-skeleton{color:transparent!important;background:var(--color-panel);border-radius:6px}
.fs-pubnote{font-size:.8125rem;color:var(--color-fg-muted);margin-top:-8px}
</style>'''
shim='''<script>
(function(){
  const COLORS=['#3b6fd8','#e07b39','#2a9d8f','#c2547a','#8a6fd1','#b8a032','#5b8c3a','#7a7a7a'];
  let DATA=null,status='loading',params=Object.assign({},%PARAMS%),cbs=[],calcs={},cache={};
  try{const u=new URLSearchParams(location.search).get('c');if(u)params.campaign=u;}catch(e){}
  function rows(id){if(status!=='ok')return null;if(DATA[id])return DATA[id];if(calcs[id]){if(!(id in cache)){const c=calcs[id];cache[id]=c.fn(...c.inputs.map(rows));}return cache[id];}return null;}
  window.dash={colors:COLORS,
    data(id){if(status!=='ok')return{status,data:[],columns:[]};const r=rows(id);return r?{status:'ok',data:r,columns:r.length?Object.keys(r[0]):[]}:{status:'missing',data:[]};},
    calc(id,o){calcs[id]=o;},loader(){},
    onData(fn){cbs.push(fn);try{fn();}catch(e){console.error(e);}},
    params(){return Object.assign({},params);},
    setParams(p){Object.assign(params,p);try{const u=new URL(location.href);if(params.campaign)u.searchParams.set('c',params.campaign);history.replaceState(null,'',u);}catch(e){}run();},
    resetParams(){},setLink(){},refresh(){}};
  function run(){cbs.forEach((f)=>{try{f();}catch(e){console.error(e);}});}
  let w=window.innerWidth;window.addEventListener('resize',()=>{if(Math.abs(window.innerWidth-w)>20){w=window.innerWidth;run();}});
  fetch('data/data.json?v=%VER%').then((r)=>r.json()).then((d)=>{DATA=d;status='ok';cache={};run();}).catch(()=>{status='error';run();});
})();
</script>'''.replace('%PARAMS%',json.dumps(params)).replace('%VER%',hashlib.sha1(json.dumps(data,ensure_ascii=False).encode()).hexdigest()[:8])
html=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>7-11 快閃購營業額看板｜我適文創</title><meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600&family=Noto+Serif+TC:wght@400&display=swap" rel="stylesheet">
<script src="d3.min.js"></script>
{tokens}{shim}</head><body><div id="dash-root">{page}</div></body></html>'''
html=html.replace('<p class="fs-take dash-skeleton" id="takeaway"></p>','<p class="fs-take dash-skeleton" id="takeaway"></p>\n    <p class="fs-pubnote">資料更新：'+__import__('datetime').date.today().isoformat()+'</p>',1)
open(OUT+'/index.html','w').write(html)
if d3js: open(OUT+'/d3.min.js','wb').write(d3js)
print('built',OUT)
