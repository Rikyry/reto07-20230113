`timescale 1ns/1ps
module tb_tang_top_20230113;
    reg clk=0,rst_n=1;
    reg [12:0] sw=13'h1fff;
    wire [7:0] led;
    tang_top_20230113 dut(.clk(clk),.sw(sw),.rst_n(rst_n),.led(led));
    always #10 clk=~clk;
    initial begin
        $dumpfile("sim/tang_top_20230113.vcd"); $dumpvars(0,tb_tang_top_20230113);
        repeat(5) @(negedge clk);
        if(led!==8'hff) $fatal(1,"power-up reset, all LEDs off");
        #2; sw=~{1'b0,4'b0010,4'd15,4'd1};
        @(posedge clk); #1; if(dut.sw_sync!==0) $fatal(1,"first-stage leak");
        @(posedge clk); #1; if(dut.sw_sync!==~sw) $fatal(1,"two-stage synchronizer, active-low switches");
        @(negedge clk); sw[12]=0;
        repeat(3) @(posedge clk); #1;
        if(led!==8'h4f) $fatal(1,"sum carry, active-low LED ordering, enable LED");
        @(negedge clk); sw[12]=1;
        repeat(3) @(posedge clk); #1;
        if(led!==8'hcf) $fatal(1,"disabled LED off, retained result");
        @(negedge clk); sw=~{1'b0,4'b0011,4'd7,4'd7};
        repeat(3) @(posedge clk); #1;
        if(led!==8'h8f) $fatal(1,"current control / retained Q");
        @(negedge clk); sw[12]=0;
        repeat(3) @(posedge clk); #1;
        if(led!==8'h08) $fatal(1,"capture max tie");
        @(negedge clk); #2; rst_n=0; #1;
        if(led[4:0]!==5'b11111) $fatal(1,"reset assertion must be asynchronous");
        #2; rst_n=1; #1;
        if(dut.rst!==1) $fatal(1,"early reset deassertion");
        @(posedge clk); #1; if(dut.rst!==1) $fatal(1,"first reset stage");
        @(posedge clk); #1;
        if(dut.rst!==0 || led[4:0]!==5'b11111) $fatal(1,"reset release captures prematurely");
        @(posedge clk); #1;
        if(led[4:0]!==5'b01000) $fatal(1,"capture after synchronized reset release");
        $display("PASS board adapter: active-low J3 switches, LEDx8 polarity and eight outputs, synchronization, stored Q/flag and reset");
        $finish;
    end
    initial begin #10000; $fatal(1,"timeout"); end
endmodule
