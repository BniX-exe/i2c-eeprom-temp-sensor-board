from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
b=p.LoadBoard(str(ROOT/'I2C_Sensor_Board.kicad_pcb'))
assert p.ImportSpecctraSES(b,str(ROOT/'reports/routed.ses'))
mm=p.FromMM
def xy(x,y):return p.VECTOR2I(mm(x),mm(y))
for item in b.GetDrawings():
    if isinstance(item,p.PCB_TEXT):
        x=p.ToMM(item.GetPosition().x)
        if abs(x-101.5)<.01:item.SetPosition(xy(101.1,p.ToMM(item.GetPosition().y)))
        elif abs(x-109)<.01:item.SetPosition(xy(109.6,p.ToMM(item.GetPosition().y)))
for layer in [p.F_Cu,p.B_Cu]:
    z=p.ZONE(b); z.SetLayer(layer); z.SetNetCode(b.FindNet('GND').GetNetCode())
    z.SetLocalClearance(mm(.2)); z.SetThermalReliefGap(mm(.2)); z.SetThermalReliefSpokeWidth(mm(.2)); z.SetMinThickness(mm(.2))
    outline=z.Outline(); outline.NewOutline()
    for x,y in [(100.4,100.4),(141.6,100.4),(141.6,129.6),(100.4,129.6)]: outline.Append(mm(x),mm(y))
    b.Add(z)
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(ROOT/'I2C_Sensor_Board.kicad_pcb'),b)
print('Routed board saved:',len(list(b.GetTracks())),'tracks/vias; GND pour on both layers.')
