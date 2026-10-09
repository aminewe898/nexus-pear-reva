"""Reproducible candidate netlist and native KiCad schematic, not a release certificate."""
from pathlib import Path
import json,uuid,math,shutil
from inspect_lib import parse,walk,child,root
OUT=Path('outputs/nexus-pear-reva-reviewed').resolve(); PRO=OUT/'hardware/kicad/nexus-pear-reva'
PRO.mkdir(parents=True,exist_ok=True)
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'nexus-pear-reva/'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
ESP='https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf'
BUCK='https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf'
SW='https://www.ti.com/lit/ds/symlink/tps22918.pdf'
parts=[]
def add(ref,value,fp,pins,sheet,xy,mpn='',maker='',url='',note='',cost=None,avail='Not verified',angle=0):
 pins=[dict(num=str(p[0]),name=p[1],net=p[2],type=p[3] if len(p)>3 else 'passive') for p in pins]
 d=dict(ref=ref,value=value,footprint=fp,pins=pins,sheet=sheet,xy=xy,mpn=mpn,manufacturer=maker,datasheet=url,notes=note,unit_cost=cost,availability=avail,angle=angle,uuid=uid(ref))
 parts.append(d);return d
RFP='Resistor_SMD:R_0805_2012Metric'; CFP='Capacitor_SMD:C_0805_2012Metric'
def r(ref,val,a,b,s,xy,mpn=''):
 return add(ref,val,RFP,[(1,'1',a),(2,'2',b)],s,xy,mpn or 'RC0805FR-07'+{'10k':'10KL','100k':'100KL','5.1k':'5K1L','22k':'22KL','100':'100RL','33':'33RL','1k':'1KL','2.2k':'2K2L','4.7k':'4K7L','82k':'82KL','330k':'330KL','0':'0RL'}.get(val,val+'L'),'Yageo','https://www.yageo.com/en/ProductSearch',note='1%; sourcing and manufacturer land-pattern review pending')
def c(ref,val,a,b,s,xy,large=False):
 mpn={'100n':'GRM21BR71H104KA01L','1u':'GRM21BR71A105KA01L','4.7n':'GRM21BR71H472KA01L','10n':'GRM21BR71H103KA01L','22u':'GRM31CR61A226KE19L','4.7u':'GRM21BR61A475KA73L','10u':'GRM31CR61A106KA01L'}[val]
 return add(ref,val,'Capacitor_SMD:C_1206_3216Metric' if large else CFP,[(1,'1',a),(2,'2',b)],s,xy,mpn,'Murata','https://www.murata.com/en-global/products/capacitor/mlcc',note='Ceramic; exact DC-bias and sourcing review pending; do not substitute voltage rating blindly')
def header(ref,title,nets,s,xy,rows=1):
 n=len(nets); count=n//rows
 fp=f'Connector_PinHeader_2.54mm:PinHeader_{rows}x{count:02d}_P2.54mm_Vertical'
 mpn=f'TSW-{count:03d}-07-G-'+('D' if rows==2 else 'S')
 return add(ref,title,fp,[(i+1,net or 'UNUSED',net) for i,net in enumerate(nets)],s,xy,mpn,'Samtec','https://www.samtec.com/products/tsw',note='Carrier-side pin order only. Cable assembly and manufacturer drawing audit remain release gates.')
# Module pad numbers transcribed from installed library and cross-checked to Espressif pin table.
symbol=parse((root/'symbols/RF_Module.kicad_sym').read_text(encoding='utf8'))
sym=next(x for x in symbol if isinstance(x,list) and x[:2]==['symbol','ESP32-S3-WROOM-1'])
assign={'IO4':'LCD_D0','IO5':'CC2_ADC','IO6':'LCD_D2','IO7':'LCD_D3','IO8':'LCD_D4','IO9':'LCD_D5','IO10':'LCD_D6','IO11':'LCD_D7','IO12':'LCD_WR_SRC','IO13':'LCD_DC_SRC','IO15':'I2C_SCL','IO16':'I2C_SDA','IO17':'I2S_BCLK_SRC','IO18':'I2S_WS_SRC','IO21':'I2S_TX_SRC','IO47':'MIC_DATA','IO39':'SD_SCK_SRC','IO40':'SD_MOSI_SRC','IO41':'SD_MISO','IO42':'SD_CS','IO1':'KEY_ADC','IO2':'CC1_ADC','IO14':'LCD_D1','IO38':'PERIPH_EN','IO48':'STATUS','RXD0':'UART_RX','TXD0':'UART_TX','IO0':'BOOT','EN':'EN','USB_D-':'USB_DM','USB_D+':'USB_DP','3V3':'+3V3','GND':'GND'}
mp=[]
for p in walk(sym,'pin'):
 num=child(p,'number')[1];name=child(p,'name')[1];mp.append((num,name,assign.get(name),p[1]))
add('U1','ESP32-S3-WROOM-1U-N16R8','RF_Module:ESP32-S3-WROOM-1U',mp,'01_processor',(66,48),'ESP32-S3-WROOM-1U-N16R8','Espressif',ESP,'GPIO35/36/37 reserved for octal PSRAM; 3/45/46 deliberately NC. Module RF socket included.',5.94,'DigiKey Spain 0; Mouser listing reports stock but not live-confirmed')
r('R1','10k','+3V3','EN','01_processor',(55,58)); c('C1','1u','EN','GND','01_processor',(59,59))
c('C2','22u','+3V3','GND','01_processor',(66,61),True);c('C3','100n','+3V3','GND','01_processor',(68,58))
r('R2','10k','+3V3','BOOT','01_processor',(74,60))
# USB-C sink, USB2 FS device. CC sampling is a candidate, not certified current detection.
usb=[]
for num,name,net in [('A1','GND','GND'),('A4','VBUS','VBUS'),('A5','CC1','CC1'),('A6','D+','USB_DP_CONN'),('A7','D-','USB_DM_CONN'),('A8','SBU1',None),('A9','VBUS','VBUS'),('A12','GND','GND'),('B1','GND','GND'),('B4','VBUS','VBUS'),('B5','CC2','CC2'),('B6','D+','USB_DP_CONN'),('B7','D-','USB_DM_CONN'),('B8','SBU2',None),('B9','VBUS','VBUS'),('B12','GND','GND'),('SH','SHIELD','GND')]:usb.append((num,name,net))
add('J1','USB-C 5V / USB2 FS','Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal',usb,'02_usb',(48,117.4),'USB4105-GF-A','GCT','https://gct.co/files/drawings/usb4105.pdf','Fixed sink; no PD, no host; shield bonded to ground. Exact footprint requires final dimension audit.')
r('R3','5.1k','CC1','GND','02_usb',(41,110));r('R4','5.1k','CC2','GND','02_usb',(55,110))
r('R5','22k','CC1','CC1_ADC','02_usb',(43,106));r('R6','22k','CC2','CC2_ADC','02_usb',(55,106))
c('C4','4.7n','CC1_ADC','GND','02_usb',(43,102));c('C5','4.7n','CC2_ADC','GND','02_usb',(55,102))
r('R7','22k','USB_DP_CONN','USB_DP','02_usb',(61,110));r('R8','22k','USB_DM_CONN','USB_DM','02_usb',(61,114))
# Correct USB termination is 22 ohm, not the CC filter value.
for d in parts:
 if d['ref'] in ('R7','R8'):d.update(value='22',mpn='RC0805FR-0722RL',notes='22 ohm source damping; tune only after SI measurement')
esd=[(1,'IO1','USB_DP_CONN'),(2,'GND','GND'),(3,'IO2','USB_DM_CONN'),(4,'IO2','USB_DM_CONN'),(5,'VBUS','VBUS'),(6,'IO1','USB_DP_CONN')]
add('U2','USBLC6-2SC6','Package_TO_SOT_SMD:SOT-23-6',esd,'02_usb',(49,112),'USBLC6-2SC6','STMicroelectronics','https://www.st.com/resource/en/datasheet/usblc6-2.pdf','Flow-through ESD device; duplicate IO pins both connected')
add('U3','USBLC6-2SC6','Package_TO_SOT_SMD:SOT-23-6',[(1,'IO1','CC1'),(2,'GND','GND'),(3,'IO2','CC2'),(4,'IO2','CC2'),(5,'VBUS','VBUS'),(6,'IO1','CC1')],'02_usb',(49,105),'USBLC6-2SC6','STMicroelectronics','https://www.st.com/resource/en/datasheet/usblc6-2.pdf','CC ESD candidate; does not provide overvoltage or powered-off ADC isolation')
# Power: delayed input switch keeps 10uF buck input behind a controlled rise.
add('F1','3A hold PTC','Fuse:Fuse_1812_4532Metric',[(1,'IN','VBUS'),(2,'OUT','+5V_FUSED')],'00_power',(38,114),'MF-MSMF300/16X-2','Bourns','https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf','Temperature derating and trip-energy coordination must be reviewed')
c('C6','4.7u','+5V_FUSED','GND','00_power',(38,108))
add('U4','TPS22918DBVR input slew','Package_TO_SOT_SMD:SOT-23-6',[(1,'VIN','+5V_FUSED','power_in'),(2,'GND','GND','power_in'),(3,'ON','+5V_FUSED','input'),(4,'CT','INPUT_CT','passive'),(5,'QOD',None),(6,'VOUT','+5V','power_out')],'00_power',(38,101),'TPS22918DBVR','Texas Instruments',SW,'Always-on controlled-rise input switch; 2A ceiling requires load derating')
c('C7','10n','INPUT_CT','GND','00_power',(34,96));c('C8','10u','+5V','GND','00_power',(45,96),True)
add('U5','AP63203WU-7 3V3 buck','Package_TO_SOT_SMD:TSOT-23-6',[(1,'FB','+3V3','input'),(2,'EN','+5V','input'),(3,'VIN','+5V','power_in'),(4,'GND','GND','power_in'),(5,'SW','SW_NODE','passive'),(6,'BST','BST','passive')],'00_power',(49,93),'AP63203WU-7','Diodes Incorporated',BUCK,'2A fixed 3.3V. Sourcing contradictory; not release-qualified.',0.765,'Mouser Spain 0; Europe cached listing reports 17010; live reconfirmation required')
c('C9','100n','BST','SW_NODE','00_power',(49,89))
add('L1','3.9uH','Inductor_SMD:L_Bourns-SRN6028',[(1,'1','SW_NODE'),(2,'2','+3V3')],'00_power',(56,93),'SRN6028C-3R9M','Bourns','https://www.bourns.com/data/global/pdfs/SRN6028C.pdf','C series selected, not obsolete SRN6028. Native footprint is old series; comparison pending.',None,'DigiKey listing found, quantity/price not extracted')
c('C10','22u','+3V3','GND','00_power',(63,92),True);c('C11','22u','+3V3','GND','00_power',(63,96),True)
add('U6','TPS22918DBVR audio gate','Package_TO_SOT_SMD:SOT-23-6',[(1,'VIN','+5V','power_in'),(2,'GND','GND','power_in'),(3,'ON','PERIPH_EN','input'),(4,'CT','AUDIO_CT'),(5,'QOD',None),(6,'VOUT','+5V_AUDIO','power_out')],'04_audio',(43,86),'TPS22918DBVR','Texas Instruments',SW,'Default off; enable only on stable 3A advertisement and firmware budget')
add('U7','TPS22918DBVR display gate','Package_TO_SOT_SMD:SOT-23-6',[(1,'VIN','+3V3','power_in'),(2,'GND','GND','power_in'),(3,'ON','PERIPH_EN','input'),(4,'CT','DISPLAY_CT'),(5,'QOD',None),(6,'VOUT','+3V3_DISPLAY','power_out')],'03_display',(91,44),'TPS22918DBVR','Texas Instruments',SW,'Display and audio enable together; powered-off signal backfeed review pending')
r('R9','100k','PERIPH_EN','GND','04_audio',(44,81));c('C12','10n','AUDIO_CT','GND','04_audio',(39,84));c('C13','10n','DISPLAY_CT','GND','03_display',(91,39))
c('C14','22u','+5V_AUDIO','GND','04_audio',(44,76),True);c('C15','22u','+3V3_DISPLAY','GND','03_display',(96,40),True)
# Candidate NXP pin map, verified in UM12018 and AN14776; mechanical mate remains unverified.
display=['+3V3_DISPLAY','GND','I2C_SCL','I2C_SDA',None,'+3V3_DISPLAY','LCD_RESET','LCD_DC','GND','LCD_WR','+3V3_DISPLAY',None]+[f'LCD_D{i}' for i in range(8)]+[None]*8
header('J2','DISPLAY CANDIDATE / NOT RELEASED',display,'03_display',(102,36),2)
r('R10','33','LCD_WR_SRC','LCD_WR','03_display',(85,48));r('R11','33','LCD_DC_SRC','LCD_DC','03_display',(85,52))
r('R12','100','EN','LCD_RESET','03_display',(91,48));r('R13','4.7k','+3V3','I2C_SCL','03_display',(90,58));r('R14','4.7k','+3V3','I2C_SDA','03_display',(90,62))
# Cable connectors are our defined harness pin order, not direct mechanical breakout footprints.
header('J3','LEFT AMP HARNESS',['+5V_AUDIO','GND','AMP_LEFT_SD',None,'I2S_TX','I2S_BCLK','I2S_WS'],'04_audio',(35,64))
header('J4','RIGHT AMP HARNESS',['+5V_AUDIO','GND','AMP_RIGHT_SD',None,'I2S_TX','I2S_BCLK','I2S_WS'],'04_audio',(52,66))
r('R15','82k','+5V_AUDIO','AMP_LEFT_SD','04_audio',(36,59));r('R16','560k','+5V_AUDIO','AMP_RIGHT_SD','04_audio',(51,61),'RC0805FR-07560KL')
r('R17','33','I2S_BCLK_SRC','I2S_BCLK','04_audio',(76,64));r('R18','33','I2S_WS_SRC','I2S_WS','04_audio',(76,68));r('R19','33','I2S_TX_SRC','I2S_TX','04_audio',(76,72))
header('J5','MIC HARNESS',['+3V3','GND','I2S_BCLK','MIC_DATA','I2S_WS','GND'],'05_microphone',(35,36))
c('C16','100n','+3V3','GND','05_microphone',(41,47));c('C17','1u','+3V3','GND','05_microphone',(41,43))
# six individually labeled controls on one ADC; no simultaneous-key support promised.
r('R20','10k','+3V3','KEY_ADC','06_buttons',(94,88));c('C18','100n','KEY_ADC','GND','06_buttons',(94,92))
for i,(name,res,xy) in enumerate([('UP','0',(113,85)),('DOWN','1k',(113,105)),('LEFT','2.2k',(103,95)),('RIGHT','4.7k',(123,95)),('OK','10k',(113,95)),('BACK','22k',(103,110))]):
 net='KEY_'+name
 add('SW'+str(i+1),name,'Button_Switch_THT:SW_PUSH_6mm',[(1,'A','KEY_ADC'),(2,'B',net)],'06_buttons',xy,'B3F-1000','Omron','https://components.omron.com/us-en/products/switches/B3F','6mm through-hole tact; verify actuator height and native pad fit')
 r('R'+str(21+i),res,net,'GND','06_buttons',(xy[0]-2,xy[1]+6))
# SPI microSD is a cable breakout option; no unverified socket land pattern.
header('J6','3V3 SD HARNESS',['+3V3','GND','SD_SCK','SD_MOSI','SD_MISO','SD_CS'],'07_storage',(84,76))
r('R27','33','SD_SCK_SRC','SD_SCK','07_storage',(80,84));r('R28','33','SD_MOSI_SRC','SD_MOSI','07_storage',(80,88));r('R29','10k','+3V3','SD_CS','07_storage',(89,78));r('R30','10k','+3V3','SD_MISO','07_storage',(89,82))
c('C19','22u','+3V3','GND','07_storage',(89,86),True)
header('J7','UART RECOVERY',['GND','UART_TX','UART_RX','EN','BOOT','+3V3'],'10_debug',(73,106))
header('J8','I2C EXPANSION',['+3V3','GND','I2C_SCL','I2C_SDA'],'09_expansion',(65,105))
for ref,name,net,xy in [('SW7','BOOT','BOOT',(88,110)),('SW8','RESET','EN',(88,101))]:
 add(ref,name,'Button_Switch_THT:SW_PUSH_6mm',[(1,'A',net),(2,'B','GND')],'10_debug',xy,'B3F-1000','Omron','https://components.omron.com/us-en/products/switches/B3F')
r('R31','1k','STATUS','LED_A','10_debug',(68,99))
add('D1','STATUS amber','LED_SMD:LED_0805_2012Metric',[(1,'K','GND'),(2,'A','LED_A')],'10_debug',(73,99),'LTST-C170KFKT','Lite-On','https://optoelectronics.liteon.com/en-global/Led/LED-Lamp','Sourcing and polarity audit pending')
# Exposed, real 2mm probe pads, away from small IC leads.
for i,(net,xy) in enumerate([('VBUS',(34,111)),('+5V',(34,90)),('+3V3',(65,89)),('GND',(65,85)),('EN',(81,101)),('BOOT',(81,105)),('+3V3_DISPLAY',(98,44)),('+5V_AUDIO',(47,77)),('I2C_SCL',(95,58)),('I2C_SDA',(95,62)),('I2S_BCLK',(69,68)),('I2S_WS',(69,72)),('MIC_DATA',(43,39)),('SD_SCK',(79,80)),('PERIPH_EN',(46,81)),('CC1_ADC',(40,99)),('CC2_ADC',(58,102))]):
 add('TP'+str(i+1),net,'TestPoint:TestPoint_Pad_D2.0mm',[(1,net,net)],'10_debug',xy,'PCB TEST PAD','PCB','',note='Bare copper probe pad, no purchased component')
for i,xy in enumerate([(34,33),(126,33),(34,116),(126,116)]):
 add('H'+str(i+1),'M3 mounting','MountingHole:MountingHole_3.2mm_M3',[],'10_debug',xy,'NPTH 3.2mm','PCB','',note='No copper; screw head keepout still requires mechanical audit')
for i,net in enumerate(['+5V_FUSED','GND','+3V3']):
 add('#FLG'+str(i+1),'PWR_FLAG','',[(1,'SUPPLIED',net,'power_out')],'00_power',(0,0),note='Logical source declaration: USB connector through fuse or verified buck through output inductor; no physical part')
# Placement corrections from the first native DRC, before routing.
reposition={'SW4':(120,95),'R21':(98,76),'R22':(98,80),'R23':(98,84),'R24':(98,88),'R25':(98,100),'R26':(98,110),'R1':(54,61),'C1':(58,63),'C3':(68,63),'F1':(40,114),'U2':(49,109),'J5':(35,39),'TP1':(33,106),'TP8':(48,73),'TP15':(48,81),'TP16':(34,99),'TP17':(60,103),'J7':(73,103)}
reposition.update({'SW1':(107,85),'SW2':(107,105),'SW3':(95,95),'SW4':(119,95),'SW5':(107,95),'SW6':(95,110),'R1':(51,56),'C3':(71,64),'F1':(40.5,110),'C6':(37,106),'R21':(116,79),'R22':(120,109),'R23':(90,95),'R24':(123,104),'R25':(103,89),'R26':(90,114),'R20':(90,90),'C18':(90,92.5)})
reposition.update({'SW7':(80,110),'SW8':(78,94),'R3':(40,115)})
reposition.update({'TP5':(77,101),'C3':(53.7,40.86),'C2':(52,45),'R1':(52,50),'C1':(52,54),'C8':(45.5,91),'C9':(52,92.8),'C10':(62,91),'C11':(62,95)})
reposition.update({'C8':(44.2,94.1),'C9':(52.7,92.8),'L1':(57.5,93),'C10':(65.3,91.5),'C11':(65.3,95.5),'TP3':(70,87),'TP5':(77,106)})
for d in parts:
 if d['ref'] in reposition:d['xy']=reposition[d['ref']]
 if d['ref'] in ('C3','C2','C8'):d['angle']=180
 if d['ref']=='C9':d['angle']=270

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
setpins('U4',[(1,'DEVSLP','GND','input'),(2,'PGOOD','POWER_GOOD','open_collector'),(3,'PGTH','PGTH','input')]+[(i,'OUT','+5V','power_out' if i==4 else 'passive') for i in range(4,9)]+[(i,'IN','+5V_FUSED','power_in') for i in range(9,14)]+[(14,'EN_UVLO','EFUSE_EN','input'),(15,'OVP','OVP','input'),(16,'GND','GND','power_in'),(17,'ILIM','ILIM'),(18,'dVdT','SLEW'),(19,'IMON','IMON','output'),(20,'FLT','POWER_FAULT','open_collector'),(21,'EP','GND','power_in')])
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
add('U9','SN74LVC2G02DCTR dual NOR','Package_SO:SSOP-8_2.95x2.8mm_P0.65mm',[(1,'1A','CC_OUT1','input'),(2,'1B','CC_OUT2','input'),(3,'2Y','CC_NOT_3A','output'),(4,'GND','GND','power_in'),(5,'2A','CC_3A_OK','input'),(6,'2B','CC_3A_OK','input'),(7,'1Y','CC_3A_OK','output'),(8,'VCC','+3V3_AON','power_in')],'02_usb',(59,107),'SN74LVC2G02DCTR','Texas Instruments','https://www.ti.com/lit/ds/symlink/sn74lvc2g02.pdf','3A truth table hardware interlock; no MCU sampling thresholds')
add('Q1','2N7002 eFuse inhibit','Package_TO_SOT_SMD:SOT-23',[(1,'G','CC_NOT_3A','input'),(2,'S','GND'),(3,'D','EFUSE_EN')],'00_power',(43,88),'2N7002,215','Nexperia','https://assets.nexperia.com/documents/data-sheet/2N7002.pdf','Pulls eFuse enable below UVLO when unattached/default/1.5A')
add('D2','SMBJ10A VBUS TVS','Diode_SMD:D_SMB',[(1,'K','+5V_FUSED'),(2,'A','GND')],'00_power',(38,106),'SMBJ10A','Littelfuse','https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj10a','17V rated pulse clamp below eFuse 20V absolute maximum; transient energy qualification pending')
for ref,val,a,b,xy in [('R32','47k','+3V3_AON','CC_OUT1',(62,110)),('R33','47k','+3V3_AON','CC_OUT2',(62,113)),('R34','887k','+5V_FUSED','VBUS_DET',(57,116)),('R35','34.8k','ILIM','GND',(34,98)),('R36','309k','+5V_FUSED','EFUSE_EN',(43,91)),('R37','100k','EFUSE_EN','GND',(43,94)),('R38','475k','+5V_FUSED','OVP',(34,91)),('R39','100k','OVP','GND',(34,94)),('R40','332k','+5V','PGTH',(44,99)),('R41','100k','PGTH','GND',(44,102)),('R42','10k','IMON','GND',(34,102)),('R43','10k','+3V3','POWER_GOOD',(46,85)),('R44','10k','+3V3','POWER_FAULT',(46,81)),('R45','10k','+3V3','DISPLAY_SD_CS',(102,44)),('R46','33','I2S_BCLK_SRC','MIC_BCLK',(73,84)),('R47','33','I2S_WS_SRC','MIC_WS',(73,80)),('R48','100k','AMP_BCLK','GND',(56,58)),('R49','100k','AMP_WS','GND',(59,58)),('R50','100k','AMP_TX','GND',(62,58))]:
 r(ref,val,a,b,'00_power' if int(ref[1:]) in range(35,45) else '03_display' if ref=='R45' else '04_audio' if int(ref[1:])>=46 else '02_usb',xy)
for ref in ('R38','R39'):
 d=next(d for d in parts if d['ref']==ref);d['mpn']='RT0805BRD07'+('475KL' if ref=='R38' else '100KL');d['notes']='0.1% OVP threshold divider'
for ref,val,a,xy in [('C20','100n','+5V_FUSED',(37,83)),('C21','1u','+3V3_AON',(37,91)),('C22','100n','+3V3_AON',(55,108)),('C23','100n','+3V3_AON',(63,104)),('C24','100n','+3V3',(57,65)),('C25','100n','+5V',(68,65))]:c(ref,val,a,'GND','00_power' if int(ref[1:])<=21 else '02_usb' if int(ref[1:])<=23 else '04_audio',xy)
add('C26','47n',CFP,[(1,'1','SLEW'),(2,'2','GND')],'00_power',(39,96),'GRM21BR71H473KA01L','Murata','https://www.murata.com/en-global/products/capacitor/mlcc','50V X7R; nominal ~19.5ms eFuse ramp')
next(d for d in parts if d['ref']=='J2')['pins'].append(dict(num='MP',name='MOUNT',net='GND',type='passive'))
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

extra={'TP1':(33,112),'TP2':(33,83),'TP4':(49,81),'TP7':(108,48),'TP3':(51,84),'U9':(60,115),'C23':(65,115),'U2':(48,110),'U3':(55,116.5),'C6':(33,105),'D2':(38,105),'F1':(39,112),'C21':(38,92),'C25':(70,62),'R50':(63,56),'R49':(59.5,56),'R48':(56,56),'C1':(78,91),'D1':(73,74),'SW7':(84,114),'C9':(68.3,43.6)}
for d in parts:
 if d['ref'] in extra:d['xy']=extra[d['ref']]
extra2={'R34':(73,114),'U9':(63,115),'C23':(68,118),'U3':(56.5,116.5),'C9':(66.7,43),'TP4':(47,77),'TP3':(52,84),'TP1':(33,109),'F1':(39,110),'C6':(33,104),'R42':(44,107),'R33':(62,111),'SW7':(84,110)}
for d in parts:
 if d['ref'] in extra2:d['xy']=extra2[d['ref']]
# Schematic source, readable per-subsystem sheets and local library with true electrical pin types.
def effects(size=1,hide=False):return f'(effects (font (size {size} {size}))'+(' (hide yes)' if hide else '')+')'
def prop(name,value,x,y,hide=False,size=1):return f'(property {q(name)} {q(value)} (at {x} {y} 0) {effects(size,hide)})'
def geom(d):
 n=len(d['pins']); left=(n+1)//2; pitch=2.54; h=max(7.62,(left+1)*pitch); w=15.24 if n>2 else 7.62
 loc=[]
 for i,p in enumerate(d['pins']):
  side=0 if i<left else 1; j=i if side==0 else i-left
  loc.append((p,(-w-5.08 if side==0 else w+5.08),h/2-2.54-j*pitch,0 if side==0 else 180))
 return w,h,loc
def libsymbol(d):
 w,h,loc=geom(d);name=d['ref']; ref='TP' if name.startswith('TP') else 'SW' if name.startswith('SW') else name[0]
 draw=f'(rectangle (start {-w} {h/2}) (end {w} {-h/2}) (stroke (width 0.254) (type default)) (fill (type background)))'
 ps=[]
 for p,x,y,ang in loc:
  ps.append(f'(pin {p["type"]} line (at {x} {y} {ang}) (length 5.08) (name {q(p["name"])} {effects(.85)}) (number {q(p["num"])} {effects(.85)}))')
 bom='no' if name.startswith(('TP','H','#')) else 'yes'; onboard='yes' if d['footprint'] else 'no'
 return f'(symbol {q("Nexus:"+name)} (pin_names (offset 0.5)) (in_bom {bom}) (on_board {onboard}) {prop("Reference",ref,0,h/2+3)} {prop("Value",d["value"],0,-h/2-3)} (symbol {q(name+"_0_1")} {draw}) (symbol {q(name+"_1_1")} {" ".join(ps)}))'
sheetnames=sorted({d['sheet'] for d in parts});rootuid=uid('root');lib=' '.join(libsymbol(d) for d in parts)
def text(s,x,y,size=1.2):return f'(text {q(s)} (at {x} {y} 0) {effects(size)} (uuid {q(uid("text/"+s+str(x)+str(y)))}) )'
def headerdoc(id,title):return f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(id)}) (paper "A3") (title_block (title {q("NEXUS PEAR REV A - "+title)}) (date "2026-10-07") (rev "A CANDIDATE") (company "Engineering prototype / DO NOT ORDER") (comment 1 "Read DESIGN_REVIEW_REVA.md before fabrication"))'
for sn in sheetnames:
 ds=[d for d in parts if d['sheet']==sn];sid=uid(sn);s=[headerdoc(sid,sn),'(lib_symbols '+ ' '.join(libsymbol(d) for d in ds)+')',text('DO NOT ORDER - no smoke speedruns. Read the design review.',200,16,1.6)]
 # Pack across columns with enough height for per-pin global labels.
 x=65;y=38;col=0
 for d in ds:
  w,h,loc=geom(d);needed=h+22
  if y+needed>270:col+=1;x=65+col*98;y=38
  x=round(x/1.27)*1.27;cy=round((y+h/2+7)/1.27)*1.27;d['sch_xy']=[x,cy];d['sheet_uuid']=sid
  fpval='Nexus:'+d['footprint'].split(':')[1] if d['footprint'] else ''
  props=[prop('Reference',d['ref'],x,cy-h/2-5),prop('Value',d['value'],x,cy-h/2-2.5,size=.9),prop('Footprint',fpval,x,cy,True),prop('Datasheet',d['datasheet'],x,cy,True),prop('MPN',d['mpn'],x,cy,True),prop('Description',d['notes'],x,cy,True)]
  inst=f'(instances (project "nexus-pear-reva" (path {q("/"+rootuid+"/"+sid)} (reference {q(d["ref"])}) (unit 1))))'
  pinids=' '.join(f'(pin {q(p["num"])} (uuid {q(uid(d["ref"]+"/pin/"+p["num"]))}))' for p in d['pins'])
  physical='yes' if d['footprint'] else 'no'
  bom='no' if d['ref'].startswith(('TP','H','#')) else 'yes'
  s.append(f'(symbol (lib_id {q("Nexus:"+d["ref"])}) (at {x} {cy} 0) (unit 1) (in_bom {bom}) (on_board {physical}) (dnp no) (uuid {q(d["uuid"])}) {" ".join(props)} {pinids} {inst})')
  for p,px,py,ang in loc:
   ax=x+px;ay=cy-py;net=p['net']
   if net is None:s.append(f'(no_connect (at {ax} {ay}) (uuid {q(uid(d["ref"]+"/nc/"+p["num"]))}))');continue
   ex=ax+(-5.08 if ang==0 else 5.08);labang=0 if ang==0 else 180
   s.append(f'(wire (pts (xy {ax} {ay}) (xy {ex} {ay})) (stroke (width 0) (type default)) (uuid {q(uid(d["ref"]+"/wire/"+p["num"]))}))')
   s.append(f'(global_label {q(net)} (shape bidirectional) (at {ex} {ay} {labang}) {effects(.9)} (uuid {q(uid(d["ref"]+"/label/"+p["num"]))}) {prop("Intersheetrefs","${INTERSHEET_REFS}",ex,ay,True)})')
  y+=needed
 s.append('(embedded_fonts no))');(PRO/(sn+'.kicad_sch')).write_text('\n'.join(s),encoding='utf8')
overview=[headerdoc(rootuid,'System overview'),'(lib_symbols)',text('NEXUS PEAR REV A',210,23,3),text('ESP32-S3 external antenna / remote AI / stereo I2S / documented SPI IPS',210,32,1.4),text('DO NOT ORDER: bench qualification and complete purchasing quote pending.',210,42,1.6)]
for i,sn in enumerate(sheetnames):
 x=45+(i%3)*125;y=62+(i//3)*46
 overview.append(f'(sheet (at {x} {y}) (size 105 31) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {q(uid(sn))}) {prop("Sheetname",sn,x,y-2)} {prop("Sheetfile",sn+".kicad_sch",x,y+34)} (instances (project "nexus-pear-reva" (path {q("/"+rootuid)} (page {q(i+2)})))))')
overview+=['(embedded_fonts no))'];(PRO/'nexus-pear-reva.kicad_sch').write_text('\n'.join(overview),encoding='utf8')
# Separate root library for editable project symbols.
ls=lib.replace('"Nexus:','"');(PRO/'Nexus.kicad_sym').write_text('(kicad_symbol_lib (version 20250114) (generator "kicad_symbol_editor") '+ls+')',encoding='utf8')
(PRO/'sym-lib-table').write_text('(sym_lib_table (lib (name "Nexus") (type "KiCad") (uri "${KIPRJMOD}/Nexus.kicad_sym") (options "") (descr "Project symbols with explicit pad numbering")))',encoding='utf8')
(PRO/'Nexus.pretty').mkdir(exist_ok=True)
for d in parts:
 if not d['footprint']:continue
 libname,fp=d['footprint'].split(':');src=root/'footprints'/f'{libname}.pretty'/f'{fp}.kicad_mod'
 if not src.exists():raise FileNotFoundError(src)
 shutil.copy2(src,PRO/'Nexus.pretty'/src.name)
ep=PRO/'Nexus.pretty/ESP32-S3-WROOM-1U.kicad_mod'
ep.write_text(ep.read_text(encoding='utf8').replace('(drill 0.2)','(drill 0.3)'),encoding='utf8')
(PRO/'fp-lib-table').write_text('(fp_lib_table (lib (name "Nexus") (type "KiCad") (uri "${KIPRJMOD}/Nexus.pretty") (options "") (descr "Snapshot of KiCad 10.0.1 native footprints; audit status in docs")))',encoding='utf8')
(PRO/'nexus-pear-reva.kicad_pro').write_text(json.dumps({'meta':{'filename':'nexus-pear-reva.kicad_pro','version':1},'board':{'design_settings':{'defaults':{},'rules':{'min_clearance':0.2,'min_track_width':0.2,'min_via_diameter':0.6,'min_through_hole_diameter':0.3,'min_copper_edge_clearance':0.3},'rule_severities':{},'drc_exclusions':[]}},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.6,'via_drill':0.3,'diff_pair_width':0.2,'diff_pair_gap':0.2,'diff_pair_via_gap':0.25}]},'erc':{'erc_exclusions':[]}},indent=2),encoding='utf8')
(OUT/'design_data.json').write_text(json.dumps({'root_uuid':rootuid,'parts':parts,'status':'DO NOT ORDER'},indent=2),encoding='utf8')
print(f'Created {len(parts)} components and {len(sheetnames)} subsystem sheets in {PRO}')
