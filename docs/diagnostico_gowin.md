# Diagnóstico de conexiones del Reto 07 en GOWIN

## Qué se comprobó
El circuito calcula por lógica `abcd=0000`, `A=0111` (7), `B=1110` (14), `enable=1`: RESTA, `Q=1001`, `flag_q=1`, `u=v=0`. Sus salidas activas en bajo son `led[7:0]=01100110` (pines eléctricos), equivalentes a bits encendidos `10011001` cuando se leen por índices **led[7] hasta led[0]**. En orden de luces L1–L8 (`Q0 Q1 Q2 Q3 flag u v en`) se enciende `10011001` para este patrón (coincide por simetría).

**No son interruptores de 0/1 de tensión directa:** cada pin tiene pull-up y un interruptor cerrado a GND pasa a **1 lógico** por `sw_sync <= ~sw_meta` (pipeline equivalente al código). Un pin abierto es 0 lógico. **Enable lógico 1 = E11 conectado a GND**.

## Prueba con diagnóstico temporal

1. Abre `fpga/gowin/reto07_20230113/reto07_diagnostico.gprj`. Conserva el .gprj original para entregar.
2. Verifica top `tang_diag_20230113` y ejecuta Synthesize, Place & Route, Generate Bitstream. Programa la SRAM con el .fs recién generado; **no uses** el .fs del proyecto original para este diagnóstico.
3. Para introducir la palabra `abcd=0000 A=0111 B=1110 en=1`, cierra hacia GND solo **D10, G11, G10, L5, K5, K11, E11**. Deja abiertos C11, C10, B11, B10, D11 y L11. No presiones reset para ver A/B.
4. Con reset E10 **abierto**, el diagnóstico presenta `led[7:0]` encendidos `01111110` (A y B), tensiones eléctricas `10000001`. Con E10 a GND presenta bits encendidos `10000000` (enable y abcd), tensiones `01111111`.
5. Si estos dos patrones no aparecen, revisa numeración de LED por pin y las conexiones de GND, pull-up, pines de J4/J5 y el módulo de ocho LED. El fallo es de interfaz/cableado o lectura, no está demostrado que sea del sumador/restador.
6. Regresa a `reto07_20230113.gprj`, ejecuta todas las etapas de compilación y programa el .fs correspondiente. Con la combinación lógica indicada, la salida eléctrica será `01100110`. El módulo físico enciende en nivel bajo.

Las 12 entradas de control/datos según el CST: abcd=C11,C10,B11,B10; A=D11,D10,G11,G10; B=L5,K5,K11,L11; enable=E11; reset=E10.

## Aviso NL0002
`control_logic` optimizado durante síntesis no prueba un error de lógica. Sus funciones siguen teniendo uso en el top como `u,v`; confirmar cambios de operación antes de alterarlas.

## X rojas del proyecto GOWIN
El archivo .gprj original hacía referencia a dos testbenches `sim/tb_*.v` (deshabilitados). Se quitaron del proyecto de GOWIN y del `fpga/build.tcl` para evitar rutas rotas: siguen en la carpeta `sim/` y se ejecutan con `make check` (Icarus/Verilator). Mantén **la estructura completa** del repositorio al abrir el .gprj, pues las rutas son relativas.

**Estado de verificación:** hay nueva regresión de `7-14` en `sim/tb_tang_top_20230113.v`. La simulación en el PC y la programación física solo quedan comprobadas después de ejecutar las herramientas; no se atribuyen resultados físicos a esta guía.
