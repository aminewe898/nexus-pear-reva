import fs from 'node:fs/promises';
import {Workbook} from '@oai/artifact-tool';
const out='outputs/nexus-pear-reva-reviewed';
const data=JSON.parse(await fs.readFile(`${out}/design_data.json`,'utf8'));
const wb=Workbook.create();const sheet=wb.worksheets.add('BOM');
// Task: engineering procurement BOM; audience: prototype assembler; industry: embedded electronics.
// Artifact Tool has no documented CSV export in this runtime. Author and calculate here,
// then serialize the verified typed values into RFC4180 CSV without an unsolicited XLSX.
const headers=['Reference','Qty','Value','Description','Manufacturer','MPN','Package','Supplier','Supplier SKU','Unit Cost','Extended Cost','Availability','Datasheet URL','Notes','Currency'];
const prices={F1:[2.63,'DigiKey','18-1812L300/24SLERCT-ND','Price/stock captured 2026-10-07'],J2:[.80,'Mouser','306-SM15BGHSTBLFSN','Indexed price; live confirmation pending'],J3:[.874,'Samtec','TSW-107-07-G-S','Manufacturer indexed price; live confirmation pending'],J4:[.874,'Samtec','TSW-107-07-G-S','Manufacturer indexed price; live confirmation pending'],U6:[1.03,'Mouser','595-TXU0104PWR','Indexed price; live confirmation pending'],U8:[.23,'Mouser','595-TLV76033DBZR','Indexed price; live confirmation pending'],R35:[.10,'Mouser','603-RC0805FR-0734K8L','Indexed price; live confirmation pending']};
let rows=data.parts.filter(d=>d.footprint&&!d.ref.startsWith('TP')&&!d.ref.startsWith('H')).map(d=>{const q=prices[d.ref];return [d.ref,1,d.value,d.notes,d.manufacturer,d.mpn,d.footprint.split(':')[1],q?.[1]||'RFQ required',q?.[2]||'',q?.[0]??null,null,q?.[3]||'Exact live price and stock unconfirmed',d.datasheet,'CANDIDATE; DO NOT ORDER. '+d.notes,q?'USD':''];});
const external=[
 ['EXT_DISPLAY',1,'3.5 inch IPS / capacitive','ST7796S + FT6336U; native 320x480; landscape 480x320','Waveshare','29318','Off-board module','Waveshare','29318',18.99,null,'Official product price captured 2026-10-07','https://www.waveshare.com/product/3.5inch-capacitive-touch-lcd.htm','3.3V mode; GHR-15V-S housing and SSHL-002T-P0.2 contacts; 12MHz write limit','USD'],
 ['EXT_AMP_L EXT_AMP_R',2,'MAX98357A breakout','Two mono I2S DAC/class-D channels','Adafruit','3006','Off-board breakout','Adafruit','3006',5.95,null,'Add to Cart shown 2026-10-07','https://www.adafruit.com/product/3006','Harness to J3/J4; speaker terminals are on amplifier breakouts','USD'],
 ['EXT_MIC',1,'SPH0645LM4H breakout','Digital I2S MEMS microphone','Adafruit','3421','Off-board breakout','Adafruit','3421',6.95,null,'Add to Cart shown 2026-10-07','https://www.adafruit.com/product/3421','J5 harness; bottom acoustic port; exact microphone datasheet audit incomplete','USD'],
 ['EXT_SD',1,'3V microSD SPI breakout','Optional storage module','Adafruit','4682','Off-board breakout','Adafruit','4682',null,null,'Product page found; stock/price not captured','https://www.adafruit.com/product/4682','J6 harness to 3V/GND/CLK/CMD/DAT0/DAT3; no 5V level shifter',''],
 ['EXT_SPK_L EXT_SPK_R',2,'8 ohm / 2W','28 x 40 mm miniature full-range loudspeakers','Visaton','2945','Off-board driver','Mouser / TME','VS-K28.40-8',null,null,'Mouser indexed listing 898; TME indexed listing 200; live confirmation pending','https://www.visaton.de/en/products/drivers/miniature-speakers/k-2840-8-ohm','Rated 2W, maximum 3W; bridge outputs must never connect to GND',''],
 ['EXT_ANT',1,'2.4GHz external antenna','Real hinged RP-SMA antenna, 50 ohm','Taoglas','GW.11.A153','Off-board antenna','Mouser','960-GW11A153',null,null,'Indexed Mouser listing 1963; price/live stock unconfirmed','https://www.taoglas.com/datasheets/GW.11.A153.pdf','Use current rev H gain, up to 3dBi; module antenna certification limits not yet qualified',''],
 ['EXT_RF_CABLE',1,'100mm U.FL to RP-SMA(F)','Bulkhead coax assembly','Taoglas','CAB.774','Off-board cable','Not qualified','',null,null,'Datasheet found; supplier stock/price unverified','https://www.taoglas.com/datasheets/CAB.774.pdf','Confirm gender and length against mechanical drawing; not CAB.011 ambiguous revision',''],
 ['EXT_DISPLAY_HOUSING',1,'15 pin GH housing','Display cable carrier mate','JST','GHR-15V-S','Cable housing','RFQ required','',null,null,'No quote','https://www.jst-mfg.com/product/pdf/eng/eGH.pdf','Use only manufacturer-compatible contacts',''],
 ['EXT_DISPLAY_CONTACTS',15,'GH crimp contacts','26-30AWG contacts','JST','SSHL-002T-P0.2','Crimp terminal','RFQ required','',null,null,'No quote','https://www.jst-mfg.com/product/pdf/eng/eGH.pdf','0.76-1.0mm insulation; correct tooling required',''],
 ['EXT_HARNESS',1,'Display/audio/mic/SD harness set','Custom point-to-point assemblies','Custom assembly','NEXUS-PEAR-HARNESS-A-CANDIDATE','Wiring','RFQ required','',null,null,'No quote','../docs/PIN_ASSIGNMENTS.md','Pin mappings released as design intent; custom assembly, wire lengths and supplier assembly drawing require quote and approval',''],
];
rows=rows.concat(external);
sheet.getRange(`A1:O${rows.length+1}`).values=[headers,...rows];
rows.forEach((r,i)=>sheet.getCell(i+1,10).formulas=[[`=IF(J${i+2}="","",B${i+2}*J${i+2})`]]);
sheet.getRange(`A1:O${rows.length+1}`).format.font={name:'Arial',size:10};
sheet.getRange('A1:O1').format={fill:'#203A4B',font:{name:'Arial',bold:true,color:'#FFFFFF'},rowHeight:30,wrapText:true};
sheet.getRange(`A2:O${rows.length+1}`).format.rowHeight=22;
sheet.getRange('A1:A80').format.columnWidth=24;sheet.getRange('B1:B80').format.columnWidth=6;
sheet.getRange('C1:C80').format.columnWidth=34;sheet.getRange('D1:D80').format.columnWidth=70;
sheet.showGridLines=false;sheet.freezePanes.freezeRows(1);wb.recalculate();
const values=sheet.getRange(`A1:O${rows.length+1}`).values;
if(values.length!==rows.length+1)throw new Error('BOM row mismatch');
for(let i=1;i<values.length;i++)if(typeof values[i][9]==='number'&&Math.abs(values[i][10]-values[i][1]*values[i][9])>1e-8)throw new Error('Extended cost mismatch');
const err=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1000});
console.log(err.ndjson);
const preview=await wb.render({sheetName:'BOM',range:'A1:D8',scale:1.5,format:'png'});
await fs.writeFile('work/bom-preview.png',new Uint8Array(await preview.arrayBuffer()));
const escape=v=>v==null?'':`"${String(v).replaceAll('"','""')}"`;
const csv=values.map(r=>r.map(escape).join(',')).join('\r\n')+'\r\n';
await fs.writeFile(`${out}/hardware/BOM_REVA.csv`,csv,'utf8');
await fs.mkdir(`${out}/hardware/manufacturing/bom`,{recursive:true});
await fs.writeFile(`${out}/hardware/manufacturing/bom/BOM_REVA.csv`,csv,'utf8');
const sums={};for(const r of values.slice(1))if(typeof r[10]==='number')sums[r[14]]=(sums[r[14]]||0)+r[10];
await fs.writeFile(`${out}/validation/bom-summary.json`,JSON.stringify({rows:rows.length,quotedSubtotals:sums,unknownPriceRows:values.slice(1).filter(r=>typeof r[9]!=='number').length,completeQuote:false},null,2));
console.log(`Saved ${rows.length} BOM rows; quotes remain incomplete.`,sums);
const grouped=new Map();for(const r of values.slice(1)){const key=r[4]+'|'+r[5];if(!grouped.has(key))grouped.set(key,[r[4],r[5],0,'',r[6],r[12],r[11],r[9],r[14]]);const g=grouped.get(key);g[2]+=r[1];g[3]+=(g[3]?' ':'')+r[0];}
const rfq=wb.worksheets.add('RFQ');const rfqRows=[['Manufacturer','MPN','Qty for one build','References','Package','Datasheet','Quote status','Observed unit price','Currency'],...grouped.values()];rfq.getRange(`A1:I${rfqRows.length}`).values=rfqRows;
await fs.writeFile(`${out}/hardware/RFQ_GROUPED.csv`,rfq.getRange(`A1:I${rfqRows.length}`).values.map(r=>r.map(escape).join(',')).join('\r\n')+'\r\n');
