`timescale 1ns/1ps
module result_register(
    input wire clk, rst, en,
    input wire [3:0] Y,
    input wire flag_comb,
    output reg [3:0] Q,
    output reg flag_q
);
    // Reset con prioridad
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            Q <= 4'b0000;
            flag_q <= 1'b0;
        end else if (en) begin
            Q <= Y;
            flag_q <= flag_comb;
        end
    end
endmodule
