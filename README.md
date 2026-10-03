# Reto 07 - Unidad de revision de datos

- Nombre: Riky Ramos
- Matricula: 20230113
- Reto: 07, Sistemas Digitales
- Descripcion: Unidad Verilog que selecciona RESTA, SUMA, XOR o MAYOR sobre dos datos de cuatro bits y registra el resultado y su indicador.
- Placa: Tang Primer 25K, GW5A-LV25MG121NC1/I0.
- Repositorio: [repositorio publico](https://github.com/Rikyry/reto07-20230113), accesible al docente sin invitacion.

## Control y operaciones

Se incorporan `src/control_logic.v` y `src/datapath.v`.
El control usa `u = ab + ad + !bc` y `v = !ad + cd + b!c`.
El selector es `{v,u}`: 00 RESTA, 01 SUMA, 10 XOR y 11 MAYOR.
Los indicadores son prestamo, acarreo, paridad impar y empate.

## Registro

`result_register.v` guarda `Q[3:0]` y `flag_q` en el flanco ascendente
cuando `en=1`. El reset es asincrono y activo en 1. Con `en=0`, el registro
conserva su valor.

## Conexion del sistema

`top_20230113.v` conecta el control, las operaciones y el registro.
`Y` y `flag_comb` son combinacionales; `Q` y `flag_q` son las salidas
almacenadas. El sistema usa un solo reloj.

## Simulacion en Ubuntu

Abrir la carpeta en VS Code con la extension WSL y seleccionar Ubuntu.
Se necesitan Icarus Verilog (`iverilog` y `vvp`). Ejecutar la tarea
**Simular Reto 07 en Ubuntu**, o desde la terminal Ubuntu:

```bash
bash sim/run_tests.sh
```

El testbench compara las 4096 combinaciones de control y operandos, y
comprueba 12 casos de registro, habilitacion y reset. Los registros de
ejecucion estan en `sim/`; las ondas VCD se generan al ejecutar la prueba.

## Tang Primer 25K

El top de la placa es `tang_top_20230113`. Las entradas tienen dos etapas
de sincronizacion. El reloj de la placa es de 50 MHz en E2.

`sw[12:0]={en,a,b,c,d,A[3:0],B[3:0]}`.
`led[6:0]={v,u,flag_q,Q[3:0]}`.

El mapa de conexiones esta en `docs/mapa_pines.csv`. Los interruptores
conectan su entrada a 3,3 V, el reset conecta `rst_n` a GND, y cada LED
lleva una resistencia de 1 kOhm. Usar `en=0` al ajustar las entradas y
esperar 0,1 s antes de habilitar.

El proyecto Gowin esta en `fpga/gowin/reto07_20230113/reto07_20230113.gprj`.
Selecciona GW5A-LV25MG121NC1/I0, revision A, Verilog 2001 y reloj de 20 ns.
Para reconstruir con Gowin V1.9.11.03 Education:

```powershell
& 'C:/Gowin/Gowin_V1.9.11.03_Education_x64/IDE/bin/gw_sh.exe' fpga/build.tcl
```

El bitstream esta en `fpga/bitstream/reto07_20230113.fs` y los informes
de implementacion en `fpga/reports/`.

## Resultados

La simulacion en Ubuntu comprueba 4096 vectores, 12 casos temporales y
16408 comparaciones, con cero errores. La prueba del adaptador verifica
la sincronizacion de entradas, el reset y el orden de los LED.

Las dos pruebas se ejecutaron con la tarea de VS Code en WSL Ubuntu.
La [captura de la simulacion](evidencias/simulacion_ubuntu_vscode.jpg)
muestra los resultados y la finalizacion de la tarea. La version de
Ubuntu y del simulador esta registrada en `sim/entorno_ubuntu.txt`.

La implementacion usa 24 LUT, 19 ALU y 33 registros, sin latches.
Cumple el reloj de 50 MHz, con Fmax estimada de 120,509 MHz y sin
violaciones de setup o hold.

## Documentacion

`docs/` contiene la tabla de verdad, los mapas de Karnaugh, el circuito
de control y el mapa de pines. Los archivos temporales y las ondas VCD
se regeneran; el proyecto, las restricciones y los registros de pruebas
se conservan en el repositorio.

