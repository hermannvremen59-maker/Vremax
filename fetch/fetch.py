import requests, json, os, io
from PIL import Image
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Accept':'application/json'}
os.makedirs('fetch/out/thumbs',exist_ok=True); os.makedirs('fetch/out/full',exist_ok=True)
meta=[]
want=[l.strip() for l in open('fetch/full.txt')] if os.path.exists('fetch/full.txt') else []
for q in [l.strip() for l in open('fetch/queries.txt') if l.strip()]:
    try:
        r=requests.get('https://unsplash.com/napi/search/photos',params={'query':q,'per_page':20,'plus':'none'},headers=H,timeout=30)
        res=r.json().get('results',[])
    except Exception as e:
        meta.append({'query':q,'error':str(e),'status':getattr(r,'status_code',None)}); continue
    for p in res:
        if p.get('premium') or p.get('plus'): continue
        pid=p['id']; meta.append({'query':q,'id':pid,'alt':p.get('alt_description'),'user':p['user']['name'],'link':p['links']['html'],'raw':p['urls']['raw']})
        try:
            im=Image.open(io.BytesIO(requests.get(p['urls']['small'],headers=H,timeout=30).content)).convert('RGB'); im.thumbnail((300,300)); im.save(f'fetch/out/thumbs/{pid}.jpg',quality=80)
        except Exception as e: pass
for pid in want:
    m=[x for x in meta if x.get('id')==pid]
    url=(m[0]['raw'] if m else f'https://unsplash.com/photos/{pid}/download?force=true')
    if m: url+= '&w=1600&q=85&fm=jpg'
    c=requests.get(url,headers=H,timeout=60,allow_redirects=True).content
    open(f'fetch/out/full/{pid}.jpg','wb').write(c)
json.dump(meta,open('fetch/out/meta.json','w'),indent=1,ensure_ascii=False)
print(len(meta))
