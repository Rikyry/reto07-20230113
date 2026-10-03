# Reto 07 - Unidad de revision de datos

- Nombre: Riky Ramos
- Matricula: 20230113
- Reto: 07, Sistemas Digitales
- Descripcion: Unidad Verilog que selecciona RESTA, SUMA, XOR o MAYOR sobre dos datos de cuatro bits y genera el indicador de cada operacion.
- Placa: Tang Primer 25K, GW5A-LV25MG121NC1/I0.
- Repositorio: [repositorio publico](https://github.com/Rikyry/reto07-20230113), accesible al docente sin invitacion.

## Control y operaciones

Se incorporan `src/control_logic.v` y `src/datapath.v`.
El control usa `u = ab + ad + !bc` y `v = !ad + cd + b!c`.
El selector es `{v,u}`: 00 RESTA, 01 SUMA, 10 XOR y 11 MAYOR.
Los indicadores son prestamo, acarreo, paridad impar y empate.

## Registro

`result_register.v` guarda `Q[3:0]` y `flag_q` en el flanco ascendente
cuando `en=1`. El reset es asincrono y activo en 1. Con `en=0`, el registro
conserva su valor.

