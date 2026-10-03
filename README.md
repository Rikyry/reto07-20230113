# Reto 07 - Unidad de revision de datos

- Nombre: Riky Ramos
- Matricula: 20230113
- Reto: 07, Sistemas Digitales
- Descripcion: Sistema Verilog que selecciona RESTA, SUMA, XOR o MAYOR sobre dos datos de cuatro bits y registra el resultado con habilitacion y reset.
- Placa prevista: Tang Primer 25K, GW5A-LV25MG121NC1/I0.
- Acceso previsto: [repositorio publico](https://github.com/Rikyry/reto07-20230113), accesible al docente sin invitacion.

## Primer avance

Se incorporan `src/control_logic.v` y `src/datapath.v`.
El control usa `u = ab + ad + !bc` y `v = !ad + cd + b!c`.
El selector es `{v,u}`: 00 RESTA, 01 SUMA, 10 XOR y 11 MAYOR.
Los indicadores son prestamo, acarreo, paridad impar y empate.

## Pendiente de incorporar

- Registro del resultado y top del sistema.
- Testbench y evidencia ejecutada en Ubuntu desde VS Code con WSL.
- Proyecto Gowin, restricciones e informes.
- Programacion y demostracion en la placa.

Esta rama de avances se prepara a partir del trabajo local disponible y solo
publicara los archivos de cada etapa. No representa revisiones anteriores
ni contiene fechas inventadas. Las pruebas previas en Windows no acreditan
la validacion solicitada en Ubuntu y VS Code.

Los siguientes avances se registraran con commits descriptivos y push antes
de cada revision. El README y los archivos de Git acompanian el codigo para
identificar al estudiante y conservar una estructura reproducible.
