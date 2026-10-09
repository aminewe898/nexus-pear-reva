from pathlib import Path
import shutil
old=Path('outputs/nexus-pear-reva');new=Path('outputs/nexus-pear-reva-reviewed')
shutil.copy2(old/'hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb','work/user-session-save.kicad_pcb')
shutil.copytree(old,new,ignore=shutil.ignore_patterns('.history','*-backups','*.kicad_prl','~*'),dirs_exist_ok=True)
names=['build_design_fixed','build_pcb','place_direct','pad_positions','critical_routes','import_fixed','stitch_planes','manufacturer_fixes','fix_new_clearance','vbus_fix','raw_power_route','ground_finish','cc2_route','finish_new_layout']
for name in names:
 s=Path('work/'+name+'.py').read_text().replace('outputs/nexus-pear-reva','outputs/nexus-pear-reva-reviewed')
 if name=='fix_new_clearance':
  idx=s.index('def xy')
  extra="""\nlookup={'cb0ad747-e365-48ac-927f-2baea1fb922c':('I2S_BCLK_SRC',(66.532,68.6742)), '5670cb03-1823-4125-84cf-a0b6ad0c5c85':('POWER_GOOD',(42.3873,99.1132)), '14485d18-4500-431b-b879-f2685f865dbc':('POWER_GOOD',(42.4889,96.9141)), '45f33b8f-93e4-4bf5-a723-238a68a16295':('POWER_GOOD',(42.3873,97.0157)), '19f58cb7-a8f9-446e-a20e-103acfc1150f':('CC1',(54.0432,111.5994)), '88795d20-790b-4cea-93f6-f38948dd765b':('CC1',(54.1998,111.756)), '92cee17a-302c-4006-9e56-e6575db2d44f':('CC1',(54.275,111.8)), 'd2d8634c-88d9-4d72-9aec-9e04accd9e89':('CC1',(54.231,111.756))}\nfor key,(net,pos) in lookup.items():\n matches=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()==net and math.dist(tuple(p.ToMM(t.GetStart())),pos)<.0001]\n if len(matches)!=1:raise RuntimeError((key,len(matches)))\n items[key]=matches[0]\n"""
  s=s[:idx]+extra+s[idx:]
 if name=='pad_positions':s=s.replace("p.FromMM(77)","p.FromMM(75.5)")
 Path('work/recover_'+name+'.py').write_text(s)
