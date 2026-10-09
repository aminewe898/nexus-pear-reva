from pathlib import Path
import pcbnew as p
pro=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva');path=pro/'nexus-pear-reva.kicad_pcb'
b=p.LoadBoard(str(path.resolve()))
for t in list(b.GetTracks()):
 if t.GetNetname() in ['CC2_ADC','LCD_D1']:b.RemoveNative(t)
 elif not isinstance(t,p.PCB_VIA) and t.GetWidth()<p.FromMM(.2):t.SetWidth(p.FromMM(.2))
for raw in b.GetFootprints():
 f=p.Cast_to_FOOTPRINT(raw)
 if f.GetReference()=='U1':
  for pad in f.Pads():
   if pad.GetNumber()=='5':pad.SetNet(b.FindNet('CC2_ADC'))
   if pad.GetNumber()=='22':pad.SetNet(b.FindNet('LCD_D1'))
p.SaveBoard(str(path.resolve()),b)
p.ExportSpecctraDSN(b,str(Path('work/nexus.dsn').resolve()))
print('ADC1 swap and track width correction saved')


