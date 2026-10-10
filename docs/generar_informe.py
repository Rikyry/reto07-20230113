from pathlib import Path as FilePath
import json, re, csv, math, os
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Path, Polygon, Circle
from reportlab.graphics import renderSVG
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_dirs=[FilePath(os.environ.get('TIMES_NEW_ROMAN_DIR','C:/Windows/Fonts')), FilePath('/usr/share/fonts/truetype/msttcorefonts'), FilePath.home()/'.local/share/fonts']
font_dir=next((d for d in font_dirs if all((d/f).exists() for f in ['times.ttf','timesbd.ttf','timesi.ttf','timesbi.ttf'])),None)
if font_dir is None:
 raise FileNotFoundError('Instalar Times New Roman o definir TIMES_NEW_ROMAN_DIR con sus cuatro archivos TTF.')
for name,file in [('TNR','times.ttf'),('TNR-Bold','timesbd.ttf'),('TNR-Italic','timesi.ttf'),('TNR-BoldItalic','timesbi.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(font_dir/file)))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNR-Bold',italic='TNR-Italic',boldItalic='TNR-BoldItalic')

R=FilePath(__file__).resolve().parent.parent; D=R/'docs'
data=json.loads((D/'logic_analysis.json').read_text()); pins=json.loads((D/'pins.json').read_text())
navy=colors.black; teal=colors.black; light=colors.white
palette=[colors.black]*3
def text(d,x,y,s,size=12,color=navy): d.add(String(x,y,s,fontName='TNR',fontSize=12,fillColor=colors.black))
def line(d,x1,y1,x2,y2,color=navy,w=1,dash=None): d.add(Line(x1,y1,x2,y2,strokeColor=colors.black,strokeWidth=w,strokeDashArray=dash))
def box(d,x,y,w,h,label):
 d.add(Rect(x,y,w,h,rx=5,ry=5,strokeColor=navy,fillColor=light)); text(d,x+8,y+h/2,label,9)
def arrow(d,x1,y1,x2,y2):
 line(d,x1,y1,x2,y2)
 ang=math.atan2(y2-y1,x2-x1); l=5
 d.add(Polygon([x2,y2,x2-l*math.cos(ang-.5),y2-l*math.sin(ang-.5),x2-l*math.cos(ang+.5),y2-l*math.sin(ang+.5)],fillColor=navy,strokeColor=navy))

def kmap(fn):
 d=Drawing(468,290); gray=[0,1,3,2]; x=100;y=58; cw=70;ch=43
 text(d,8,260,fn); text(d,40,226,'ab / cd',10)
 for c,g in enumerate(gray): text(d,x+c*cw+27,y+4*ch+9,f'{g:02b}',11)
 for r,g in enumerate(gray):
  text(d,65,y+(3-r)*ch+16,f'{g:02b}',11)
  for c,h in enumerate(gray):
   n=4*g+h; xx=x+c*cw; yy=y+(3-r)*ch
   d.add(Rect(xx,yy,cw,ch,strokeColor=colors.black,fillColor=colors.white))
   text(d,xx+5,yy+ch-10,str(n),7,colors.grey)
   text(d,xx+33,yy+14,str(int(n in data['minterms_'+fn])),14)
 for i,group in enumerate(data[fn]['chosen']):
  cells={(gray.index(n//4),gray.index(n%4)) for n in group['minterms']}
  # Outline cells in the same group; separated top/bottom outlines mark wraparound.
  for rr,cc in cells:
   xx=x+cc*cw+3+i*2; yy=y+(3-rr)*ch+3+i*2
   ww=cw-6-i*4;hh=ch-6-i*4
   if (rr-1,cc) not in cells: line(d,xx,yy+hh,xx+ww,yy+hh,palette[i],1.2,[None,[5,3],[1,3]][i])
   if (rr+1,cc) not in cells: line(d,xx,yy,xx+ww,yy,palette[i],1.2,[None,[5,3],[1,3]][i])
   if (rr,cc-1) not in cells: line(d,xx,yy,xx,yy+hh,palette[i],1.2,[None,[5,3],[1,3]][i])
   if (rr,cc+1) not in cells: line(d,xx+ww,yy,xx+ww,yy+hh,palette[i],1.2,[None,[5,3],[1,3]][i])
  term=''.join(('!' if v=='0' else '')+s for s,v in zip('abcd',group['cube']) if v!='-')
  text(d,20+i*155,27,f'G{i+1}: {term}',11,palette[i])
 return d

def gates():
 d=Drawing(468,280)
 for offset,fn in [(0,'u'),(232,'v')]:
  text(d,offset+5,255,fn)
  for i,group in enumerate(data[fn]['chosen']):
   yy=205-i*82; xx=offset+78
   terms=[(s,v) for s,v in zip('abcd',group['cube']) if v!='-']
   for j,(s,val) in enumerate(terms):
    yin=yy+12-j*24; text(d,offset+4,yin-3,s,11)
    if val=='0':
     line(d,offset+15,yin,offset+27,yin)
     d.add(Polygon([offset+27,yin-6,offset+27,yin+6,offset+39,yin],strokeColor=navy,fillColor=colors.white))
     d.add(Circle(offset+42,yin,3,strokeColor=navy,fillColor=colors.white)); line(d,offset+45,yin,xx,yin)
    else: line(d,offset+15,yin,xx,yin)
   # AND symbol: flat input face and semicircular output face.
   p=Path(strokeColor=navy,fillColor=light);p.moveTo(xx,yy-22);p.lineTo(xx+18,yy-22)
   p.curveTo(xx+48,yy-22,xx+48,yy+22,xx+18,yy+22);p.lineTo(xx,yy+22);p.closePath()
   d.add(p); text(d,xx+3,yy-3,'AND',8)
   xo=offset+165; dest=135+(1-i)*12
   line(d,xx+41,yy,xo-12,yy);line(d,xo-12,yy,xo-12,dest);line(d,xo-12,dest,xo,dest)
  # OR symbol.
  xx=offset+163;yy=135
  p=Path(strokeColor=navy,fillColor=light);p.moveTo(xx,yy-28)
  p.curveTo(xx+27,yy-28,xx+40,yy-15,xx+51,yy)
  p.curveTo(xx+40,yy+15,xx+27,yy+28,xx,yy+28)
  p.curveTo(xx+12,yy+9,xx+12,yy-9,xx,yy-28);p.closePath();d.add(p)
  text(d,xx+14,yy-3,'OR',9);arrow(d,xx+51,yy,offset+228,yy);text(d,offset+222,yy+8,fn,11)
 return d

def blocks():
 d=Drawing(468,240)
 box(d,65,155,130,48,'control_logic');text(d,0,179,'a,b,c,d');arrow(d,43,180,65,180)
 box(d,250,155,150,48,'datapath');arrow(d,195,180,250,180);text(d,210,188,'u,v')
 text(d,268,225,'A[3:0], B[3:0]');arrow(d,325,218,325,203)
 box(d,250,55,150,48,'result_register');arrow(d,325,155,325,103);text(d,335,122,'Y, flag_comb')
 text(d,88,77,'clk, rst, en');arrow(d,152,80,250,80)
 arrow(d,400,80,464,80);text(d,410,110,'Q, flag_q')
 return d

stats=json.loads((R/'fpga/reports/summary.json').read_text())
rpt=(R/'fpga/reports/reto07_20230113.rpt.txt').read_text()
banks={}
for port,label,conn,pos,ball in pins:
 m=re.search(r'^'+re.escape(port)+r'\s+\|[^|]+\|\s*'+ball+r'/(\d+)',rpt,re.M)
 if not m: raise ValueError('Missing assigned pin '+port)
 banks[port]=m.group(1)
ff=stats['registers']; fmax=stats['fmax_mhz']
pinrows=[['Señal','Puerto','PMOD','Pos.','Pin','Banco','Polaridad','I/O'], ['clk','clk','Core','Osc.','E2','5','Reloj','LVCMOS33']]
for port,label,conn,pos,ball in pins:
 pinrows.append([label,port,conn,str(pos),ball,banks[port],'activa 0','LVCMOS33'])

def wave():
 # Figure sourced from the VCD, rather than invented expected traces.
 lines=(R/'sim/top_20230113.vcd').read_text().splitlines(); scopes=[]; ids={}; histories={};t=0
 for l in lines:
  if l.startswith('$scope'):scopes.append(l.split()[2])
  elif l.startswith('$upscope'):scopes.pop()
  elif l.startswith('$var') and scopes==['tb_top_20230113']:
   a=l.split();name=a[4];ids[a[3]]=name;histories[name]=[]
  elif l.startswith('#'):t=int(l[1:])
  elif l and l[0] in '01xz':
   if l[1:] in ids:histories[ids[l[1:]]].append((t/1000,l[0]))
  elif l.startswith('b'):
   a=l[1:].split()
   if len(a)==2 and a[1] in ids:histories[ids[a[1]]].append((t/1000,a[0]))
 tmax=max(tt for h in histories.values() for tt,v in h);start=tmax-180;end=tmax
 d=Drawing(468,245);names=['clk','rst','en','u','v','Q','flag_q'];x0=52;w=416
 for i,name in enumerate(names):
  yy=216-i*24;text(d,0,yy+1,name,9);line(d,x0,yy-3,x0+w,yy-3,colors.black)
  h=histories[name];prev=[v for tt,v in h if tt<=start];val=prev[-1] if prev else 'x'
  entries=[(start,val)]+[(tt,v) for tt,v in h if start<tt<end]+[(end,None)]
  for j in range(len(entries)-1):
   ta,va=entries[j];tb,_=entries[j+1];xx=x0+(ta-start)*w/(end-start);xb=x0+(tb-start)*w/(end-start)
   if name=='Q':
    line(d,xx,yy+8,xb,yy+8,teal,1.2);line(d,xx,yy-2,xb,yy-2,teal,1.2)
    if xb-xx>10:
     try:txt=str(int(va,2))
     except ValueError:txt=va
     text(d,xx+2,yy+1,txt,8,teal)
    line(d,xx,yy-2,xx,yy+8,teal)
   else:
    yh=yy+(8 if va=='1' else -2);line(d,xx,yh,xb,yh,teal,1.3)
    if j>0:
     old=entries[j-1][1];line(d,xx,yy+(8 if old=='1' else -2),xx,yh,teal,1.2)
 for tt in range(math.ceil(start/20)*20,int(end)+1,20):text(d,x0+(tt-start)*w/(end-start)-8,25,str(tt),7)
 text(d,165,1,'Tiempo (ns) - datos reales del VCD',8)
 return d
renderSVG.drawToFile(wave(),str(D/'ondas_temporales.svg'))
(D/'ondas_temporales.svg').write_bytes(((D/'ondas_temporales.svg').read_text().rstrip()+'\n').encode('utf-8'))

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyR',fontName='TNR',fontSize=12,leading=24,firstLineIndent=36,spaceAfter=0,spaceBefore=0,textColor=colors.black,splitLongWords=True,allowWidows=0,allowOrphans=0))
styles.add(ParagraphStyle(name='CoverR',fontName='TNR',fontSize=12,leading=24,alignment=TA_CENTER,textColor=colors.black))
styles.add(ParagraphStyle(name='ReferenceR',fontName='TNR',fontSize=12,leading=24,leftIndent=36,firstLineIndent=-36,spaceAfter=0,textColor=colors.black,splitLongWords=True))
story=[]

def p(s):
 s=re.sub(r'<b>([^<]+):</b>',r'\1:',s)
 story.append(Paragraph(s,styles['BodyR']))

def h(s):
 pass

def tab(rows,widths=None,small=False):
 width=468
 widths=[v*width/sum(widths) for v in widths] if widths else None
 cells=[]
 for ri,row in enumerate(rows):
  cells.append([Paragraph(str(v),ParagraphStyle(name='cell',fontName='TNR-Bold' if ri==0 else 'TNR',fontSize=12,leading=15,alignment=TA_CENTER if ri==0 or ci>0 else 0,splitLongWords=True)) for ci,v in enumerate(row)])
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('LINEABOVE',(0,0),(-1,0),0.7,colors.black),('LINEBELOW',(0,0),(-1,0),0.7,colors.black),('LINEBELOW',(0,-1),(-1,-1),0.7,colors.black),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
 if len(rows)>=10:
  t.setStyle(TableStyle([('NOSPLIT',(0,-3),(-1,-1))]))
 story.append(Spacer(1,6))
 story.append(t if len(rows)>=10 else KeepTogether([t]))
 story.append(Spacer(1,6))

def page():
 pass

story.append(Spacer(1,120))
story.append(Paragraph('<b>Unidad de revisión de datos en la Tang Primer 25K</b>',styles['CoverR']))
story.append(Spacer(1,24))
for item in ['Riky Ramos','Matrícula 20230113','ITLA','Sistemas Digitales','Reto 07','9 de octubre de 2026']:
 story.append(Paragraph(item,styles['CoverR']))
story.append(PageBreak())

h('Especificación y estado')
p('El proyecto consiste en una unidad de revisión de datos que recibe dos operandos sin signo de 4 bits, A y B, y los transforma según el selector {v,u}. El control procede de las cuatro variables a,b,c,d. Q y flag_q almacenan la salida cuando en=1; rst es asíncrono y activo en 1. Las salidas combinacionales continúan respondiendo durante reset. El funcionamiento corresponde a la variante del Reto 07 (ITLA, s. f.).')
tab([['Selector {v,u}','Operación','Resultado Y','Indicador'],['00','RESTA','(A-B) módulo 16','Préstamo: A &lt; B'],['01','SUMA','(A+B) módulo 16','Acarreo: A+B &gt; 15'],['10','XOR','A XOR B','Paridad impar de Y'],['11','MAYOR','máximo(A,B)','Empate: A=B']],[80,75,165,170])
p('La simulación comprobó 4096 vectores y 12 casos temporales sin errores. Gowin completó síntesis, ubicación, ruteo, análisis temporal y generación del bitstream. La carga SRAM terminó correctamente. Las pruebas en placa confirmaron resultados de RESTA, SUMA y XOR; las fotografías y el video de explicación acompañan este informe.')
story.append(blocks());page()

h('Tabla de verdad completa')
p('Índice decimal m=8a+4b+2c+d. Todos los minterms no listados valen cero; no existen condiciones indiferentes.')
rows=[['m','a b c d','u','v','{v,u}','Operación']]
for t in data['truth']:rows.append([t['m'],' '.join(t['bits']),t['u'],t['v'],f"{t['v']}{t['u']}",t['operation']])
tab(rows,[35,105,40,40,80,190])
p('u vale 1 en los minterms (2,3,9,10,11,12,13,14,15)<br/>v vale 1 en los minterms (1,3,4,5,7,11,12,13,15)')
p('Ejemplos para la explicación individual: abcd=0000 activa RESTA; 0010 activa SUMA; 0001 activa XOR; 0011 activa MAYOR. El orden del selector es v primero, u después.');page()

h('Karnaugh y minimalidad')
for fn in ['u','v']:
 story.append(kmap(fn))
 terms='ab + ad + !bc' if fn=='u' else '!ad + b!c + cd'
 p(f'<b>{fn} = {terms}</b>. Tres grupos de cuatro celdas, dos literales por grupo.')
page()
h('Justificación y circuito de control')
tab([['Función','Grupo','Minterms agrupados','Celdas que lo hacen esencial'],['u','ab','12,13,14,15','12'],['u','ad','9,11,13,15','9'],['u','!bc','2,3,10,11','2 y 3'],['v','!ad','1,3,5,7','1'],['v','b!c','4,5,12,13','4 y 12'],['v','cd','3,7,11,15','11']],[60,55,145,208])
p('En u, !bc cruza los bordes superior e inferior: las filas ab=00 y 10 son adyacentes en el mapa. Los implicantes primos ac de u y bd de v son redundantes. Cada función tiene tres implicantes esenciales: ninguna cobertura con menos de tres productos puede cubrir las celdas esenciales. Los seis literales alcanzan el segundo criterio de mínima SOP.')
tab([['Forma','Términos por función','Literales por función'],['Canónica','9','36'],['Simplificada','3','6']],[170,150,170])
p('Este conteo expresa productos y variables booleanas; no es el número de LUT de la FPGA. NOT se aplica a las entradas indicadas; tres AND alimentan un OR por función.')
story.append(gates());page()

h('Módulos, anchos y temporización')
tab([['Módulo','Responsabilidad'],['control_logic','assign de las dos SOP mínimas'],['datapath','Operadores, extensión a 5 bits en suma y selección ?:'],['result_register','5 bits almacenados: Q[3:0] y flag_q; reset asíncrono y enable'],['top_20230113','Tres instancias conectadas por nombre; usado en simulación'],['tang_top_20230113','13 interruptores con dos etapas; reset adaptado; ocho LED']],[160,330])
p('A,B,Y,Q tienen 4 bits sin signo. La suma usa {1\'b0,A}+{1\'b0,B} y conserva el quinto bit para acarreo. La resta de 4 bits se trunca módulo 16; el préstamo se calcula mediante A&lt;B. El XOR usa reducción ^ para paridad. Los controles y los indicadores tienen un bit.')
p('<b>Préstamo y acarreo:</b> 0-1 necesita préstamo y devuelve 15 módulo 16; 15+1 produce 0 y acarreo. El préstamo describe un minuendo insuficiente, mientras el acarreo describe una suma que excede cuatro bits. No son la misma condición.')
p('El registro usa always @(posedge clk or posedge rst), asignaciones &lt;=, prioridad de reset y retención al deshabilitar. Liberar reset no captura. No hay relojes derivados, retardos RTL ni latches.')
p('El adaptador afirma reset asíncronamente al pulsar rst_n=0 y lo libera tras dos flancos de 50 MHz. Los interruptores son señales de nivel. Ajustar datos con en=0, esperar 0,1 s y habilitar garantiza estabilidad; los dos registros por bit no hacen una captura atómica de un bus que esté cambiando.')
p('El Sipeed LED×8 tiene salidas físicas activas en bajo; el adaptador invierte la polaridad para que un LED encendido represente 1 lógico. Q y flag_q muestran el valor almacenado; u/v indican la operación actual y el octavo LED muestra enable. En el orden de lectura identificado durante las pruebas: v | en | flag_q | u | Q3 Q2 Q1 Q0.')
p('Enable controla la actualización del registro; el registro es la memoria. Con en=1, soltar reset permite capturar de nuevo la operación actual. Con en=0, presionar y soltar reset deja Q y flag_q en cero. Los indicadores de control no se borran con reset.');page()

h('Verificación automática y ondas')
p('El modelo de referencia usa las listas originales de minterms y las definiciones aritméticas. No reutiliza las SOP del RTL. Se ejecutan 16 controles ×16 valores A ×16 valores B =4096 vectores; 16384 comparaciones combinacionales y 24 temporales, total 16408, con cero errores. !== detecta X o Z.')
labels=['Afirmar reset entre flancos','Reset con en=1 durante flanco','Liberar reset sin flanco','Capturar RESTA con préstamo','Capturar SUMA con acarreo','Capturar XOR con paridad impar','Capturar MAYOR con empate 15=15','Cambiar entradas con en=0 y retener','Rehabilitar y capturar','Cambiar datos entre flancos con en=1','Reset asíncrono de un Q no nulo','Capturar después del reset, B=0']
tab([['Caso','Comprobación','Estado']]+[[i+1,s,'PASS'] for i,s in enumerate(labels)],[40,395,55],True)
story.append(wave())
p('Figura extraída de sim/top_20230113.vcd: ventanas finales de captura, retención y reset. Los logs y VCD acompañan las pruebas; las ondas complementan las comparaciones automáticas. El test del adaptador verifica sincronización, polaridad y liberación del reset.');page()

h('Mapa de pines y montaje')
p('El mapa de pines se verificó con el esquema del Dock 60033 y el informe de Gowin (Sipeed, s. f.-b). Todos los puertos físicos tienen ubicación explícita y estándar LVCMOS33. El reloj es E2, banco 5, oscilador Y1100 de 50 MHz del core 52300; periodo SDC=20 ns (Sipeed, s. f.-a).')
tab(pinrows,[48,60,52,42,37,40,72,82],True)
p('Los interruptores se conectan a las entradas hembra J4/J5 con jumpers macho-macho; al cerrarlos unen la entrada a GND. El pull-up interno y la inversión del adaptador producen abierto=0 lógico y cerrado=1 lógico. El pulsador une E10 a GND mientras se presiona. Los rieles de tierra de la protoboard comparten GND con la FPGA.')
p('El Sipeed LED×8 se conecta directamente a J6 y contiene las resistencias de sus LED (Sipeed, s. f.-c). En J4/J5/J6, 1/2 son 3,3 V y 3/4 son GND. GPIO a 3,3 V, estándar LVCMOS33. Q0 está en J5, Q1 en H5, Q2 en H8 y Q3 en H7; flag en G7, u en G8, v en F5 y enable en G5.')
p('El montaje utiliza 22 GPIO externos: 13 interruptores, un reset y ocho salidas LED; el reloj procede del oscilador de la placa. El mapa de pines corresponde al bitstream cargado.');page()

h('Implementación y pruebas en placa')
tab([['Métrica','Resultado comprobado'],['Herramienta','Gowin V1.9.11.03 Education'],['Dispositivo','GW5A-LV25MG121NC1/I0, revisión A'],['LUT / ALU',f"{stats['lut']} LUT / {stats['alu']} ALU"],['Registros / latches',f"{ff} registros / 0 latches"],['Reloj / Fmax',f"50 MHz requerido / {fmax} MHz estimado por STA"],['Setup / hold','0 endpoints violados; TNS=0'],['Bitstream','fpga/bitstream/reto07_20230113.fs']],[180,310])
p('Las excepciones SDC excluyen solamente interruptores externos hacia sw_meta y reset externo hacia rst_pipe. Los caminos entre etapas y hacia el registro permanecen temporizados. Las salidas LED usan un presupuesto de 10 ns; no tienen reloj externo de captura. Se habilitan CPU/SSPI como GPIO para E2. JTAG conserva programación.')
p('Gowin Programmer detectó GW5A-25A y completó SRAM Program con User Code 0x0000A3AE y Status Code 0x76026238. La captura está en evidencias/programacion_sram.jpg. La carga SRAM es volátil; el archivo cargado está conservado en fpga/bitstream/.')
p('En las pruebas del montaje se compararon las lecturas de los LED con los resultados esperados. El orden de lectura es v, en, flag, u, Q3, Q2, Q1, Q0. Las fotografías muestran el circuito armado y diferentes estados de las salidas.')
tab([['Prueba','A','B','Q / flag','Lectura','Confirmación'],
 ['RESTA','3','1','2 / 0','01000010','Lectura reportada'],
 ['SUMA','0','0','0 / 0','01010000','Lectura reportada'],
 ['SUMA','15','0','15 / 0','01011111','Lectura reportada'],
 ['SUMA con acarreo','15','1','0 / 1','01110000','Lectura reportada'],
 ['SUMA con acarreo','15','13','12 / 1','01111100','Confirmación verbal'],
 ['XOR paridad impar','15','13','2 / 1','11100010','Confirmación verbal']], [107,26,26,55,77,117], True)
p('Para repetir: ajustar control y operandos con en=0, esperar 0,1 s y activar en. La retención conserva Q y flag_q al deshabilitar; reset borra ambos y tiene prioridad. Las verificaciones automáticas incluyen MAYOR, empate, préstamo, retención y reset con en=0 y en=1.')
p('El video original de explicación está en evidencias/EXPLICACION.mp4. <link href="https://raw.githubusercontent.com/Rikyry/reto07-20230113/main/evidencias/EXPLICACION.mp4" color="black">Ver o descargar la explicación</link>. Las fotos originales están en evidencias/fotos/.')
p('Para la simulación se utilizó Icarus Verilog en Ubuntu desde VS Code; la implementación y la programación se realizaron con Gowin. El informe se generó con Python y ReportLab. Para la preparación del proyecto y la documentación se contó con asistencia de Codex.')

photos=[
 ('funcionamiento_01.jpg','Fotografía 1 Montaje general','Protoboard con interruptores de control y datos, habilitación y pulsador de reset; Tang Primer 25K alimentada por USB y módulo Sipeed LED×8 conectado. Los LED de salida aparecen apagados en esta toma.'),
 ('funcionamiento_02.jpg','Fotografía 2 Salidas activas','El mismo montaje muestra algunos LED de salida encendidos. Los interruptores suministran las entradas y el módulo LED×8 presenta el resultado y los indicadores del sistema.'),
 ('funcionamiento_03.jpg','Fotografía 3 Panel encendido','Vista del montaje con los ocho LED de salida encendidos. La fotografía conserva el cableado de la protoboard, el pulsador y la conexión del módulo LED×8.')
]
for name,title,caption in photos:
 story.append(PageBreak()); p(caption)
 path=R/'evidencias/fotos'/name
 iw,ih=ImageReader(str(path)).getSize()
 scale=min(375/iw,500/ih)
 story.append(Image(str(path),width=iw*scale,height=ih*scale))



story.append(PageBreak())
p('Las fuentes consultadas para la especificación y el montaje del proyecto fueron las siguientes.')
refs=[
 'ITLA. (s. f.). <i>Reto 07 Unidad de revisión de datos</i> [Material de la asignatura Sistemas Digitales].',
 'Sipeed. (s. f.-a). <i>Tang Primer 25K 52300 schematic</i> [Esquema]. https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_52300_Schematic.pdf',
 'Sipeed. (s. f.-b). <i>Tang Primer 25K Dock 60033 schematic</i> [Esquema]. https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_Dock_60033_Schematic.pdf',
 'Sipeed. (s. f.-c). <i>PMOD 8XLED schematic</i> [Esquema]. https://dl.sipeed.com/fileList/TANG/PMOD/PMOD_8XLED_Schematic.pdf'
]
for ref in refs:
 story.append(Paragraph(ref,styles['ReferenceR']))

def header(c,doc):
 c.setFillColor(colors.black);c.setFont('TNR',12)
 c.drawRightString(540,756,str(doc.page))

SimpleDocTemplate(str(D/'informe_20230113_reto07.pdf'),pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=72,title='Unidad de revisión de datos en la Tang Primer 25K',author='Riky Ramos').build(story,onFirstPage=header,onLaterPages=header)
print('Created',D/'informe_20230113_reto07.pdf')
