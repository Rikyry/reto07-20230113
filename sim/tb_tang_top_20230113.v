`timescale 1ns/1ps
module tb_tang_top_20230113;
    reg clk=0,rst_n=1;
    reg [12:0] sw=0;
    wire [6:0] led;
    tang_top_20230113 dut(.clk(clk),.sw(sw),.rst_n(rst_n),.led(led));
    always #10 clk=~clk;
    initial begin
        $dumpfile("sim/tang_top_20230113.vcd"); $dumpvars(0,tb_tang_top_20230113);
        repeat(5) @(negedge clk);
        if(led!==0) $fatal(1,"power-up reset");
        #2; sw={1'b0,4'b0010,4'd15,4'd1};
        @(posedge clk); #1; if(dut.sw_sync!==0) $fatal(1,"first-stage leak");
        @(posedge clk); #1; if(dut.sw_sync!==sw) $fatal(1,"two-stage synchronizer");
        @(negedge clk); sw[12]=1;
        repeat(3) @(posedge clk); #1;
        if(led!==7'b0110000) $fatal(1,"sum carry, LED ordering");
        @(negedge clk); sw[12]=0;
        repeat(3) @(posedge clk); #1;
        @(negedge clk); sw={1'b0,4'b0011,4'd7,4'd7};
        repeat(3) @(posedge clk); #1;
        if(led!==7'b1110000) $fatal(1,"current control / retained Q");
        @(negedge clk); sw[12]=1;
        repeat(3) @(posedge clk); #1;
        if(led!==7'b1110111) $fatal(1,"capture max tie");
        @(negedge clk); #2; rst_n=0; #1;
        if(led[4:0]!==0) $fatal(1,"reset assertion must be asynchronous");
        #2; rst_n=1; #1;
        if(dut.rst!==1) $fatal(1,"early reset deassertion");
        @(posedge clk); #1; if(dut.rst!==1) $fatal(1,"first reset stage");
        @(posedge clk); #1;
        if(dut.rst!==0 || led[4:0]!==0) $fatal(1,"reset release captures prematurely");
        @(posedge clk); #1;
        if(led[4:0]!==5'b10111) $fatal(1,"capture after synchronized reset release");
        $display("PASS board adapter: 13 switch bits synchronized, current u/v, stored Q/flag, asynchronous assertion and two-clock reset release");
        $finish;
    end
    initial begin #10000; $fatal(1,"timeout"); end
endmodule
