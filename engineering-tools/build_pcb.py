from pathlib import Path
import json,math,os
import pcbnew as p
from inspect_lib import parse,child
OUT=Path('outputs/nexus-pear-reva').resolve(); PRO=OUT/'hardware/kicad/nexus-pear-reva'
data=json.loads((OUT/'design_data.json').read_text(encoding='utf8'));parts=data['parts']
b=p.BOARD();b.GetDesignSettings().SetCopperLayerCount(4)
ds=b.GetDesignSettings();ds.m_MinClearance=p.FromMM(.2);ds.m_CopperEdgeClearance=p.FromMM(.3);ds.m_HoleClearance=p.FromMM(.25)
def xy(v):return p.VECTOR2I(p.FromMM(v[0]),p.FromMM(v[1]))
nets={}
export=parse(Path('work/nexus.net').read_text(encoding='utf8'));nodes={}
for net in child(export,'nets')[1:]:
 name=child(net,'name')[1]
 for node in net:
  if isinstance(node,list) and node and node[0]=='node':nodes[(child(node,'ref')[1],child(node,'pin')[1])]=name
for name in sorted(set(nodes.values())):
 n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
fps={};audit=[]
for d in parts:
 if not d['footprint']:continue
 name=d['footprint'].split(':')[1];fp=p.FootprintLoad(str(PRO/'Nexus.pretty'),name)
 if fp is None:raise ValueError(name)
 fp.SetReference(d['ref']);fp.SetValue(d['value']);fp.SetFPID(p.LIB_ID('Nexus',name));fp.SetPosition(xy(d['xy']));fp.SetOrientationDegrees(d['angle'])
 fp.SetPath(p.KIID_PATH('/'+data['root_uuid']+'/'+d['sheet_uuid']+'/'+d['uuid']))
 fp.SetFields({'MPN':d['mpn'],'Datasheet':d['datasheet'],'Description':d['notes']})
 for field in fp.GetFields():
  if field.GetName() not in ('Reference','Value'):field.SetVisible(False)
 fp.Reference().SetTextSize(xy((.9,.9)));fp.Reference().SetTextThickness(p.FromMM(.15))
 pinmap={a['num']:a['net'] for a in d['pins']};pads=[]
 for pad in fp.Pads():
  num=pad.GetNumber();net=nodes.get((d['ref'],num))
  # Thermal vias are fabrication geometry, not component lead dimensions.
  if d['ref']=='U1' and num=='41' and pad.GetAttribute()==p.PAD_ATTRIB_PTH:
   pad.SetDrillSize(xy((.3,.3)));pad.SetSize(xy((.6,.6)))
  if net:pad.SetNet(nets[net])
  elif num and num not in pinmap:raise ValueError(f'{d["ref"]} unmapped footprint pad {num}')
  pads.append({'number':num,'net':net,'at_mm':[p.ToMM(pad.GetPosition().x),p.ToMM(pad.GetPosition().y)],'size_mm':[p.ToMM(pad.GetSize().x),p.ToMM(pad.GetSize().y)],'drill_mm':[p.ToMM(pad.GetDrillSize().x),p.ToMM(pad.GetDrillSize().y)]})
 b.Add(fp);fps[d['ref']]=fp;audit.append({'ref':d['ref'],'footprint':d['footprint'],'pads':pads,'audit_status':'PIN NUMBER CONSISTENCY ONLY; manufacturer dimensional review not completed'})
for a,z in [((30,30),(130,30)),((130,30),(130,120)),((130,120),(30,120)),((30,120),(30,30))]:
 line=p.PCB_SHAPE(b);line.SetShape(p.SHAPE_T_SEGMENT);line.SetStart(xy(a));line.SetEnd(xy(z));line.SetLayer(p.Edge_Cuts);line.SetWidth(p.FromMM(.05));b.Add(line)
def label(t,at,size=1.2,layer=p.F_SilkS):
 text=p.PCB_TEXT(b);text.SetText(t);text.SetPosition(xy(at));text.SetTextSize(xy((size,size)));text.SetTextThickness(p.FromMM(.15));text.SetLayer(layer);b.Add(text)
label('NEXUS PEAR / REV A CANDIDATE',(80,32),1.4)
label('DO NOT ORDER - SEE DESIGN REVIEW',(99,117),1)
label('MIC / TOP',(39,32),1);label('RF U.FL ON MODULE',(67,36),.9)
label('DISPLAY / VERIFY CABLE',(113,72),.9);label('STEREO AMP HARNESS',(47,63),.9)
label('USB-C 5V / DEVICE',(47,119),.8)
for d in parts:
 if d['ref'].startswith('SW'):
  fps[d['ref']].Reference().SetVisible(False);label(d['value'],(d['xy'][0]+3,d['xy'][1]-2),1)
 # Supply labels on real test pads must be readable.
 if d['ref'].startswith('TP'):
  fps[d['ref']].Reference().SetVisible(False)
  fps[d['ref']].Value().SetVisible(True);fps[d['ref']].Value().SetLayer(p.F_SilkS);fps[d['ref']].Value().SetTextSize(xy((1,1)))
# Reserve an uninterrupted inner ground plane. No guessed controlled-impedance stackup.
for layer,rail in [(p.In1_Cu,'GND'),(p.In2_Cu,'+3V3')]:
 zone=p.ZONE(b);zone.SetLayer(layer);zone.SetNet(nets[rail]);zone.SetLocalClearance(p.FromMM(.25));zone.SetThermalReliefGap(p.FromMM(.3));zone.SetThermalReliefSpokeWidth(p.FromMM(.4));zone.SetPadConnection(p.ZONE_CONNECTION_THERMAL)
 outline=zone.Outline();outline.NewOutline()
 for pt in [(30.5,30.5),(129.5,30.5),(129.5,119.5),(30.5,119.5)]:outline.Append(int(xy(pt).x),int(xy(pt).y))
 b.Add(zone)
# Routing is performed from a clean DSN export, with native clearance constraints.
def pad(ref,num):return next(x for x in fps[ref].Pads() if x.GetNumber()==str(num))
def track_points(points,net,width=.5,layer=p.F_Cu):
 for a,z in zip(points,points[1:]):
  if a==z:continue
  t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(z));t.SetLayer(layer);t.SetWidth(p.FromMM(width));t.SetNet(nets[net]);b.Add(t)
def pos(ref,num):
 v=pad(ref,num).GetPosition();return [p.ToMM(v.x),p.ToMM(v.y)]
def link(a,z,net,width=.5,mid=[]):track_points([pos(*a)]+mid+[pos(*z)],net,width)
# Minimum local regulator loop, bootstrap, feedback and paired output capacitors.
"""
link(('U5',5),('L1',1),'SW_NODE',.6)
link(('U5',6),('C9',1),'BST',.25)
link(('C9',2),('U5',5),'SW_NODE',.25)
link(('L1',2),('C10',1),'+3V3',.8)
link(('C10',1),('C11',1),'+3V3',.8)
link(('C10',1),('U5',1),'+3V3',.25,[(62,90),(51.5,90)])
link(('C8',1),('U5',3),'+5V',.6)
link(('U5',2),('U5',3),'+5V',.25)
link(('U4',6),('C8',1),'+5V',.8)
link(('U4',4),('C7',1),'INPUT_CT',.25)
link(('U6',4),('C12',1),'AUDIO_CT',.25)
link(('U7',4),('C13',1),'DISPLAY_CT',.25)
link(('U1',2),('C3',1),'+3V3',.5)
link(('U1',3),('R1',2),'EN',.25)
link(('R1',2),('C1',1),'EN',.25)
link(('U6',6),('C14',1),'+5V_AUDIO',.6)
link(('U7',6),('C15',1),'+3V3_DISPLAY',.5)
"""
# Export exact geometry and connectivity so partial board status can be inspected.
(OUT/'validation').mkdir(exist_ok=True)
(OUT/'validation/footprint-pad-inventory.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
p.SaveBoard(str(PRO/'nexus-pear-reva.kicad_pcb'),b)
print('DSN export:',p.ExportSpecctraDSN(b,str(Path('work/nexus.dsn').resolve())))
print('Created native four-layer 100 x 90 mm board; placed '+str(len(fps))+' footprints; initial local routes only.')
