import requests, os, io, json
from PIL import Image
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Referer':'https://www.pexels.com/'}
os.makedirs('fetch/out/pexels',exist_ok=True)
log={}
for line in open('fetch/pexels.txt'):
    line=line.strip()
    if not line: continue
    slot,pid=line.split()
    url=f'https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1600'
    try:
        r=requests.get(url,headers=H,timeout=60); log[pid]=r.status_code
        if r.status_code==200:
            im=Image.open(io.BytesIO(r.content)).convert('RGB'); im.save(f'fetch/out/pexels/{slot}_{pid}.jpg',quality=88)
    except Exception as e: log[pid]=str(e)
json.dump(log,open('fetch/out/pexels_log.json','w'),indent=1)
