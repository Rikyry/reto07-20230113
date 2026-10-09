# Programación en SRAM

Fecha: 9 de octubre de 2026, 18:37 (UTC−4).

Gowin Programmer V1.9.11.03 Education detectó GW5A-25A, IDCODE 0x0001281B. Se seleccionó SRAM Mode / SRAM Program y el archivo `fpga/bitstream/reto07_20230113.fs`.

La operación mostró User Code 0x0000D628, Status Code 0x76026238 y Finished. Duración indicada: 4,66 segundos. No aparecieron mensajes de error durante esta carga. Se restauró el bitstream del reto después del diagnóstico temporal.

SHA-256 del archivo cargado: `5f68dc37761e2d0243834d76df4ef8140f02687dbda97fd3f6213dea6d2c931f`.

La captura está en `programacion_sram.jpg`. Se programó la versión con las entradas en los conectores hembra J4/J5, reset en E10 y salidas L1–L8 ordenadas como Q3 Q2 Q1 Q0 flag u v en. La comprobación física de interruptores, reset y LED debe anotarse por separado en `registro_placa.csv`.

La programación SRAM se pierde al quitar la alimentación. Para repetir la prueba, seleccionar el mismo archivo y ejecutar SRAM Program otra vez.
