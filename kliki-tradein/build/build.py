import base64, json, sys
src = open('video.html', encoding='utf-8').read()
words = json.dumps([{"w": x["w"]} for x in json.load(open('words.json'))], ensure_ascii=False)
def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
common = src.replace('__WORDS__', words)
open('render.html', 'w', encoding='utf-8').write(common.replace('__FONT__', 'fonts/inter-latin.woff2').replace('__VO__', 'vo.mp3').replace('__SPL__', '../assets/spaylater-orange.png'))
out = common.replace('__FONT__', b64('fonts/inter-latin.woff2', 'font/woff2')).replace('__VO__', b64('vo.mp3', 'audio/mpeg')).replace('__SPL__', b64('../assets/spaylater-orange.png', 'image/png'))
open('../kliki-tradein.html', 'w', encoding='utf-8').write(out)
print('ok', len(out)//1024, 'KB')
