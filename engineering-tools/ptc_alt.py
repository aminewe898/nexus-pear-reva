import requests
from pathlib import Path
u='https://www.littelfuse.com/~/media/electronics/datasheets/resettable_ptcs/littelfuse_ptc_low_rho_datasheet.pdf.pdf';r=requests.get(u,timeout=15);print(r.status_code,len(r.content));
if r.status_code==200 and r.content.startswith(b'%PDF'):Path('work/ptc.pdf').write_bytes(r.content)
