`timescale 1ns/1ps
module tang_top_20230113(
    input wire clk,
    input wire [12:0] sw,
    input wire rst_n,
    output wire [7:0] led
);
    reg [12:0] sw_meta, sw_sync;
    reg [1:0] rst_pipe = 2'b11;
    wire rst_raw, rst;
    wire u, v, unused_flag_comb, flag_q;
    wire [3:0] unused_Y, Q;

    assign rst_raw = ~rst_n;

    always @(posedge clk or posedge rst_raw) begin
        if (rst_raw)
            rst_pipe <= 2'b11;
        else
            rst_pipe <= {rst_pipe[0], 1'b0};
    end
    assign rst = rst_pipe[1];

    always @(posedge clk) begin
        sw_meta <= ~sw;
        sw_sync <= sw_meta;
    end

    top_20230113 sistema(
        .a(sw_sync[11]), .b(sw_sync[10]),
        .c(sw_sync[9]), .d(sw_sync[8]),
        .A(sw_sync[7:4]), .B(sw_sync[3:0]),
        .clk(clk), .rst(rst), .en(sw_sync[12]),
        .u(u), .v(v), .Y(unused_Y), .flag_comb(unused_flag_comb),
        .Q(Q), .flag_q(flag_q)
    );

    assign led = ~{sw_sync[12], v, u, flag_q, Q};
endmodule
