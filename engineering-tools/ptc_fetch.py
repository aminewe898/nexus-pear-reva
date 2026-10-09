import requests
from pathlib import Path
from pypdf import PdfReader
u='https://www.littelfuse.com/assetdocs/low-rho-datasheet-update?assetguid=b786faf0-de16-4763-9d22-6b8080943caf';r=requests.get(u,timeout=25);r.raise_for_status();Path('work/ptc.pdf').write_bytes(r.content);Path('work/ptc.txt').write_text('\n'.join(p.extract_text() or '' for p in PdfReader('work/ptc.pdf').pages),encoding='utf8')
