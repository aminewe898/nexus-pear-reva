from pathlib import Path
s=Path('work/finish_planes.py').read_text().replace("outputs/nexus-pear-reva/validation/drc-stitched.json","work/drc-new.json");s=s.replace("net=item.GetNetCode();done=False", "net=item.GetNetCode();done=False\n  if item.GetNetname() not in ('GND','+3V3'):continue")
Path('work/ground_finish.py').write_text(s)
