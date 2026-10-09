`timescale 1ns/1ps
module control_logic(
    input wire a, b, c, d,
    output wire u, v
);

    assign u = (a & b) | (a & d) | (~b & c);
    assign v = (~a & d) | (c & d) | (b & ~c);
endmodule
