# Implementación con LED×8

El adaptador sincroniza las 13 entradas de J3, invierte su polaridad y muestra Q, flag_q, u, v y en en el Sipeed LED×8 conectado a J6. El reset se activa de forma asíncrona y se libera después de dos flancos del reloj.

Las simulaciones se ejecutaron en Ubuntu desde la tarea de pruebas de VS Code. El testbench del sistema recorrió 4096 combinaciones de control y datos, más 12 pruebas temporales: 16408 comparaciones y cero errores. El testbench del adaptador verificó la inversión de entradas, los ocho LED, la sincronización, la conservación del resultado y el reset. Los registros de compilación quedaron sin avisos.

Gowin completó síntesis, Place & Route, análisis temporal y generación del bitstream. El reloj es de 50 MHz; el informe indica Fmax de 248,062 MHz, cero violaciones de setup y hold y cero latches. Recursos: 43 LUT, 19 ALU y 33 registros.

La síntesis informa NL0002 al integrar la instancia control_logic en la lógica optimizada. Es un aviso de optimización de jerarquía: las funciones u/v siguen verificadas por simulación. No se encontraron otros avisos ni errores en la implementación.

Los resultados están en `sim/`, los informes y el resumen con SHA-256 del bitstream en `fpga/reports/`, y la captura de Ubuntu en `evidencias/simulacion_ubuntu_vscode.jpg`. La prueba física se registra por separado cuando se programe la placa y se compruebe el montaje.
