`timescale 1ns/1ps
// Diagnostico TEMPORAL de cableado. No es el top del parcial.
// rst_n=1 -> LED fisicos (por indice led[7:0]) muestran A[3:0],B[3:0].
// rst_n=0 -> LED fisicos muestran enable,000,abcd.
// Las entradas van a GND para 1 logico; LED electricamente activo-bajo.
module tang_diag_20230113(
    input wire clk,
    input wire [12:0] sw,
    input wire rst_n,
    output wire [7:0] led
);
    reg [12:0] sw_meta, sw_sync;
    always @(posedge clk) begin
        sw_meta <= ~sw;
        sw_sync <= sw_meta;
    end
    wire [7:0] bits_encendidos;
    assign bits_encendidos = rst_n ? {sw_sync[7:4], sw_sync[3:0]}
                                   : {sw_sync[12], 3'b000, sw_sync[11:8]};
    assign led = ~bits_encendidos;
endmodule
