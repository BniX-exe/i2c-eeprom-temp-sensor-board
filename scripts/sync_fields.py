from pathlib import Path
from sexp import *
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
s=parse((ROOT/'I2C_Sensor_Board.kicad_sch').read_text())
fields={}
for n in children(s,'symbol'):
    props={value(x[1]):value(x[2]) for x in children(n,'property')}; fields[props['Reference']]=props
b=p.LoadBoard(str(ROOT/'I2C_Sensor_Board.kicad_pcb'))
for fp in b.GetFootprints():
    for key in ['Description','Datasheet']:
        f=fp.GetField(key)
        if f: f.SetText(fields[fp.GetReference()].get(key,'')); f.SetVisible(False)
p.SaveBoard(str(ROOT/'I2C_Sensor_Board.kicad_pcb'),b)
