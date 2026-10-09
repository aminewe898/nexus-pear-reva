from pathlib import Path
import re
p=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb');s=p.read_text();i=s.index('\t(footprint "Nexus:L_Bourns-SRN6028"');j=s.find('\n\t(footprint ',i+1);j=j if j>=0 else s.index('\n\t(segment ',i+1)
block=s[i:j];block=re.sub(r'\t\t\(fp_line.*?\n\t\t\)\n',lambda m:'' if 'F.SilkS' in m[0] else m[0],block,flags=re.S);s=s[:i]+block+s[j:];p.write_text(s)
