# Prueba inicial en placa

Usar el bitstream `fpga/bitstream/reto07_20230113.fs`, no el diagnóstico temporal. Las entradas tienen pull-up e inversión: abierto = 0 lógico, conectado a GND = 1 lógico. Mantener E10 abierto salvo al presionar reset.

Conectar GND de la FPGA al riel negativo de la protoboard. Abrir los trece interruptores. Presionar y soltar reset; Q y flag quedan en cero.

| Paso | Entradas conectadas a GND | abcd | A | B | en | Q | flag | u | v | Salidas encendidas esperadas |
|---|---|---|---|---|---|---|---|---|---|---|
| Cero | E11 | 0000 | 0000 | 0000 | 1 | 0000 | 0 | 0 | 0 | G5, enable |
| Uno | E11 y G10 | 0000 | 0001 | 0000 | 1 | 0001 | 0 | 0 | 0 | G5, enable; H7, Q0 |
| Retención | Solo G10, después del paso Uno | 0000 | 0001 | 0000 | 0 | 0001 | 0 | 0 | 0 | H7, Q0 |

En el paso Uno, las otras entradas C11, C10, B11, B10, D11, D10, G11, L5, K5, K11 y L11 permanecen abiertas. E10 también permanece abierto.

El paso Uno hace RESTA, 1 − 0 = 1. En el orden lógico Q3 Q2 Q1 Q0 flag u v en, la lectura es 00010001. El orden visual de los LED debe identificarse en el módulo físico: el LED enable es el que quedaba fijo en el diagnóstico cuando E11 estaba unido a GND. Al agregar G10 debe encenderse un segundo LED. Esta comprobación no depende de contar los LED desde un extremo concreto.

El testbench del adaptador comprueba estos pasos y el borrado por reset con enable desactivado. Los resultados físicos están pendientes de registrar; no deben sustituirse por las expectativas de la tabla.
