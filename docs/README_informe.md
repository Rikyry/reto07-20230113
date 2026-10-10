# Informe del Reto 07

El informe incluye tabla de verdad, Karnaugh, circuito, módulos, simulación, mapa de pines, implementación y las fotografías del montaje. El video está enlazado desde el informe y desde `evidencias/README.md`.

Para regenerarlo, ejecutar primero las pruebas en Ubuntu desde VS Code o con `bash sim/run_tests.sh`; después ejecutar `python docs/generar_informe.py` con ReportLab y Pillow instalados. El generador utiliza el VCD de la simulación, los informes de Gowin, el análisis lógico y las tres fotos de `evidencias/fotos/`.

Los datos físicos de la tabla provienen de las lecturas comunicadas durante la prueba. Las fotografías muestran estados del montaje y no se usan para inferir combinaciones de entrada sin rotular.

El informe usa Times New Roman de 12 puntos, interlineado doble en el texto, sangría de 1,27 cm y márgenes de 2,54 cm en papel carta. No incluye subtítulos ni pies de página; las tablas y los diagramas son en blanco y negro. La numeración aparece arriba a la derecha.

Para regenerar la misma fuente, Times New Roman debe estar instalada. En Windows se usan los archivos `times.ttf`, `timesbd.ttf`, `timesi.ttf` y `timesbi.ttf` de la carpeta de fuentes; en otro sistema se puede definir `TIMES_NEW_ROMAN_DIR` con la ubicación de esos archivos. Las fuentes no se distribuyen en el repositorio.
