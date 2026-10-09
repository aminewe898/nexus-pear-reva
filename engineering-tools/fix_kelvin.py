from pathlib import Path
s=Path('work/critical_routes.py').read_text();s=s.replace("for ref,pos in", "for t in list(b.GetTracks()):b.RemoveNative(t)\nfor ref,pos in");s=s.replace("[(76.525,40),(64.8625,40)]","[(76.525,40),(62.8,40),(62.8,44.5),(64.35,46.05)]")
Path('work/critical_routes.py').write_text(s)
