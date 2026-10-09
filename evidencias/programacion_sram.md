# Programación en SRAM

Fecha: 9 de octubre de 2026, 18:45 (UTC−4).

Gowin Programmer V1.9.11.03 Education detectó GW5A-25A, IDCODE 0x0001281B. Se seleccionó SRAM Mode / SRAM Program y el archivo `fpga/bitstream/reto07_20230113.fs`.

La operación mostró User Code 0x0000A3AE, Status Code 0x76026238 y Finished. Duración indicada: 4,68 segundos. No aparecieron mensajes de error durante esta carga. Se cargó el bitstream del reto con Q0, de peso 1, asignado a J5.

SHA-256 del archivo cargado: `8510aee9dc03e2a6ab9057460af5e066b3fb5641c8dbc2476553929729faa955`.

La captura está en `programacion_sram.jpg`. Se programó la versión con las entradas en los conectores hembra J4/J5, reset en E10 y salidas L1–L8 ordenadas como Q0 Q1 Q2 Q3 flag u v en. La comprobación física de interruptores, reset y LED debe anotarse por separado en `registro_placa.csv`.

La programación SRAM se pierde al quitar la alimentación. Para repetir la prueba, seleccionar el mismo archivo y ejecutar SRAM Program otra vez.
