from pathlib import Path
s=Path('work/build_design.py').read_text()
cut=s.index('# Schematic source')
patch=r'''
# Reviewed replacement circuit. Native generation is kept reproducible.
remove={'R3','R4','R5','R6','C4','C5','C7','U6','U7','C12','C13','R12'}
parts[:]=[d for d in parts if d['ref'] not in remove]
by={d['ref']:d for d in parts}
def change(ref,**kw):by[ref].update(kw)
def setpins(ref,pins):by[ref]['pins']=[dict(num=str(a[0]),name=a[1],net=a[2],type=a[3] if len(a)>3 else 'passive') for a in pins]
for d in parts:
 for a in d['pins']:
  a['net']={'+5V_AUDIO':'+5V','+3V3_DISPLAY':'+3V3'}.get(a['net'],a['net'])
 if d['ref'].startswith('TP'):d['value']=d['pins'][0]['net']
newassign={'IO4':'LCD_MOSI','IO6':'LCD_CS','IO7':'LCD_BL','IO8':'TP_RST','IO9':'TP_INT','IO10':'LCD_MISO','IO12':'LCD_SCLK_SRC','IO13':'LCD_DC_SRC','IO14':'LCD_RST','IO2':None,'IO5':None,'IO11':None}
for a in by['U1']['pins']:
 if a['name'] in newassign:a['net']=newassign[a['name']]
change('U1',xy=(62,96),notes='Manufacturer pin table checked; GPIO35/36/37 reserved for octal PSRAM. External RF socket.')
change('U2',notes='USB data ESD; bias from protected main 5V, not raw VBUS')
for a in by['U2']['pins']:
 if a['name']=='VBUS':a['net']='+5V'
change('U3',value='PESD5V0S2BT CC ESD',footprint='Package_TO_SOT_SMD:SOT-23',mpn='PESD5V0S2BT,215',manufacturer='Nexperia',datasheet='https://assets.nexperia.com/documents/data-sheet/PESD5V0S2BT.pdf',notes='Ground-referenced CC ESD; no rail injection. Not a 20V CC-to-VBUS short protector.')
setpins('U3',[(1,'LINE1','CC1'),(2,'LINE2','CC2'),(3,'COMMON','GND')])
change('C6',value='100n',mpn='GRM21BR71H104KA01L',notes='50V X7R raw input decoupling; upstream capacitance below 1uF')
change('U4',value='TPS25940LRVCR eFuse',footprint='Package_DFN_QFN:Texas_RVC0020A_WQFN-20-1EP_3x4mm_P0.5mm_EP1.6x2.6mm',mpn='TPS25940LRVCR',datasheet='https://www.ti.com/lit/ds/symlink/tps25940.pdf',notes='Latched eFuse: reverse blocking, UVLO, OVP, ~2.56A limit, controlled rise; only enabled on 3A advertisement',unit_cost=None,availability='Mouser indexed 5963; live cart required')
setpins('U4',[(1,'DEVSLP','GND','input'),(2,'PGOOD','POWER_GOOD','open_collector'),(3,'PGTH','PGTH','input')]+[(i,'OUT','+5V','power_out') for i in range(4,9)]+[(i,'IN','+5V_FUSED','power_in') for i in range(9,14)]+[(14,'EN_UVLO','EFUSE_EN','input'),(15,'OVP','OVP','input'),(16,'GND','GND','power_in'),(17,'ILIM','ILIM'),(18,'dVdT','SLEW'),(19,'IMON','IMON','output'),(20,'FLT','POWER_FAULT','open_collector'),(21,'EP','GND','power_in')])
change('J2',value='WAVESHARE 29318 GH15',footprint='Connector_JST:JST_GH_SM15B-GHS-TB_1x15-1MP_P1.25mm_Horizontal',mpn='SM15B-GHS-TB(LF)(SN)',manufacturer='JST',datasheet='https://www.jst-mfg.com/product/pdf/eng/eGH.pdf',notes='GH15 straight-through harness, 3.3V mode; mate GHR-15V-S and SSH-003T-P0.2. No 5V on either supply pin.')
setpins('J2',[(i+1,n,n) for i,n in enumerate(['+3V3','+3V3','GND','LCD_MISO','LCD_MOSI','LCD_SCLK','DISPLAY_SD_CS','LCD_CS','LCD_DC','LCD_RST','LCD_BL','I2C_SDA','I2C_SCL','TP_INT','TP_RST'])])
setpins('R10',[(1,'1','LCD_SCLK_SRC'),(2,'2','LCD_SCLK')])
for ref in ('J3','J4'):
 for a in by[ref]['pins']:
  a['net']={'I2S_TX':'AMP_TX','I2S_BCLK':'AMP_BCLK','I2S_WS':'AMP_WS'}.get(a['net'],a['net'])
for ref,a,b in [('R17','AMP_BCLK_BUF','AMP_BCLK'),('R18','AMP_WS_BUF','AMP_WS'),('R19','AMP_TX_BUF','AMP_TX')]:setpins(ref,[(1,'1',a),(2,'2',b)])
# Microphone clocks remain 3.3V; amplifier clocks pass through the fail-safe buffer.
for a in by['J5']['pins']:a['net']={'I2S_BCLK':'MIC_BCLK','I2S_WS':'MIC_WS'}.get(a['net'],a['net'])
for ref,net in [('TP7','+3V3'),('TP8','+5V'),('TP11','MIC_BCLK'),('TP12','MIC_WS'),('TP16','CC_3A_OK'),('TP17','IMON')]:setpins(ref,[(1,net,net)]);change(ref,value=net)
change('R21',mpn='RC0805JR-070RL',notes='Zero-ohm jumper; resistor tolerance code J, not F')
add('U6','TXU0104PWR fail-safe I2S','Package_SO:TSSOP-14_4.4x5mm_P0.65mm',[(1,'VCCA','+3V3','power_in'),(2,'A1','I2S_BCLK_SRC','input'),(3,'A2','I2S_WS_SRC','input'),(4,'A3','I2S_TX_SRC','input'),(5,'A4','GND','input'),(6,'NC',None),(7,'GND','GND','power_in'),(8,'OE','PERIPH_EN','input'),(9,'NC',None),(10,'B4',None,'output'),(11,'B3','AMP_TX_BUF','output'),(12,'B2','AMP_WS_BUF','output'),(13,'B1','AMP_BCLK_BUF','output'),(14,'VCCB','+5V','power_in')],'04_audio',(63,65),'TXU0104PWR','Texas Instruments','https://www.ti.com/lit/ds/symlink/txu0104.pdf','Automatic supply isolation and Ioff; default disabled by R9. Same-rail display/mic/SD eliminate independent power-off injection.')
add('U7','TUSB320LAIRWBR Type-C sink','Package_DFN_QFN:Texas_X2QFN-12_1.6x1.6mm_P0.4mm',[(1,'CC1','CC1'),(2,'CC2','CC2'),(3,'PORT','GND','input'),(4,'VBUS_DET','VBUS_DET','input'),(5,'ADDR',None,'input'),(6,'OUT3',None,'open_collector'),(7,'OUT1','CC_OUT1','open_collector'),(8,'OUT2','CC_OUT2','open_collector'),(9,'ID',None,'open_collector'),(10,'GND','GND','power_in'),(11,'EN_N','GND','input'),(12,'VDD','+3V3_AON','power_in')],'02_usb',(55,112),'TUSB320LAIRWBR','Texas Instruments','https://www.ti.com/lit/ds/symlink/tusb320lai.pdf','GPIO mode ADDR floating; sink PORT grounded; internal Rd. OUT1/2 low only for 3A advertisement.')
add('U8','TLV76033DBZR always-on','Package_TO_SOT_SMD:SOT-23',[(1,'OUT','+3V3_AON','power_out'),(2,'IN','+5V_FUSED','power_in'),(3,'GND','GND','power_in')],'00_power',(37,87),'TLV76033DBZR','Texas Instruments','https://www.ti.com/lit/ds/symlink/tlv760.pdf','30V input rating; pin order follows corrected Rev A datasheet. Powers only CC detector and logic.')
add('U9','SN74LVC2G02DCUR dual NOR','Package_SO:VSSOP-8_2.3x2mm_P0.5mm',[(1,'1A','CC_OUT1','input'),(2,'1B','CC_OUT2','input'),(3,'2Y','CC_NOT_3A','output'),(4,'GND','GND','power_in'),(5,'2A','CC_3A_OK','input'),(6,'2B','CC_3A_OK','input'),(7,'1Y','CC_3A_OK','output'),(8,'VCC','+3V3_AON','power_in')],'02_usb',(59,107),'SN74LVC2G02DCUR','Texas Instruments','https://www.ti.com/lit/ds/symlink/sn74lvc2g02.pdf','3A truth table hardware interlock; no MCU sampling thresholds')
add('Q1','2N7002 eFuse inhibit','Package_TO_SOT_SMD:SOT-23',[(1,'G','CC_NOT_3A','input'),(2,'S','GND'),(3,'D','EFUSE_EN')],'00_power',(43,88),'2N7002,215','Nexperia','https://assets.nexperia.com/documents/data-sheet/2N7002.pdf','Pulls eFuse enable below UVLO when unattached/default/1.5A')
add('D2','SMBJ10A VBUS TVS','Diode_SMD:D_SMB',[(1,'K','+5V_FUSED'),(2,'A','GND')],'00_power',(38,106),'SMBJ10A','Littelfuse','https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj10a','17V rated pulse clamp below eFuse 20V absolute maximum; transient energy qualification pending')
for ref,val,a,b,xy in [('R32','47k','+3V3_AON','CC_OUT1',(62,110)),('R33','47k','+3V3_AON','CC_OUT2',(62,113)),('R34','887k','+5V_FUSED','VBUS_DET',(57,116)),('R35','34.8k','ILIM','GND',(34,98)),('R36','309k','+5V_FUSED','EFUSE_EN',(43,91)),('R37','100k','EFUSE_EN','GND',(43,94)),('R38','475k','+5V_FUSED','OVP',(34,91)),('R39','100k','OVP','GND',(34,94)),('R40','332k','+5V','PGTH',(44,99)),('R41','100k','PGTH','GND',(44,102)),('R42','10k','IMON','GND',(34,102)),('R43','10k','+3V3','POWER_GOOD',(46,85)),('R44','10k','+3V3','POWER_FAULT',(46,81)),('R45','10k','+3V3','DISPLAY_SD_CS',(102,44)),('R46','33','I2S_BCLK_SRC','MIC_BCLK',(73,84)),('R47','33','I2S_WS_SRC','MIC_WS',(73,80)),('R48','100k','AMP_BCLK','GND',(56,58)),('R49','100k','AMP_WS','GND',(59,58)),('R50','100k','AMP_TX','GND',(62,58))]:
 r(ref,val,a,b,'00_power' if int(ref[1:]) in range(35,45) else '03_display' if ref=='R45' else '04_audio' if int(ref[1:])>=46 else '02_usb',xy)
for ref in ('R38','R39'):
 d=next(d for d in parts if d['ref']==ref);d['mpn']='RT0805BRD07'+('475KL' if ref=='R38' else '100KL');d['notes']='0.1% OVP threshold divider'
for ref,val,a,xy in [('C20','100n','+5V_FUSED',(37,83)),('C21','1u','+3V3_AON',(37,91)),('C22','100n','+3V3_AON',(55,108)),('C23','100n','+3V3_AON',(63,104)),('C24','100n','+3V3',(57,65)),('C25','100n','+5V',(68,65))]:c(ref,val,a,'GND','00_power' if int(ref[1:])<=21 else '02_usb' if int(ref[1:])<=23 else '04_audio',xy)
add('C26','47n',CFP,[(1,'1','SLEW'),(2,'2','GND')],'00_power',(39,96),'GRM21BR71H473KA01L','Murata','https://www.murata.com/en-global/products/capacitor/mlcc','50V X7R; nominal ~19.5ms eFuse ramp')
# Reposition critical loops and MCU close to USB. Spare upper board remains accessible.
reposition={'U4':(38,100),'U5':(66,47),'C8':(61,47),'C9':(69.2,46),'L1':(72,48),'C10':(78,46),'C11':(78,50),'U1':(62,96),'C2':(49,93),'C3':(49,90),'R1':(74,91),'C1':(77,91),'R2':(74,95),'R7':(48,102),'R8':(48,105),'U2':(48,112),'U3':(53,116),'C6':(33,107),'J2':(105,40),'R10':(94,48),'R11':(94,52),'C15':(99,48),'TP3':(49,85),'TP4':(46,89),'TP5':(83,106),'TP6':(85,102),'TP16':(67,108),'TP17':(33,87),'J7':(77,102),'J8':(125,71),'SW8':(81,65),'D1':(72,74),'R31':(69,74),'R17':(63,71),'R18':(63,74),'R19':(63,77),'R9':(57,74),'TP11':(76,59),'TP12':(80,59),'TP15':(57,78)}
for d in parts:
 if d['ref'] in reposition:d['xy']=reposition[d['ref']]
 if d['ref'] in ('C2','C3','C8'):d['angle']=180
 if d['ref']=='C9':d['angle']=90
 if d['ref']=='J2':d['angle']=0
 # Procurement-only assumptions must never masquerade as verified quotations.
 if d['ref'].startswith('R') and d['ref'] not in ('R38','R39','R21'):
  d['notes']='1% 0805 thick-film; exact value and pin mapping explicit'
'''
s=s[:cut]+patch+'\n'+s[cut:]
s=s.replace('ESP32-S3 external antenna / remote AI / stereo I2S / candidate 8080 IPS','ESP32-S3 external antenna / remote AI / stereo I2S / documented SPI IPS')
s=s.replace('DO NOT ORDER - candidate circuit; unresolved release gates in design review','DO NOT ORDER - no smoke speedruns. Read the design review.')
s=s.replace('DO NOT ORDER: routing, power negotiation and footprint audit are not released.','DO NOT ORDER: bench qualification and complete purchasing quote pending.')
Path('work/build_design_fixed.py').write_text(s)
