import requests
from pathlib import Path
from pypdf import PdfReader
urls={'cc':'https://www.ti.com/lit/ds/symlink/tusb320lai.pdf','efuse':'https://www.ti.com/lit/ds/symlink/tps25940.pdf','aon':'https://www.ti.com/lit/ds/symlink/tlv760.pdf','nor':'https://www.ti.com/lit/ds/symlink/sn74lvc2g02.pdf','audio-isolation':'https://www.ti.com/lit/ds/symlink/txu0104.pdf','display-schematic':'https://files.waveshare.com/wiki/3.5inch%20Capacitive%20Touch%20LCD/3.5inch_Capacitive_Touch_LCD_Schematic.pdf'}
for name,url in urls.items():
 r=requests.get(url,timeout=25);r.raise_for_status();p=Path('work/'+name+'.pdf');p.write_bytes(r.content);p.with_suffix('.txt').write_text('\n'.join(a.extract_text() or '' for a in PdfReader(p).pages),encoding='utf8');print(name,len(r.content))
