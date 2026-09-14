from pathlib import Path
from copy import deepcopy
import uuid
from sexp import *
ROOT=Path(__file__).resolve().parents[1]
LIB=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols')
s=parse((ROOT/'backup_original/I2C_Sensor_Board.kicad_sch').read_text())
libs=child(s,'lib_symbols'); rootid=value(child(s,'uuid')[1])
def uid(): return str(uuid.uuid4())
def add(txt):
    n=parse(txt); s.append(n); return n
def prop(n,name): return next(p for p in children(n,'property') if value(p[1])==name)
syms={value(prop(n,'Reference')[2]):n for n in children(s,'symbol')}
def loadlib(lib,name):
    n=deepcopy(next(x for x in children(parse((LIB/(lib+'.kicad_sym')).read_text()),'symbol') if value(x[1])==name))
    n[1]=q(lib+':'+name); libs.append(n)
loadlib('Device','LED'); loadlib('power','PWR_FLAG')
for ref,changes in {
    'C1':{'Value':'1uF'},
    'C2':{'Footprint':'Capacitor_SMD:C_0603_1608Metric'},
    'C3':{'Footprint':'Capacitor_SMD:CP_Elec_6.3x5.4'},
    'C5':{'Value':'10nF'},
    'R1':{'Value':'4.99k'},
    'D1':{'Value':'SS14','Footprint':'Diode_SMD:D_SMA','Datasheet':'https://www.vishay.com/docs/88746/ss12.pdf'},
    'J1':{'Footprint':'Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical'},
}.items():
    for key,val in changes.items(): prop(syms[ref],key)[2]=q(val)
def label(name,x,y):
    add(f'(label {q(name)} (at {x} {y} 0) (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid {q(uid())}))')
def wire(x,y,xx,yy):
    add(f'(wire (pts (xy {x} {y}) (xy {xx} {yy})) (stroke (width 0) (type default)) (uuid {q(uid())}))')
def inst(lib,ref,val,fp,x,y):
    return add(f'''(symbol (lib_id {q(lib)}) (at {x} {y} 0) (unit 1)
      (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid())})
      (property "Reference" {q(ref)} (at {x+3} {y-2} 0) (effects (font (size 1.27 1.27))))
      (property "Value" {q(val)} (at {x+3} {y} 0) (effects (font (size 1.0 1.0))))
      (property "Footprint" {q(fp)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (instances (project "I2C_Sensor_Board" (path {q('/'+rootid)} (reference {q(ref)}) (unit 1)))))''')
def text(txt,x,y): add(f'(text {q(txt)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {q(uid())}))')
# Direct pin labels repair the disconnected regulator ground and expose ETR signals.
wire(96.52,68.58,96.52,73.66); label('GND',96.52,73.66)
label('EVENT',266.7,71.12); label('ALARM',266.7,73.66)
for i,(x,y,net) in enumerate([(63.5,58.42,'+5V'),(81.28,77.47,'GND'),(88.9,58.42,None)],1):
    inst('power:PWR_FLAG',f'#FLG0{i}','PWR_FLAG','',x,y)
# Custom DS1683 symbol: pin mapping verified against ADI data sheet, page 4.
pins=[('1','EVENT','input',-10.16,5.08,0),('2','NC','no_connect',-10.16,2.54,0),
      ('3','ALARM','open_collector',-10.16,0,0),('4','GND','power_in',0,-10.16,90),
      ('5','SCL','input',10.16,-2.54,180),('6','SDA','bidirectional',10.16,0,180),
      ('7','NC','no_connect',10.16,2.54,180),('8','VCC','power_in',0,10.16,270)]
pinstr=''.join(f'(pin {typ} line (at {x} {y} {ang}) (length 2.54) (name {q(name)} (effects (font (size 1.0 1.0)))) (number {q(num)} (effects (font (size 1.0 1.0)))))' for num,name,typ,x,y,ang in pins)
custom=parse(f'''(symbol "I2C_Sensor_Board:DS1683S+" (pin_names (offset 0.8)) (in_bom yes) (on_board yes)
  (property "Reference" "U" (at 0 0 0) (effects (font (size 1.27 1.27))))
  (property "Value" "DS1683S+" (at 0 0 0) (effects (font (size 1.27 1.27))))
  (property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
  (property "Datasheet" "https://www.analog.com/media/en/technical-documentation/data-sheets/DS1683.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
  (symbol "DS1683S+_0_1" (rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width 0.254) (type default)) (fill (type background))))
  (symbol "DS1683S+_1_1" {pinstr}))''')
libs.append(custom)
external=deepcopy(custom); external[1]=q('DS1683S+')
(ROOT/'I2C_Sensor_Board.kicad_sym').write_text(dump(['kicad_symbol_lib',['version','20241209'],['generator',q('kicad_symbol_editor')],external])+'\n')
(ROOT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "I2C_Sensor_Board") (type "KiCad") (uri "${KIPRJMOD}/I2C_Sensor_Board.kicad_sym") (options "") (descr "DS1683, datasheet pin mapping")))\n')
inst('I2C_Sensor_Board:DS1683S+','U4','DS1683S+','Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',96.52,137.16)
for num,name,typ,px,py,angle in pins:
    x,y=round(96.52+px,4),round(137.16-py,4)
    if typ=='no_connect': add(f'(no_connect (at {x} {y}) (uuid {q(uid())}))')
    else:
        nx=x-5.08 if px<0 else x+5.08 if px>0 else x
        ny=y-5.08 if py>7.62 else y+5.08 if py<-7.62 else y
        wire(x,y,round(nx,4),round(ny,4)); label('+3V3' if name=='VCC' else name,round(nx,4),round(ny,4))
inst('Device:C','C6','10nF','Capacitor_SMD:C_0402_1005Metric',129.54,134.62)
label('+3V3',129.54,130.81); label('GND',129.54,138.43)
text('ETR - DS1683 / alarm indicator',66.04,114.3)
for ref,val,x,top,bottom in [('R3','390',60.96,'+3V3','LED_A'),('R4','4.7k',170.18,'+3V3','SDA'),('R5','4.7k',193.04,'+3V3','SCL'),('R6','10k',215.9,'+3V3','ALERT')]:
    inst('Device:R',ref,val,'Resistor_SMD:R_0402_1005Metric',x,134.62)
    label(top,x,130.81); label(bottom,x,138.43)
inst('Device:LED','D2','LED_Red','LED_SMD:LED_0603_1608Metric',60.96,149.86)
label('ALARM',57.15,149.86); label('LED_A',64.77,149.86)
text('I2C pull-ups + ALERT pull-up',165.1,121.92)
text('5V input; 3V3 output. R1=4.99k / R2=3k: nominal 3.30V.',66.04,165.1)
text('J1: 1 GND / 2 +5V / 3 GND / 4 +3V3 / 5 ALERT',66.04,170.18)
text('     6 EVENT / 7 WP / 8 ALARM / 9 SCL / 10 SDA',66.04,175.26)
(ROOT/'I2C_Sensor_Board.kicad_sch').write_text(dump(s)+'\n')
print('Completed schematic and project-local DS1683 library.')
