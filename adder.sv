module adder #(
  parameter integer DATA_WIDTH = 4
) (
  input  logic unsigned [1:0]A[DATA_WIDTH-1:0],
  input  logic unsigned [1:0]B[DATA_WIDTH-1:0],
  output logic unsigned [1:0]X[DATA_WIDTH:0]
);


  assign X[0] = A[0] + B[0];
  assign X[1] = A[1] + B[1];
  // Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, adder);
  end

endmodule