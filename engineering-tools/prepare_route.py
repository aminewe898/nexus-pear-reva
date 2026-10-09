from pathlib import Path
from inspect_lib import parse
import json
dsn=Path('work/nexus.dsn');s=dsn.read_text(encoding='utf8')
i=s.index('(class kicad_default');depth=0;quote=False;escape=False
for j in range(i,len(s)):
 ch=s[j]
 if quote:
  if escape:escape=False
  elif ch=='\\':escape=True
  elif ch=='"':quote=False
 else:
  if ch=='"':quote=True
  elif ch=='(':depth+=1
  elif ch==')':
   depth-=1
   if depth==0:break
node=parse(s[i:j+1]);power={'+5V','+5V_AUDIO','+5V_FUSED','+3V3_DISPLAY','VBUS','SW_NODE'}
node=[x for x in node if isinstance(x,list) or x not in power]
def emit(x):
 if isinstance(x,list):return '('+' '.join(emit(a) for a in x)+')'
 return json.dumps(x) if any(c in x for c in ' ()') else x
wide=['class','Power']+sorted(power)+[['circuit',['use_via','Via[0-3]_600:300_um']],['rule',['width','800'],['clearance','200']]]
s=s[:i]+emit(node)+'\n'+emit(wide)+s[j+1:]
dsn.write_text(s,encoding='utf8')
print('Prepared route: 0.8mm main 5V/switched power paths; 0.2mm signals, 0.2mm clearance, 0.6/0.3mm vias. Automatic neckdown allowed at pads.')
