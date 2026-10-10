Las pruebas se ejecutan en Ubuntu desde VS Code con WSL. Las herramientas necesarias son Make, Python 3, Verilator, Icarus Verilog y GTKWave. Para instalarlas: `sudo apt install make python3 verilator iverilog gtkwave`.

Desde la raiz del repositorio:

```bash
make lint
make sim
make check
```

`make lint` ejecuta Verilator con `-Wall` sobre el top de simulacion y el adaptador de placa. Las advertencias hacen fallar la tarea. `make sim` compila y ejecuta ambos testbenches. El primero recorre 4096 vectores y 12 casos temporales; el segundo verifica la sincronizacion, el reset, el enable y las salidas fisicas del adaptador.

`make check` ejecuta ambas comprobaciones y escribe `resultados.json`, con resultados, versiones de las herramientas, fecha y hashes de los archivos comprobados. Si un testbench falla, el comando devuelve error. Los logs y los resumenes individuales quedan en `sim/`.

Para examinar una señal al investigar un fallo, ejecutar `make wave` despues de generar el VCD. Se abre GTKWave con las entradas, los controles, el resultado y los indicadores. Para cambiar el VCD: `make wave WAVE_FILE=sim/tang_top_20230113.vcd`.

En VS Code: `Ctrl+Shift+P`, `Tasks: Run Task`, y seleccionar `Verilog: lint`, `Verilog: sim`, `Verilog: wave` o `Verilog: check`. La ruta de fuentes predeterminada es `src`; las tareas tambien permiten introducir otra ruta mediante `SRC_DIR`.

GitHub Actions ejecuta el mismo `make check` con cada push. Guarda `resultados.json`, logs y VCD en el artefacto `resultados-reto07`. Los VCD y ejecutables temporales se regeneran y no se guardan como archivos Git.

Las conexiones `unused_Y` y `unused_flag_comb` del adaptador corresponden a las salidas combinacionales que no se muestran en el modulo LED. Las salidas visibles siguen siendo el resultado registrado y su indicador. Se identifican siguiendo la convencion de [Verilator para señales sin usar](https://verilator.org/guide/latest/warnings.html#unusedsignal), sin desactivar advertencias globales.

`lint_inicial.log` conserva las dos advertencias de la primera revision. Los logs `lint_top_20230113.log` y `lint_tang_top_20230113.log` corresponden al codigo actual comprobado.
