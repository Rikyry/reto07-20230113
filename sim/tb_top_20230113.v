`timescale 1ns/1ps
module tb_top_20230113;
    reg a=0,b=0,c=0,d=0,clk=0,rst=0,en=0;
    reg [3:0] A=0,B=0;
    wire u,v,flag_comb,flag_q;
    wire [3:0] Y,Q;
    integer m,aa,bb,vecs=0,comparisons=0,errors=0,temporal=0;
    reg eu,ev,ef; reg [3:0] ey;
    top_20230113 dut(.a(a),.b(b),.c(c),.d(d),.A(A),.B(B),
        .clk(clk),.rst(rst),.en(en),.u(u),.v(v),.Y(Y),
        .flag_comb(flag_comb),.Q(Q),.flag_q(flag_q));
    always #10 clk=~clk;

    function ref_u;
        input integer n;
        begin case(n) 2,3,9,10,11,12,13,14,15:ref_u=1; default:ref_u=0; endcase end
    endfunction
    function ref_v;
        input integer n;
        begin case(n) 1,3,4,5,7,11,12,13,15:ref_v=1; default:ref_v=0; endcase end
    endfunction
    task model;
        input integer ctrl,x,z;
        integer val,j,par;
        begin
            eu=ref_u(ctrl); ev=ref_v(ctrl);
            case ({ev,eu})
                0:begin val=(x-z+16)%16; ef=(x<z); end
                1:begin val=(x+z)%16; ef=(x+z>15); end
                2:begin val=x^z; par=0; for(j=0;j<4;j=j+1) par=par+((val>>j)&1); ef=(par%2); end
                3:begin val=(x>z)?x:z; ef=(x==z); end
            endcase
            ey=val;
        end
    endtask
    task check_q;
        input integer number,value,flag;
        input [511:0] label;
        begin
            temporal=temporal+1; comparisons=comparisons+2;
            if(Q!==value[3:0] || flag_q!==flag[0]) begin
                errors=errors+1; $display("FAIL temporal %0d %0s: Q=%h flag=%b expected=%0d/%0d",number,label,Q,flag_q,value,flag);
            end else $display("PASS temporal %0d: %0s",number,label);
        end
    endtask
    initial begin
        $dumpfile("sim/top_20230113.vcd"); $dumpvars(0,tb_top_20230113);
        #2; rst=1; #1;
        for(m=0;m<16;m=m+1) begin
            {a,b,c,d}=m;
            for(aa=0;aa<16;aa=aa+1) for(bb=0;bb<16;bb=bb+1) begin
                A=aa; B=bb; model(m,aa,bb); #2;
                vecs=vecs+1; comparisons=comparisons+4;
                if(u!==eu || v!==ev || Y!==ey || flag_comb!==ef) begin
                    errors=errors+1;
                    $display("FAIL ctrl=%04b A=%0d B=%0d got=%b%b/%h/%b expected=%b%b/%h/%b",m[3:0],aa,bb,v,u,Y,flag_comb,ev,eu,ey,ef);
                end
            end
        end
        $display("COMBINATIONAL: vectors=%0d comparisons=%0d errors=%0d",vecs,comparisons,errors);
        @(negedge clk); rst=0; en=0; #2; rst=1; #1;
        check_q(1,0,0,"assert reset between edges");
        en=1; @(posedge clk); #1;
        check_q(2,0,0,"reset has priority over enable at edge");
        @(negedge clk); #2; rst=0; #1;
        check_q(3,0,0,"release reset without capture edge");

        {a,b,c,d}=0; A=0; B=1;
        @(posedge clk); #1; check_q(4,15,1,"capture RESTA with borrow");

        @(negedge clk); {a,b,c,d}=2; A=15; B=1;
        @(posedge clk); #1; check_q(5,0,1,"capture SUMA with carry");

        @(negedge clk); {a,b,c,d}=1; A=0; B=7;
        @(posedge clk); #1; check_q(6,7,1,"capture XOR with odd parity");

        @(negedge clk); {a,b,c,d}=3; A=15; B=15;
        @(posedge clk); #1; check_q(7,15,1,"capture MAYOR with tie A=B=15");
        @(negedge clk); en=0; {a,b,c,d}=2; A=1; B=1;
        @(posedge clk); #1; check_q(8,15,1,"retain while disabled despite new data");
        @(negedge clk); en=1;
        @(posedge clk); #1; check_q(9,2,0,"enable again and capture");
        @(negedge clk); #2; A=9; B=0; #1;
        check_q(10,2,0,"change data between edges with enable high");

        #1; rst=1; #1; check_q(11,0,0,"async reset clears nonzero Q between edges");
        @(negedge clk); #2; rst=0; {a,b,c,d}=3; A=9; B=0;
        @(posedge clk); #1; check_q(12,9,0,"capture again after reset, B=0");
        $display("SUMMARY vectors=%0d temporal=%0d total_comparisons=%0d errors=%0d",vecs,temporal,comparisons,errors);
        if(vecs!=4096 || temporal!=12 || errors!=0) $fatal(1,"verification failed");
        $display("PASS tb_top_20230113"); $finish;
    end
    initial begin #100000; $fatal(1,"timeout"); end
endmodule
