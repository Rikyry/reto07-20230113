`timescale 1ns/1ps
module top_20230113(
    input wire a, b, c, d,
    input wire [3:0] A, B,
    input wire clk, rst, en,
    output wire u, v,
    output wire [3:0] Y,
    output wire flag_comb,
    output wire [3:0] Q,
    output wire flag_q
);
    control_logic control(
        .a(a), .b(b), .c(c), .d(d),
        .u(u), .v(v)
    );

    datapath operaciones(
        .A(A), .B(B), .u(u), .v(v),
        .Y(Y), .flag_comb(flag_comb)
    );

    result_register registro(
        .clk(clk), .rst(rst), .en(en),
        .Y(Y), .flag_comb(flag_comb),
        .Q(Q), .flag_q(flag_q)
    );
endmodule
