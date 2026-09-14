from pathlib import Path
from sexp import *
import uuid
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'I2C_Sensor_Board.kicad_sch'; s=parse(p.read_text())
def prop(n,name):return next((x for x in children(n,'property') if value(x[1])==name),None)
syms={value(prop(n,'Reference')[2]):n for n in children(s,'symbol')}
for ref,n in syms.items():
    if ref.startswith('#FLG'):
        for name in ['Reference','Value']: child(prop(n,name),'effects').append(['hide','yes'])
for ref in ['R3','R4','R5','R6','C6']:
    n=syms[ref]; x=float(child(n,'at')[1]); y=float(child(n,'at')[2])
    for name,dy in [('Reference',-1.27),('Value',1.27)]:
        child(prop(n,name),'at')[1:3]=[str(x+3.81),str(y+dy)]
        child(prop(n,name),'effects').append(['justify','left'])
# Move pullups away from the temperature sensor ground symbol.
for ref in ['R4','R5','R6']:
    n=syms[ref]; x=float(child(n,'at')[1]); child(n,'at')[2]=str(float(child(n,'at')[2])+12.7)
    for field in children(n,'property'):
        at=child(field,'at')
        if at: at[2]=str(float(at[2])+12.7)
    for lab in children(s,'label'):
        at=child(lab,'at')
        if abs(float(at[1])-x)<.001 and 130<float(at[2])<140: at[2]=str(float(at[2])+12.7)
for t in children(s,'text'):
    if value(t[1])=='I2C pull-ups + ALERT pull-up': child(t,'at')[2]='134.62'
for name,y in [('Reference',125.73),('Value',128.27)]:
    field=prop(syms['U4'],name); child(field,'at')[1:3]=['106.68',str(y)]; child(field,'effects').append(['justify','left'])
for name,y in [('Reference',144.78),('Value',147.32)]: child(prop(syms['D2'],name),'at')[1:3]=['60.96',str(y)]
def extend(lab,xx,yy):
    at=child(lab,'at'); x,y=at[1:3]
    s.append(parse(f'(wire (pts (xy {x} {y}) (xy {xx} {yy})) (stroke (width 0) (type default)) (uuid {q(uuid.uuid4())}))'))
    at[1:3]=[str(xx),str(yy)]
for lab in children(s,'label'):
    at=child(lab,'at'); x,y=float(at[1]),float(at[2])
    if abs(y-149.86)<.001:
        if abs(x-57.15)<.001:extend(lab,49.53,y)
        elif abs(x-64.77)<.001:extend(lab,72.39,y)
    elif x in [60.96,129.54,170.18,193.04,215.9]:
        if round(y,2) in [130.81,143.51]:extend(lab,x,round(y-2.54,4))
        elif round(y,2) in [138.43,151.13]:extend(lab,x,round(y+2.54,4))
s.append(['title_block',['title',q('I2C Sensor Board - EEPROM / TMP102 / DS1683')],['date',q('2026-10-05')],['rev',q('A')]])
p.write_text(dump(s)+'\n')
