# Montaje del Reto 07

Materiales: Tang Primer 25K con Dock 60033, protoboard, 13 interruptores (por ejemplo, dos DIP de 8 posiciones), un pulsador, siete LED, siete resistencias de 1 kΩ y cables Dupont.

Los interruptores forman cuatro entradas de control `a,b,c,d`, cuatro bits de `A`, cuatro bits de `B` y una entrada `en`. Cada interruptor conecta su entrada a 3,3 V al cerrarse. Las resistencias pull-down internas mantienen las entradas en 0 al abrirse; no hacen falta resistencias externas en esas entradas.

El pulsador de reset conecta `rst_n` a GND al presionarlo. La resistencia pull-up interna mantiene el reset inactivo al soltarlo. En un pulsador de cuatro patas, usar dos contactos que se unan solamente al presionar.

Cada salida conecta en este orden: pin de la FPGA, resistencia de 1 kΩ, ánodo del LED, cátodo a GND. El ánodo suele ser la pata larga; el lado plano del encapsulado identifica el cátodo. Los siete LED muestran `v`, `u`, `flag_q` y `Q[3:0]`.

Alimentar la placa por su USB-C. Llevar el 3,3 V y GND de la placa a los rieles de la protoboard. En J4, J5 y J6, los pines 1 y 2 son 3,3 V; 3 y 4 son GND. No conectar 5 V a los pines de entrada. Identificar el pin 1 en la placa antes de contar; el dibujo es un mapa de numeración del esquema, no una vista del cableado por detrás.

![Mapa de conexión](montaje_protoboard.png)

| Entrada | Conector y pin | Pin de FPGA |
|---|---|---|
| a | J4-5 | C11 |
| b | J4-6 | C10 |
| c | J4-7 | B11 |
| d | J4-8 | B10 |
| A3 | J4-9 | D11 |
| A2 | J4-10 | D10 |
| A1 | J4-11 | G11 |
| A0 | J4-12 | G10 |
| B3 | J5-5 | L5 |
| B2 | J5-6 | K5 |
| B1 | J5-7 | K11 |
| B0 | J5-8 | L11 |
| en | J5-9 | E11 |
| Reset | J5-10 | E10 |

| LED | Conector y pin | Pin de FPGA |
|---|---|---|
| v | J6-5 | H5 |
| u | J6-6 | J5 |
| Indicador | J6-7 | H8 |
| Q3 (peso 8) | J6-8 | H7 |
| Q2 (peso 4) | J6-9 | G7 |
| Q1 (peso 2) | J6-10 | G8 |
| Q0 (peso 1) | J6-11 | F5 |

Los nombres J4/J5/J6 en la columna de conector identifican los conectores del Dock. El nombre J5 en la columna de pin de FPGA es la bola de la señal `u`, conectada físicamente a J6-6.

Para cargar un resultado, abrir `en`, ajustar el control y los datos, esperar 0,1 segundos y cerrar `en`. Abrir `en` de nuevo para conservar el resultado mientras se cambian las entradas. Mientras `en` siga cerrado, el registro se actualiza con el reloj. El reset borra `Q` y `flag_q`; los LED `u` y `v` siguen mostrando la operación seleccionada.

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

Proyecto: `fpga/gowin/reto07_20230113/reto07_20230113.gprj`. Top de implementación: `tang_top_20230113`. Reloj interno de la placa: 50 MHz en E2. Bitstream: `fpga/bitstream/reto07_20230113.fs`.

Pines verificados con el [esquema oficial del Dock 60033](https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_Dock_60033_Schematic.pdf). Reloj verificado con el [esquema oficial del núcleo 52300](https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_52300_Schematic.pdf).
