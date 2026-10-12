import requests, json, os, io, re, html
from PIL import Image
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Accept':'text/html,application/xhtml+xml','Accept-Language':'en-US,en;q=0.9'}
os.makedirs('fetch/out/thumbs',exist_ok=True); os.makedirs('fetch/out/full',exist_ok=True)
meta=[]; seen=set()
for q in [l.strip() for l in open('fetch/queries.txt') if l.strip()]:
    slug=q.replace(' ','-')
    r=requests.get(f'https://unsplash.com/s/photos/{slug}',params={'license':'free'},headers=H,timeout=30)
    if r.status_code!=200: meta.append({'query':q,'status':r.status_code}); continue
    t=r.text
    for m in re.finditer(r'<img[^>]+>',t):
        tag=m.group(0)
        src=re.search(r'src="(https://images\.unsplash\.com/(?:flagged/)?photo-[^"?]+)',tag)
        if not src: continue
        base=src.group(1)
        if base in seen: continue
        seen.add(base)
        alt=re.search(r'alt="([^"]*)"',tag); alt=html.unescape(alt.group(1)) if alt else ''
        pid='u%03d'%len(meta)
        meta.append({'query':q,'id':pid,'alt':alt,'url':base})
        try:
            im=Image.open(io.BytesIO(requests.get(base+'?w=400&q=70&fm=jpg',headers=H,timeout=30).content)).convert('RGB'); im.thumbnail((300,300)); im.save(f'fetch/out/thumbs/{pid}.jpg',quality=80)
        except Exception as e: meta[-1]['err']=str(e)
json.dump(meta,open('fetch/out/meta.json','w'),indent=1,ensure_ascii=False)
want=[l.strip() for l in open('fetch/full.txt')] if os.path.exists('fetch/full.txt') else []
for u in want:
    if not u: continue
    name=u.split('/')[-1][:60]
    c=requests.get(u+'?w=1800&q=85&fm=jpg',headers=H,timeout=60).content
    open(f'fetch/out/full/{name}.jpg','wb').write(c)
print(len(meta))
