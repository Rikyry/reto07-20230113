from pathlib import Path as FilePath
import json, re, csv, math
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Path, Polygon, Circle
from reportlab.graphics import renderSVG
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

R=FilePath(__file__).resolve().parent.parent; D=R/'docs'
data=json.loads((D/'logic_analysis.json').read_text()); pins=json.loads((D/'pins.json').read_text())
navy=colors.HexColor('#15364b'); teal=colors.HexColor('#007e87'); light=colors.HexColor('#eef5f8')
palette=[colors.HexColor(x) for x in ['#007e87','#ad5c12','#7552aa']]
def text(d,x,y,s,size=10,color=navy): d.add(String(x,y,s,fontName='Helvetica',fontSize=size,fillColor=color))
def line(d,x1,y1,x2,y2,color=navy,w=1): d.add(Line(x1,y1,x2,y2,strokeColor=color,strokeWidth=w))
def box(d,x,y,w,h,label):
 d.add(Rect(x,y,w,h,rx=5,ry=5,strokeColor=navy,fillColor=light)); text(d,x+8,y+h/2,label,9)
def arrow(d,x1,y1,x2,y2):
 line(d,x1,y1,x2,y2)
 ang=math.atan2(y2-y1,x2-x1); l=5
 d.add(Polygon([x2,y2,x2-l*math.cos(ang-.5),y2-l*math.sin(ang-.5),x2-l*math.cos(ang+.5),y2-l*math.sin(ang+.5)],fillColor=navy,strokeColor=navy))

def kmap(fn):
 d=Drawing(480,290); gray=[0,1,3,2]; x=100;y=58; cw=70;ch=43
 text(d,8,260,f'Mapa de Karnaugh: {fn}',15); text(d,40,226,'ab / cd',10)
 for c,g in enumerate(gray): text(d,x+c*cw+27,y+4*ch+9,f'{g:02b}',11)
 for r,g in enumerate(gray):
  text(d,65,y+(3-r)*ch+16,f'{g:02b}',11)
  for c,h in enumerate(gray):
   n=4*g+h; xx=x+c*cw; yy=y+(3-r)*ch
   d.add(Rect(xx,yy,cw,ch,strokeColor=colors.HexColor('#bccad1'),fillColor=colors.white))
   text(d,xx+5,yy+ch-10,str(n),7,colors.grey)
   text(d,xx+33,yy+14,str(int(n in data['minterms_'+fn])),14)
 for i,group in enumerate(data[fn]['chosen']):
  cells={(gray.index(n//4),gray.index(n%4)) for n in group['minterms']}
  # Outline cells in the same group; separated top/bottom outlines mark wraparound.
  for rr,cc in cells:
   xx=x+cc*cw+3+i*2; yy=y+(3-rr)*ch+3+i*2
   ww=cw-6-i*4;hh=ch-6-i*4
   if (rr-1,cc) not in cells: line(d,xx,yy+hh,xx+ww,yy+hh,palette[i],2)
   if (rr+1,cc) not in cells: line(d,xx,yy,xx+ww,yy,palette[i],2)
   if (rr,cc-1) not in cells: line(d,xx,yy,xx,yy+hh,palette[i],2)
   if (rr,cc+1) not in cells: line(d,xx+ww,yy,xx+ww,yy+hh,palette[i],2)
  term=''.join(('!' if v=='0' else '')+s for s,v in zip('abcd',group['cube']) if v!='-')
  text(d,20+i*155,27,f'G{i+1}: {term}',11,palette[i])
 return d

def gates():
 d=Drawing(480,280)
 for offset,fn in [(0,'u'),(245,'v')]:
  text(d,offset+5,255,f'Circuito de {fn}',13)
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
  text(d,xx+14,yy-3,'OR',9);arrow(d,xx+51,yy,offset+236,yy);text(d,offset+231,yy+8,fn,11)
 return d

def blocks():
 d=Drawing(480,240)
 box(d,70,155,145,48,'control_logic');text(d,5,179,'a,b,c,d',10);arrow(d,45,180,70,180)
 box(d,260,155,150,48,'datapath');arrow(d,215,180,260,180);text(d,228,188,'u,v',9)
 text(d,278,225,'A[3:0], B[3:0]',10);arrow(d,335,218,335,203)
 box(d,260,55,150,48,'result_register');arrow(d,335,155,335,103);text(d,341,122,'Y, flag_comb',9)
 text(d,85,77,'clk, rst, en',10);arrow(d,150,80,260,80)
 arrow(d,410,80,478,80);text(d,415,91,'Q, flag_q',9)
 text(d,12,20,'top_20230113 instancia los tres bloques por nombre.',10)
 return d

stats=json.loads((R/'fpga/reports/summary.json').read_text())
rpt=(R/'fpga/reports/reto07_20230113.rpt.txt').read_text()
banks={}
for port,label,conn,pos,ball in pins:
 m=re.search(r'^'+re.escape(port)+r'\s+\|[^|]+\|\s*'+ball+r'/(\d+)',rpt,re.M)
 if not m: raise ValueError('Missing assigned pin '+port)
 banks[port]=m.group(1)
ff=stats['registers']; fmax=stats['fmax_mhz']
pinrows=[['Señal','Puerto','Conector','Posición','Bola','Banco','Polaridad','I/O'], ['clk','clk','Core','Oscilador','E2','5','Reloj','LVCMOS33']]
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
 d=Drawing(480,215);names=['clk','rst','en','u','v','Q','flag_q'];x0=52;w=416
 for i,name in enumerate(names):
  yy=186-i*24;text(d,0,yy+1,name,9);line(d,x0,yy-3,x0+w,yy-3,colors.HexColor('#e1e6ea'))
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
 for tt in range(math.ceil(start/20)*20,int(end)+1,20):text(d,x0+(tt-start)*w/(end-start)-8,9,str(tt),7)
 text(d,165,0,'Tiempo (ns) - datos reales del VCD',8)
 return d
renderSVG.drawToFile(wave(),str(D/'ondas_temporales.svg'))

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyR',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=navy))
styles.add(ParagraphStyle(name='CodeR',fontName='Courier',fontSize=10,leading=15,spaceAfter=7,textColor=navy))
styles.add(ParagraphStyle(name='TitleR',fontName='Helvetica-Bold',fontSize=24,leading=28,spaceAfter=18,textColor=navy))
styles['Heading1'].textColor=navy;styles['Heading2'].textColor=teal
story=[]
def p(s):story.append(Paragraph(s,styles['BodyR']))
def h(s):story.append(Paragraph(s,styles['Heading1']))
def tab(rows,widths=None,small=False):
 rows=[[Paragraph(str(v),ParagraphStyle(name='cell',fontName='Helvetica',fontSize=8 if small else 9,leading=11)) for v in row] for row in rows]
 t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),light),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#b5c5ce')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),3 if small else 5),('BOTTOMPADDING',(0,0),(-1,-1),3 if small else 5)]));story.append(t);story.append(Spacer(1,10))
def page():story.append(PageBreak())

story.append(Paragraph('Reto 07<br/>Unidad de revisión de datos',styles['TitleR']))
p('<b>Riky Ramos · Matrícula 20230113</b><br/>Sistemas Digitales · Verilog 2001 · Tang Primer 25K<br/>Actualización: 9 de octubre de 2026')
h('Especificación y estado')
p('Dos operandos sin signo de 4 bits A y B se transforman según el selector {v,u}. El control procede de las cuatro variables a,b,c,d. Q y flag_q almacenan la salida cuando en=1; rst es asíncrono y activo en 1. Las salidas combinacionales continúan respondiendo durante reset.')
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
tab([['Función','Grupo','Minterms agrupados','Celdas que lo hacen esencial'],['u','ab','12,13,14,15','12'],['u','ad','9,11,13,15','9'],['u','!bc','2,3,10,11','2 y 3'],['v','!ad','1,3,5,7','1'],['v','b!c','4,5,12,13','4 y 12'],['v','cd','3,7,11,15','11']],[45,65,150,230])
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
p('Mapa verificado con el esquema Sipeed del Dock 60033, hoja 1, y el informe de pines de Gowin. Todos los puertos físicos tienen ubicación explícita y estándar LVCMOS33. El reloj es E2, banco 5, oscilador Y1100 de 50 MHz del core 52300; periodo SDC=20 ns.')
tab(pinrows,[48,60,52,42,37,35,72,62],True)
p('Los interruptores se conectan a las entradas hembra J4/J5 con jumpers macho-macho; al cerrarlos unen la entrada a GND. El pull-up interno y la inversión del adaptador producen abierto=0 lógico y cerrado=1 lógico. El pulsador une E10 a GND mientras se presiona. Los rieles de tierra de la protoboard comparten GND con la FPGA.')
p('El Sipeed LED×8 se conecta directamente a J6 y contiene las resistencias de sus LED. En J4/J5/J6, 1/2 son 3,3 V y 3/4 son GND. GPIO a 3,3 V, estándar LVCMOS33. Q0 está en J5, Q1 en H5, Q2 en H8 y Q3 en H7; flag en G7, u en G8, v en F5 y enable en G5.')
p('El montaje utiliza 22 GPIO externos: 13 interruptores, un reset y ocho salidas LED; el reloj procede del oscilador de la placa. El mapa de pines corresponde al bitstream cargado.');page()

h('Implementación y pruebas en placa')
tab([['Métrica','Resultado comprobado'],['Herramienta','Gowin V1.9.11.03 Education'],['Dispositivo','GW5A-LV25MG121NC1/I0, revisión A'],['LUT / ALU',f"{stats['lut']} LUT / {stats['alu']} ALU"],['Registros / latches',f"{ff} registros / 0 latches"],['Reloj / Fmax',f"50 MHz requerido / {fmax} MHz estimado por STA"],['Setup / hold','0 endpoints violados; TNS=0'],['Bitstream','fpga/bitstream/reto07_20230113.fs']],[180,310])
p('Las excepciones SDC excluyen solamente interruptores externos hacia sw_meta y reset externo hacia rst_pipe. Los caminos entre etapas y hacia el registro permanecen temporizados. Las salidas LED usan un presupuesto de 10 ns; no tienen reloj externo de captura. Se habilitan CPU/SSPI como GPIO para E2. JTAG conserva programación.')
p('Gowin Programmer detectó GW5A-25A y completó SRAM Program con User Code 0x0000A3AE y Status Code 0x76026238. La captura está en evidencias/programacion_sram.jpg. La carga SRAM es volátil; el archivo cargado está conservado en fpga/bitstream/.')
p('Las siguientes lecturas fueron comunicadas o confirmadas durante la verificación del montaje. El orden es v, en, flag, u, Q3, Q2, Q1, Q0. Las fotos documentan el montaje y los estados de los LED; no se les asigna una operación a partir de la posición de interruptores sin rotular.')
tab([['Prueba','A','B','Q / flag','Lectura','Confirmación'],
 ['RESTA','3','1','2 / 0','01000010','Lectura reportada'],
 ['SUMA','0','0','0 / 0','01010000','Lectura reportada'],
 ['SUMA','15','0','15 / 0','01011111','Lectura reportada'],
 ['SUMA con acarreo','15','1','0 / 1','01110000','Lectura reportada'],
 ['SUMA con acarreo','15','13','12 / 1','01111100','Confirmación verbal'],
 ['XOR paridad impar','15','13','2 / 1','11100010','Confirmación verbal']], [107,26,26,55,77,117], True)
p('Para repetir: ajustar control y operandos con en=0, esperar 0,1 s y activar en. La retención conserva Q y flag_q al deshabilitar; reset borra ambos y tiene prioridad. Las verificaciones automáticas incluyen MAYOR, empate, préstamo, retención y reset con en=0 y en=1.')
p('El video original de explicación está en evidencias/EXPLICACION.mp4. <link href="https://raw.githubusercontent.com/Rikyry/reto07-20230113/main/evidencias/EXPLICACION.mp4" color="#007e87">Ver o descargar la explicación</link>. Las fotos originales están en evidencias/fotos/.')
p('<b>Recursos y herramientas:</b> enunciado Reto_07_20230113.pdf (6 páginas); esquemas oficiales Sipeed core 52300 y Dock 60033; ejemplos oficiales TangPrimer-25K-example; manuales Gowin incluidos; Icarus Verilog para simulación; Python y ReportLab para análisis e informe; Codex como asistencia de preparación. El estudiante debe revisar, explicar y poder modificar el diseño.')
p('Documentación de placa: <link href="https://wiki.sipeed.com/hardware/en/tang/tang-primer-25k/primer-25k.html" color="#007e87">Sipeed Tang Primer 25K</link>. Esquema: <link href="https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_Dock_60033_Schematic.pdf" color="#007e87">Dock 60033</link>. Reloj: <link href="https://github.com/sipeed/TangPrimer-25K-example/blob/main/pmod_led/src/pmod_led.sdc" color="#007e87">ejemplo SDC oficial</link>. Consulta: 3 de octubre de 2026.')

photos=[
 ('funcionamiento_01.jpg','Fotografía 1 Montaje general','Protoboard con interruptores de control y datos, habilitación y pulsador de reset; Tang Primer 25K alimentada por USB y módulo Sipeed LED×8 conectado. Los LED de salida aparecen apagados en esta toma.'),
 ('funcionamiento_02.jpg','Fotografía 2 Salidas activas','El mismo montaje muestra algunos LED de salida encendidos. Los interruptores suministran las entradas y el módulo LED×8 presenta el resultado y los indicadores del sistema.'),
 ('funcionamiento_03.jpg','Fotografía 3 Panel encendido','Vista del montaje con los ocho LED de salida encendidos. La fotografía conserva el cableado de la protoboard, el pulsador y la conexión del módulo LED×8.')
]
for name,title,caption in photos:
 page(); h(title); p(caption)
 path=R/'evidencias/fotos'/name
 iw,ih=ImageReader(str(path)).getSize()
 scale=min(440/iw,580/ih)
 story.append(Image(str(path),width=iw*scale,height=ih*scale))
 story.append(Spacer(1,9))
 p('Evidencia original: evidencias/fotos/'+name)


def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#cbd7dd'));c.line(45,39,550,39);c.setFont('Helvetica',8);c.setFillColor(navy)
 c.drawString(45,26,'Riky Ramos | 20230113 | Reto 07');c.drawRightString(550,26,f'Página {doc.page}')
SimpleDocTemplate(str(D/'informe_20230113_reto07.pdf'),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=40,bottomMargin=52,title='Reto 07 - Riky Ramos - 20230113',author='Riky Ramos').build(story,onFirstPage=footer,onLaterPages=footer)
print('Created',D/'informe_20230113_reto07.pdf')
