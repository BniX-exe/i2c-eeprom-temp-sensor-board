"""Generate a placed KiCad board from the checked schematic XML netlist.
Run using the Python bundled with KiCad (pcbnew).
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
LIB=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
b=p.BOARD(); b.SetCopperLayerCount(2)
mm=p.FromMM
def xy(x,y): return p.VECTOR2I(mm(x),mm(y))
tree=ET.parse(ROOT/'reports/completed.xml').getroot()
netmap={}; padnets={}
for n in tree.findall('nets/net'):
    net=p.NETINFO_ITEM(b,n.attrib['name'],int(n.attrib['code'])); b.Add(net); netmap[n.attrib['name']]=net
    for node in n.findall('node'): padnets[(node.attrib['ref'],node.attrib['pin'])]=net
pos={
 'J1':(104,110,0),'D1':(110,103,0),'C1':(114,105,90),'U1':(118,105,0),
 'C2':(121.5,102.5,0),'R1':(121.5,105.5,90),'R2':(121.5,108,90),'C3':(129,104.5,0),
 'U2':(117,116,0),'C4':(121.5,113.5,90),'U4':(130,116,0),'C6':(134.5,113.5,90),
 'U3':(138.5,124,0),'C5':(139,121.5,0),
 'R3':(130,124.5,0),'D2':(134,124.5,0),
 'R4':(116,123,90),'R5':(120,123,90),'R6':(124,123,90)}
fps={}
for c in tree.findall('components/comp'):
    ref=c.attrib['ref']; fpid=c.findtext('footprint'); lib,name=fpid.split(':')
    fp=p.FootprintLoad(str(LIB/(lib+'.pretty')),name)
    if fp is None: raise RuntimeError(fpid)
    fp.SetReference(ref); fp.SetValue(c.findtext('value')); fp.SetFPID(p.LIB_ID(lib,name))
    b.Add(fp); x,y,angle=pos[ref]; fp.SetPosition(xy(x,y)); fp.SetOrientationDegrees(angle)
    path=p.KIID_PATH(); path.push_back(p.KIID('e63406c1-b616-4867-9800-4b2a4032d152')); path.push_back(p.KIID(c.findtext('tstamps'))); fp.SetPath(path)
    for pad in fp.Pads():
        if (ref,pad.GetNumber()) in padnets: pad.SetNet(padnets[(ref,pad.GetNumber())])
    fp.Value().SetVisible(False)
    field=fp.Reference(); field.SetTextSize(xy(.8,.8)); field.SetTextThickness(mm(.12)); field.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T)); field.SetPosition(xy(x,y-3.4))
    for item in fp.GraphicalItems():
        if isinstance(item,p.PCB_TEXT): item.SetVisible(False)
    fps[ref]=fp
for ref,xx,yy in [('J1',104,106.5),('D1',110,105.5),('C1',114,107),('C2',122,100.9),('R1',122.5,106.4),('R2',124,108),('C3',129,109.1),('C4',122.5,112),('C6',135,112),('C5',139,120),('U3',139,126.5),('R3',130,126),('D2',134,126)]:
    fps[ref].Reference().SetPosition(xy(xx,yy))
for a,z in [((100,100),(142,100)),((142,100),(142,130)),((142,130),(100,130)),((100,130),(100,100))]:
    edge=p.PCB_SHAPE(); edge.SetShape(p.SHAPE_T_SEGMENT); edge.SetStart(xy(*a)); edge.SetEnd(xy(*z)); edge.SetLayer(p.Edge_Cuts); edge.SetWidth(mm(.05)); b.Add(edge)
def txt(t,x,y,size=.9):
    item=p.PCB_TEXT(b); item.SetText(t); item.SetPosition(xy(x,y)); item.SetTextSize(xy(size,size)); item.SetTextThickness(mm(.12)); item.SetLayer(p.F_SilkS); b.Add(item)
txt('I2C SENSOR / ETR',120.5,128.4,1)
txt('REV A',137.8,102,.8)
txt('5V IN',104,105,.8)
# Signal key, separated from header courtyard.
for i,(left,right) in enumerate([('G','5V'),('G','3V3'),('ALT','EVT'),('WP','ALM'),('SCL','SDA')]):
    txt(left,101.5,110+2.54*i,.8); txt(right,109,110+2.54*i,.8)
settings=b.GetDesignSettings(); settings.m_MinClearance=mm(.15); settings.m_TrackMinWidth=mm(.15); settings.m_ViasMinSize=mm(.6); settings.m_MinThroughDrill=mm(.3)
nc=settings.m_NetSettings.GetDefaultNetclass(); nc.SetClearance(mm(.15)); nc.SetTrackWidth(mm(.2)); nc.SetViaDiameter(mm(.6)); nc.SetViaDrill(mm(.3))
p.SaveBoard(str(ROOT/'I2C_Sensor_Board.kicad_pcb'),b)
# Synchronize project defaults with the routing rules, preserving other settings.
pro=json.loads((ROOT/'I2C_Sensor_Board.kicad_pro').read_text())
for n in pro['net_settings']['classes']:
    if n['name']=='Default': n.update(clearance=.15,track_width=.2,via_diameter=.6,via_drill=.3)
pro['board']['design_settings']['rules'].update(min_clearance=.15,min_track_width=.15,min_via_diameter=.6,min_through_hole_diameter=.3)
(ROOT/'I2C_Sensor_Board.kicad_pro').write_text(json.dumps(pro,indent=2)+'\n')
assert p.ExportSpecctraDSN(b,str(ROOT/'reports/placed.dsn'))
print('Board placed:',len(fps),'components; 42 x 30 mm; 2 layers.')
