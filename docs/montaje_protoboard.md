# Montaje del Reto 07 con Sipeed LED×8

Materiales: Tang Primer 25K con Dock 60033, módulo Sipeed LED×8, protoboard, dos DIP de ocho interruptores, un pulsador, 15 jumpers macho–hembra y 14 jumpers macho–macho. Si el riel negativo está dividido, agregar un jumper para unir sus mitades.

Conectar el LED×8 directamente al PMOD **J6**, con la placa apagada. Alinear los 12 contactos y las marcas de alimentación del módulo y del Dock; identificar el pin 1 antes de insertarlo. El módulo ya contiene las resistencias de los LED y se alimenta desde la placa a 3,3 V.

Las entradas salen del conector **J3**, que tiene pines machos. La punta hembra de cada jumper macho–hembra entra en J3; la punta macho entra en la protoboard. Conectar **J3-12 (GND)** al riel negativo. **J3-11 es +5 V y no se usa.**

Cada interruptor conecta una entrada a GND al cerrarse. El pull-up interno mantiene el pin en alto cuando está abierto; el adaptador Verilog invierte ese nivel. Por tanto, **abierto = 0 lógico y cerrado = 1 lógico**. No se necesitan resistencias externas en las entradas ni alimentar el riel positivo.

![Montaje de los jumpers](montaje_protoboard.png)

## Interruptores y jumpers

Este ejemplo usa una protoboard con columnas A–E y F–J, separadas por la ranura central. A–E de una misma fila están unidos; F–J de esa fila forman otro grupo independiente.

Colocar el primer DIP atravesando la ranura central, con contactos opuestos en E10–E17 y F10–F17. Los jumpers macho–hembra llevan las señales de J3 a A10–A17. Desde J10–J17, conectar jumpers macho–macho al riel de GND.

Colocar el segundo DIP atravesando la ranura en las filas 25–32. Usar cinco posiciones: señales en A25–A29, y jumpers macho–macho desde J25–J29 a GND. Las otras tres posiciones quedan libres. Identificar cada interruptor por su fila; la numeración impresa del DIP depende de su orientación.

| Entrada | Pin macho del Dock | Bola FPGA | Señal en protoboard | Jumper macho–macho |
|---|---|---|---|---|
| a | J3-1 | K2 | A10 | J10 → GND |
| b | J3-2 | K1 | A11 | J11 → GND |
| c | J3-3 | L1 | A12 | J12 → GND |
| d | J3-4 | L2 | A13 | J13 → GND |
| A[3] | J3-5 | K4 | A14 | J14 → GND |
| A[2] | J3-6 | J4 | A15 | J15 → GND |
| A[1] | J3-7 | G1 | A16 | J16 → GND |
| A[0] | J3-8 | G2 | A17 | J17 → GND |
| B[3] | J3-9 | L3 | A25 | J25 → GND |
| B[2] | J3-10 | L4 | A26 | J26 → GND |
| B[1] | J3-23 | H4 | A27 | J27 → GND |
| B[0] | J3-24 | G4 | A28 | J28 → GND |
| en | J3-15 | F1 | A29 | J29 → GND |
| Reset | J3-16 | F2 | Grupo del primer contacto del pulsador | Segundo contacto → GND |
| GND | J3-12 | — | Riel negativo | Unir las mitades si están separadas |

Contar los pines desde el pin 1 marcado en J3: una columna contiene 1,3,5…39; la otra, 2,4,6…40. El diagrama muestra la numeración del esquema, no una vista por detrás. La bola FPGA J4 de A2 no es el conector J4 del Dock.

## Pulsador

Colocar el pulsador atravesando la ranura central, en una zona libre. La punta macho del jumper de J3-16 comparte el grupo de agujeros con un contacto del pulsador. El otro contacto se conecta a GND con un jumper macho–macho. En un pulsador de cuatro patas, escoger dos contactos que se unan solamente al presionar; verificar esta pareja con continuidad antes de alimentar.

Al presionar se borran Q y flag_q. Los indicadores u/v y en siguen mostrando sus entradas actuales.

## LED del módulo

El LED×8 es activo en bajo. El adaptador invierte sus salidas para que **LED encendido = 1 lógico**.

| LED | Señal | Pin de J6 | Bola FPGA |
|---|---|---|---|
| D1 | Q[0] | 11 | F5 |
| D2 | Q[1] | 12 | G5 |
| D3 | Q[2] | 9 | G7 |
| D4 | Q[3] | 10 | G8 |
| D5 | flag_q | 6 | J5 |
| D6 | u | 5 | H5 |
| D7 | v | 8 | H7 |
| D8 | en_led | 7 | H8 |

D1–D4 representan Q0–Q3, con pesos 1,2,4,8. Leer el resultado como **D4 D3 D2 D1**. D5 muestra préstamo, acarreo, paridad o empate según la operación. D6=u, D7=v y D8=en.

## Comprobación

Alimentar la placa por USB-C. Abrir en, ajustar el control y los datos, esperar 0,1 segundos y cerrar en. Abrir en de nuevo para conservar el resultado. Mientras en siga cerrado, el registro se actualiza con el reloj.

| Operación | a b c d | A | B | Q esperado | Indicador |
|---|---|---|---|---|---|
| RESTA | 0 0 0 0 | 0101 (5) | 0011 (3) | 0010 (2) | 0 |
| SUMA | 0 0 1 0 | 0101 (5) | 0011 (3) | 1000 (8) | 0 |
| XOR | 0 0 0 1 | 0101 (5) | 0011 (3) | 0110 (6) | 0 |
| MAYOR | 0 0 1 1 | 0101 (5) | 0011 (3) | 0101 (5) | 0 |
| SUMA con acarreo | 0 0 1 0 | 1111 (15) | 0001 (1) | 0000 (0) | 1 |
| RESTA con préstamo | 0 0 0 0 | 0000 (0) | 0001 (1) | 1111 (15) | 1 |
| MAYOR con empate | 0 0 1 1 | 0111 (7) | 0111 (7) | 0111 (7) | 1 |

Estos valores son resultados esperados para comprobar el montaje; no son mediciones de la placa.

Proyecto: `fpga/gowin/reto07_20230113/reto07_20230113.gprj`. Top: `tang_top_20230113`. Dispositivo: GW5A-LV25MG121NC1/I0, revisión A. Reloj: 50 MHz en E2, restricción de 20 ns. Bitstream: `fpga/bitstream/reto07_20230113.fs`.

Fuentes: [esquema oficial del Dock 60033](https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_Dock_60033_Schematic.pdf), [esquema del núcleo 52300](https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_52300_Schematic.pdf), [esquema Sipeed PMOD 8×LED](https://dl.sipeed.com/fileList/TANG/PMOD/PMOD_8XLED_Schematic.pdf) y [documentación Sipeed PMOD](https://wiki.sipeed.com/hardware/en/tang/tang-PMOD/FPGA_PMOD.html).
