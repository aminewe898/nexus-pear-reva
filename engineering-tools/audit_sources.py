import requests
from pathlib import Path
from pypdf import PdfReader
urls={'buttons':'https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf','gh':'https://www.jst-mfg.com/product/pdf/eng/eGH.pdf','panel-controller':'https://files.waveshare.com/wiki/common/ST7796S_Datasheet.pdf','touch-controller':'https://files.waveshare.com/wiki/common/FT6336U_Datasheet.pdf','inductor':'https://www.bourns.com/data/global/pdfs/SRN6028C.pdf','fuse':'https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf','mosfet':'https://assets.nexperia.com/documents/data-sheet/2N7002.pdf'}
for n,u in urls.items():
 try:
  r=requests.get(u,timeout=20);r.raise_for_status();p=Path('work/'+n+'.pdf');p.write_bytes(r.content);p.with_suffix('.txt').write_text('\n'.join(x.extract_text() or '' for x in PdfReader(p).pages),encoding='utf8');print(n,len(r.content))
 except Exception as e:print(n,str(e))
