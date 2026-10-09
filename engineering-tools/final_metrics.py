from pathlib import Path
import pcbnew as p,json,collections
r=Path('outputs/nexus-pear-reva-reviewed');b=p.LoadBoard(str((r/'hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve()));lens=collections.defaultdict(float);width={};layers=collections.Counter();vias=0;tracks=0
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):vias+=1;continue
 tracks+=1;n=t.GetNetname();lens[n]+=p.ToMM(t.GetLength());w=p.ToMM(t.GetWidth());width[n]=min(width.get(n,100),w);layers[b.GetLayerName(t.GetLayer())]+=1
metrics={'lengths_mm':dict(lens),'minimum_width_mm':width,'track_layer_counts':dict(layers),'vias':vias,'tracks':tracks,'footprints':len(list(b.GetFootprints())),'length_note':'Summed net segment length, including branches; not necessarily end-to-end path length.','usb_90ohm_qualified':False,'physical_tests_performed':False}
(r/'validation/layout-metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps({k:metrics[k] for k in ['vias','tracks','footprints','track_layer_counts']},indent=2));print('USB and SW net sums:',{k:v for k,v in lens.items() if k.startswith('USB') or k=='SW_NODE'})
