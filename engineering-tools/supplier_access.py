import requests
u='https://www.mouser.com/c/?q=RC0805FR-0710KL';r=requests.get(u,timeout=15);print(r.status_code,len(r.content),r.text[:100])
