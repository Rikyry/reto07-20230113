# Retos

- Nombre: Riky Ramos
- Matrícula: 20230113
- Número de reto: 07
- Materia: Sistemas Digitales

## Descripción del proyecto

Diseñar una unidad de revisión de datos en Verilog para la Tang Primer 25K. El sistema debe seleccionar RESTA, SUMA, XOR o MAYOR entre dos datos de cuatro bits, generar el indicador correspondiente y guardar el resultado con habilitación y reset asíncrono.

**Formato de RESTA:** salida `Q=|A-B|` (magnitud de 4 bits) y bandera de préstamo `flag_q=1` cuando `A<B`. Ejemplo: `7−14=−7` se indica con `Q=0111` y `flag_q=1`; no se representa en complemento a dos.

## Trabajo requerido

1. Elaborar la tabla de verdad, los mapas de Karnaugh y las expresiones simplificadas de las funciones de control `u` y `v`.
2. Implementar y conectar `control_logic`, `datapath`, `result_register` y `top_20230113`, usando Verilog sintetizable y un solo reloj.
3. Crear el testbench y comprobar las operaciones, los indicadores, la habilitación y el reset en Ubuntu desde VS Code.
4. Configurar el proyecto Gowin, las restricciones de pines y reloj, y generar los informes de síntesis, implementación y temporización, junto con el bitstream.
5. Programar la Tang Primer 25K y presentar fotografías y un video de la demostración.
6. Registrar los avances con commits claros y subirlos a GitHub antes de cada revisión. Organizar la entrega en `src/`, `sim/`, `docs/`, `fpga/` y `evidencias/`.

## Diagnóstico en placa

Si el LED×8 no coincide con la prueba 7−14, utiliza primero la [prueba individual de pines y LED](docs/prueba_aislamiento_pines.md). Separa errores de cableado, orden visual y selección de control antes de modificar las operaciones Verilog. También está el [proyecto temporal de diagnóstico](fpga/gowin/reto07_20230113/reto07_diagnostico.gprj).
