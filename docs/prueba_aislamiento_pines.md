# Prueba de aislamiento de pines: LED y DIP (7 - 14)

**Convención de la resta actualizada:** Q=|A−B| en cuatro bits y flag de préstamo=1 si A<B. La magnitud no es el resultado en complemento a dos.

El resultado observado **01100101** no basta para determinar si el fallo es del código o del montaje: es necesario confirmar el orden de lectura (LED encendido = 1 frente a nivel eléctrico = 0) y el caso ensayado. El módulo `tang_top_20230113` contiene `assign led = ~{sw_sync[12], v, u, flag_q, Q};`. No se cambió esta asignación arbitrariamente.

## Precauciones y montaje fijo
- Usa el proyecto original `fpga/gowin/reto07_20230113/reto07_20230113.gprj` (no el de diagnóstico), recompila y programa el .fs nuevo.
- Mantén **ENABLE (E11 / J5-9) cerrado hacia GND** para habilitar el registro: `en` lógico = 1. Deja **RESET (E10 / J5-10) abierto**, salvo pulsar brevemente al iniciar.
- El interruptor **cerrado hacia GND equivale a 1 lógico**. Los demás deben estar abiertos y los dos DIP deben compartir GND.
- Cada prueba parte de `abcd=0000` y `B=0000`, excepto donde se indique. Si puedes, lee los LED **L1 a L8** en el orden `Q0,Q1,Q2,Q3,flag,u,v,enable`. Las referencias L1–L8 son del diseño y deben corroborarse en el LED×8 físico.

## Pruebas para identificar A y LED: RESTA A - 0

**Poner únicamente E11 y el pin indicado a GND**; dejar todos los demás abiertos. Cada prueba debe encender el LED de habilitación más un LED de resultado.

| Cerrar pines a GND | Señal | Operación | Q | L1–L8 (1=encendido) | led[7:0] eléctrico |
|---|---|---|---|---|---|
| E11 | A=0 | 0−0 | 0000 | 00000001 | 01111111 |
| E11 + G10 | A0=1 | 1−0 | 0001 | 10000001 | 01111110 |
| E11 + G11 | A1=1 | 2−0 | 0010 | 01000001 | 01111101 |
| E11 + D10 | A2=1 | 4−0 | 0100 | 00100001 | 01111011 |
| E11 + D11 | A3=1 | 8−0 | 1000 | 00010001 | 01110111 |

**Si en estos cuatro casos se enciende otro LED de resultado, hay un cruce de cables de A o un orden visual de LED distinto al supuesto.** Si todos salen bien, A y los LED Q están correctamente identificados; sigue con B.

## Pruebas para identificar B: RESTA 0 - B

**Poner únicamente E11 y el pin indicado a GND**; mantener A=0 y abcd=0.

| Cerrar a GND | B | Q esperado | Préstamo | L1–L8 (1=encendido) |
|---|---|---|---|---|
| E11 + L11 | 1 | 0001 | 1 | 10001001 |
| E11 + K11 | 2 | 0010 | 1 | 01001001 |
| E11 + K5 | 4 | 0100 | 1 | 00101001 |
| E11 + L5 | 8 | 1000 | 1 | 00011001 |

## Prueba de selector (A=B=0)
- Cerrar E11 solamente: RESTA, L1–L8 = `00000001`.
- Cerrar E11 + B11 (**c=1**, `abcd=0010`): SUMA, L1–L8 = `00000101`.
- Cerrar E11 + B10 (**d=1**, `abcd=0001`): XOR, L1–L8 = `00000011`.
- Cerrar E11 + B11 + B10 (`abcd=0011`): MAYOR con empate, L1–L8 = `00001111`.

## La prueba original: 7 - 14
Enlaza a GND **D10, G11, G10** para A=0111; **L5, K5, K11** para B=1110; y **E11** para enable=1. Los pines C11, C10, B11, B10, D11 y L11 van abiertos. Tras liberar E10 (RESET), esperar el reloj.

| Elemento | Valor correcto |
|---|---|
| control abcd | `0000` |
| A | `0111` = 7 |
| B | `1110` = 14 |
| Q / préstamo | `0111` / `1` |
| `led[7:0]`, niveles eléctricos | `01101000` |
| L1–L8, LED encendidos | `11101001` |

**Interpretación alternativa para tu lectura 01100101:** si ese valor procede de un analizador lógico y corresponde a los *niveles eléctricos led[7:0]*, representa Q=`1010` (10), `flag=1`, `u=v=0`, `en=1`. Con la resta en magnitud eso podría representar una diferencia de 10; no equivale a A=7 y B=14. Si `01100101` representa visualmente las luces L1–L8 (1=encendido), esta interpretación **no aplica** y hay que usar las pruebas de aislamiento anteriores.

Si no coinciden las pruebas de A/B, abre el proyecto alterno `reto07_diagnostico.gprj` para ver directamente el nivel lógico sincronizado de las entradas, sin depender de la ALU. No cambies el orden del código hasta detectar concretamente qué pin difiere.
