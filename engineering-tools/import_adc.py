from pathlib import Path
import pcbnew as p
PRO=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva').resolve()
b=p.LoadBoard(str(PRO/'nexus-pear-reva.kicad_pcb'))
ses=Path('work/nexus-adc-fixed.ses').resolve()
print('SES import',p.ImportSpecctraSES(b,str(ses)))
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
fps={f.GetReference():f for f in b.GetFootprints()}
refs={'C17':(40,41),'R2':(78,60),'R27':(80,85.8),'R23':(87,95),'C18':(87,92.5),'U2':(52,109),'C9':(52.7,89.8)}
for ref,pos in refs.items():fps[ref].Reference().SetPosition(xy(pos));fps[ref].Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
values={'TP13':(43,36),'TP8':(46,70),'TP15':(44,79.2),'TP6':(85,105),'TP14':(77,77),'TP16':(36,97),'TP7':(95,47)}
for ref,pos in values.items():fps[ref].Value().SetPosition(xy(pos))
for text in b.Drawings():
 if isinstance(text,p.PCB_TEXT):
  t=text.GetText()
  if t=='MIC / TOP':text.SetPosition(xy((43,33)))
  if t=='STEREO AMP HARNESS':text.SetPosition(xy((45,56)))
  if t=='USB-C 5V / DEVICE':text.SetPosition(xy((60,118)))
p.SaveBoard(str(PRO/'nexus-pear-reva.kicad_pcb'),b)
print('Saved routed candidate,',len(list(b.GetTracks())),'tracks/vias; full native DRC follows')

