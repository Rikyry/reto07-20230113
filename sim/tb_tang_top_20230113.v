`timescale 1ns/1ps
module tb_tang_top_20230113;
    reg clk=0,rst_n=1;
    reg [12:0] sw=13'h1fff;
    wire [7:0] led;
    wire [7:0] panel_on;
    assign panel_on=~{led[0],led[1],led[2],led[3],led[4],led[5],led[6],led[7]};
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
        if(panel_on!==8'b00001101) $fatal(1,"L1-L8 sum carry layout");
        @(negedge clk); sw[12]=1;
        repeat(3) @(posedge clk); #1;
        if(led!==8'hcf) $fatal(1,"disabled LED off, retained result");
        if(panel_on!==8'b00001100) $fatal(1,"L8 enable off, L1-L5 retained");
        @(negedge clk); sw=~{1'b0,4'b0011,4'd7,4'd7};
        repeat(3) @(posedge clk); #1;
        if(led!==8'h8f) $fatal(1,"current control / retained Q");
        if(panel_on!==8'b00001110) $fatal(1,"L6-L7 current control with retained result");
        @(negedge clk); sw[12]=0;
        repeat(3) @(posedge clk); #1;
        if(led!==8'h08) $fatal(1,"capture max tie");
        if(panel_on!==8'b11101111) $fatal(1,"L1-L4 weights 1 2 4 8, result 7 and tie");
        @(negedge clk); #2; rst_n=0; #1;
        if(led[4:0]!==5'b11111) $fatal(1,"reset assertion must be asynchronous");
        if(panel_on!==8'b00000111) $fatal(1,"reset clears L1-L5 only");
        #2; rst_n=1; #1;
        if(dut.rst!==1) $fatal(1,"early reset deassertion");
        @(posedge clk); #1; if(dut.rst!==1) $fatal(1,"first reset stage");
        @(posedge clk); #1;
        if(dut.rst!==0 || led[4:0]!==5'b11111) $fatal(1,"reset release captures prematurely");
        @(posedge clk); #1;
        if(led[4:0]!==5'b01000) $fatal(1,"capture after synchronized reset release");
        @(negedge clk); sw=~{1'b1,4'b0000,4'd0,4'd0};
        repeat(3) @(posedge clk); #1;
        if(led!==8'h7f || panel_on!==8'b00000001)
            $fatal(1,"0 minus 0, only G5 enable on");
        @(negedge clk); sw[4]=0;
        repeat(3) @(posedge clk); #1;
        if(led!==8'h7e || panel_on!==8'b10000001)
            $fatal(1,"G10 grounded: 1 minus 0, J5 result and G5 enable on");
        @(negedge clk); sw[12]=1;
        repeat(3) @(posedge clk); #1;
        if(led!==8'hfe || panel_on!==8'b10000000)
            $fatal(1,"enable off must retain result 1");
        @(negedge clk); rst_n=0; #1;
        if(led!==8'hff || panel_on!==8'h00)
            $fatal(1,"reset with enable off must clear result");
        $display("PASS board adapter: J5 Q0, H5 Q1, H8 Q2, H7 Q3; synchronization, retention, reset, 0-0 and 1-0 with G10/E11");
        $finish;
    end
    initial begin #10000; $fatal(1,"timeout"); end
endmodule
