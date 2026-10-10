# Informe del Reto 07

El informe incluye tabla de verdad, Karnaugh, circuito, módulos, simulación, mapa de pines, implementación y las fotografías del montaje. El video está enlazado desde el informe y desde `evidencias/README.md`.

Para regenerarlo, ejecutar primero las pruebas en Ubuntu desde VS Code o con `bash sim/run_tests.sh`; después ejecutar `python docs/generar_informe.py` con ReportLab y Pillow instalados. El generador utiliza el VCD de la simulación, los informes de Gowin, el análisis lógico y las tres fotos de `evidencias/fotos/`.

Los datos físicos de la tabla provienen de las lecturas comunicadas durante la prueba. Las fotografías muestran estados del montaje y no se usan para inferir combinaciones de entrada sin rotular.
