# Programación en SRAM

Fecha: 9 de octubre de 2026, 17:32 (UTC−4).

Gowin Programmer V1.9.11.03 Education detectó GW5A-25A, IDCODE 0x0001281B. Se seleccionó SRAM Mode / SRAM Program y el archivo `fpga/bitstream/reto07_20230113.fs`.

La operación mostró User Code 0x000020AF, Status Code 0x76026238 y Finished. Duración indicada: 4,69 segundos. No aparecieron mensajes de error durante esta carga.

SHA-256 del archivo cargado: `2916c75423539ba8a592240ff22110c686fc72dd18cd753a63470ee84a33ff53`.

La captura está en `programacion_sram.jpg`. Se programó la versión con las entradas en los conectores hembra J4/J5 y el reset en E10. La comprobación física de interruptores, reset y LED debe anotarse por separado en `registro_placa.csv`.

La programación SRAM se pierde al quitar la alimentación. Para repetir la prueba, seleccionar el mismo archivo y ejecutar SRAM Program otra vez.
