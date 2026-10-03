module datapath(
    input wire [3:0] A, B,
    input wire u, v,
    output wire [3:0] Y,
    output wire flag_comb
);
    wire [1:0] selector;
    wire [4:0] suma;
    wire [3:0] resta, xor_datos, mayor;

    assign selector = {v, u};
    // El quinto bit guarda el acarreo
    assign suma = {1'b0, A} + {1'b0, B};
    assign resta = A - B;
    assign xor_datos = A ^ B;
    assign mayor = (A >= B) ? A : B;

    assign Y = (selector == 2'b00) ? resta :
               (selector == 2'b01) ? suma[3:0] :
               (selector == 2'b10) ? xor_datos : mayor;

    // Indicador de cada operacion
    assign flag_comb = (selector == 2'b00) ? (A < B) :
                       (selector == 2'b01) ? suma[4] :
                       (selector == 2'b10) ? (^xor_datos) : (A == B);
endmodule
