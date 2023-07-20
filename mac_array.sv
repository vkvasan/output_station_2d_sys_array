
module mac_array #(
  parameter bw = 8,
            input_seq_len = 4,        //should be 100
            kernel_width_max = 2,             //should be 7
            input_channel_max = 4,          //should be 256
            output_channel_max = 4,     //should be 8
            bw_psum = 2*bw + $clog2(kernel_width_max * input_channel_max)
  )(
    input logic [input_seq_len-1:0]activ_in[bw -1:0] ,
    input logic [output_channel_max-1:0]weight_in[bw -1:0] ,
    input logic clk,
    input logic rst,
    output logic [(input_seq_len*output_channel_max)-1:0]accum[bw_psum-1:0]
);
// Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(5, mac_array);
  end

genvar i;
genvar j;

logic [input_seq_len:0][output_channel_max:0]activ_wire[bw -1:0];  //wire;
logic [input_seq_len:0][output_channel_max:0]weight_wire[bw -1:0];  //wire;

generate
for(i=0; i<input_seq_len; i = i+1) begin  : assign_activations
    assign activ_wire[i][0] = activ_in[i];
end
endgenerate

generate
for(j=0; j<output_channel_max; j = j+1) begin : assign_weights
    assign weight_wire[0][j] = weight_in[j];
end
endgenerate


generate
for(i=0; i<input_seq_len; i = i+1) begin : outer
  for(j=0; j<output_channel_max; j=j+1) begin : inner
    mac_unit inst (.clk(clk), .rst(rst), .activ_in( activ_wire[i][j]), .weight_in( weight_wire[i][j]), .activ_out( activ_wire[i][j+1] ), .weight_out( weight_wire[i+1][j] ), .accum( accum[i*output_channel_max + j] )   );
  end
end
endgenerate



endmodule


module mac_unit #(
  parameter bw = 8,
            input_seq_len = 4,        //should be 100
            kernel_width_max = 2,             //should be 7
            input_channel_max = 4,          //should be 256
            output_channel_max = 4,     //should be 8
            bw_psum = 2*bw + $clog2(kernel_width_max * input_channel_max)
  )(
    input logic [bw-1:0]activ_in,
input logic [bw-1:0]weight_in,
input logic clk,
input logic rst,
output logic [bw-1:0]activ_out,
output logic [bw-1:0]weight_out,
output logic [bw_psum-1:0]accum
);

//Declaration of Variables( registers and wires )

logic [bw-1:0]activ_in_reg;
logic [bw-1:0]weight_in_reg;
logic [bw_psum-1:0]accum_out_wire;

assign accum_out_wire = accum;
assign activ_out = activ_in_reg;
assign weight_out = weight_in_reg;


always@(posedge clk)begin
if ( rst ) begin
    activ_in_reg <= 0;
    weight_in_reg <= 0;
    accum <=0;
end 
else begin
    activ_in_reg <= activ_in;
    weight_in_reg <= weight_in;   
    accum <= activ_in_reg * weight_in_reg + accum_out_wire;
end    

end
endmodule