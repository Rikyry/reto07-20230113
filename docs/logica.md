# Tabla, Karnaugh y SOP minima

u = ab + ad + !bc
v = !ad + cd + b!c

Cada funcion: 9 terminos / 36 literales en forma canonica; 3 terminos / 6 literales en forma minima.

Filas ab y columnas cd en Gray 00,01,11,10. No hay don't-care.

## u
- G1: cubo 11--, minterms [12, 13, 14, 15], esenciales por [12].
- G2: cubo 1--1, minterms [9, 11, 13, 15], esenciales por [9].
- G3: cubo -01-, minterms [2, 3, 10, 11], esenciales por [2, 3].

## v
- G1: cubo 0--1, minterms [1, 3, 5, 7], esenciales por [1].
- G2: cubo -10-, minterms [4, 5, 12, 13], esenciales por [12, 4].
- G3: cubo --11, minterms [3, 7, 11, 15], esenciales por [11].

Los tres implicantes esenciales de cada funcion obligan a tres productos. Cada producto contiene dos literales; las soluciones alcanzan el minimo de 3 terminos y 6 literales. El archivo logic_analysis.json conserva todos los implicantes primos y la cobertura minima calculada por enumeracion.

En u, el grupo !bc une las filas 00 y 10 por los bordes superior/inferior del mapa. Los productos ac (u) y bd (v) son primos redundantes y no se usan.

Controles de ejemplo: 0000 -> RESTA; 0010 -> SUMA; 0001 -> XOR; 0011 -> MAYOR.
