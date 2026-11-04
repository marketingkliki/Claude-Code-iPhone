import base64, json, sys
src_name, render_name, out_name = sys.argv[1:4]
src = open(src_name, encoding='utf-8').read()
words = json.dumps([{"w": x["w"]} for x in json.load(open('words.json'))], ensure_ascii=False)
def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
common = src.replace('__WORDS__', words)
R = {'__FONT__': 'fonts/inter-latin.woff2', '__CAVEAT__': 'fonts/caveat-latin.woff2', '__VO__': 'vo.mp3', '__SPL__': '../assets/spaylater-orange.png'}
M = {'__FONT__': 'font/woff2', '__CAVEAT__': 'font/woff2', '__VO__': 'audio/mpeg', '__SPL__': 'image/png'}
r, o = common, common
for k, v in R.items():
    r = r.replace(k, v)
    if k in o: o = o.replace(k, b64(v, M[k]))
open(render_name, 'w', encoding='utf-8').write(r)
open(out_name, 'w', encoding='utf-8').write(o)
print('ok', len(o)//1024, 'KB')
