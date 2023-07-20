# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an mac_array module
import os
import random
import sys
from pathlib import Path
import numpy as np

import cocotb
from cocotb.runner import get_runner
from cocotb.clock import Clock
from cocotb.triggers import Timer


@cocotb.test()
async def mac_array_basic_test(dut):
    """Test for 5 + 10"""

    #A = 5
    #B = 10
    input_seq_len = 4        
    kernel_width_max = 2             
    input_channel_max = 4          
    output_channel_max = 4     
    a =[1 ,2]
    b =[1 ,2]

##################################    GOLDEN MODEL  ##############################
    x =[1, 2 ,3, 4, 0]
   
    w = []
    for i in range(1, 5):
        row= []
        for j in range( 1, 3):
            row.append(i +j)
            #print(row[j-1])
        w.append(row)

    for i in range(0, 4):
        row= []
        for j in range( 0, 2):
            print(w[i][j])
    print("weight printing over!")   

    out = []
    for i in range(0,4):
       out_row = []
       for j in range(0,4): 
           out_row.append(x[i]*w[j][0] + x[i+1]*w[j][1])
           #print(out[i][j])
       out.append(out_row)

    for i in range(0, 4):
        row= []
        for j in range( 0, 4):
            print(out[i][j])
    print("Output printing over!")  

###################################     END OF GOLDEN MODEL     ###################################


    activ_send =[]
    weight_send =[]
    #Clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())   
    #Reset
    dut.rst.value = 1
    await Timer(10, units="ns")
    dut.rst.value = 0
    dut.activ_in[0] = 0
    dut.activ_in[1] = 0
    dut.activ_in[2] = 0
    dut.activ_in[3] = 0

    dut.weight_in[0] = 0
    dut.weight_in[1] = 0
    dut.weight_in[2] = 0
    dut.weight_in[3] = 0

    await Timer(10, units="ns")
    print( dut.accum[0].value )
    #clock cycle 1
    dut.activ_in[0] = x[0]
    dut.activ_in[1] = 0
    dut.activ_in[2] = 0
    dut.activ_in[3] = 0

    dut.weight_in[0] = w[0][0]
    dut.weight_in[1] = 0
    dut.weight_in[2] = 0
    dut.weight_in[3] = 0

    await Timer(1, units="ns")

    
    #clock cycle 2
    dut.activ_in[0] = x[1]
    dut.activ_in[1] = x[1]
    dut.activ_in[2] = 0
    dut.activ_in[3] = 0

    dut.weight_in[0] = w[0][1]
    dut.weight_in[1] = w[1][0]
    dut.weight_in[2] = 0
    dut.weight_in[3] = 0

    await Timer(1, units="ns")
    
    #clock cycle 3
    dut.activ_in[0] = 0
    dut.activ_in[1] = x[2]
    dut.activ_in[2] = x[2]
    dut.activ_in[3] = 0

    dut.weight_in[0] = 0
    dut.weight_in[1] = w[1][1]
    dut.weight_in[2] = w[2][0]
    dut.weight_in[3] = 0

    await Timer(1, units="ns")

    #clock cycle 4
    dut.activ_in[0] = 0
    dut.activ_in[1] = 0
    dut.activ_in[2] = x[3]
    dut.activ_in[3] = x[3]

    dut.weight_in[0] = 0
    dut.weight_in[1] = 0
    dut.weight_in[2] = w[2][1]
    dut.weight_in[3] = w[3][0]

    await Timer(1, units="ns")

    #clock cycle 5
    dut.activ_in[0] = 0
    dut.activ_in[1] = 0
    dut.activ_in[2] = 0
    dut.activ_in[3] = 0

    dut.weight_in[0] = 0
    dut.weight_in[1] = 0
    dut.weight_in[2] = 0
    dut.weight_in[3] = w[3][1]


    await Timer(4, units="ns")
    
    for i in range( 0,4 ):
        for j in range( 0, 4 ):
            if ( out[i][j]== dut.accum[i*4 + j]):
                print( "success verifying %d th output" %(i*4 + j +1 ) )
            else :
                print( "error verifying %d th output " %(i*4 + j +1 ) )    

def test_mac_array_runner():
    """Simulate the mac_array example using the Python runner.

    This file can be run directly or via pytest discovery.
    """
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent
    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path))

    verilog_sources = []

    if hdl_toplevel_lang == "verilog":
        verilog_sources = [proj_path/"mac_array.sv"]
   

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path ))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="mac_array",
        always=True,
    )
    runner.test(hdl_toplevel="mac_array", test_module="test_mac_array")


if __name__ == "__main__":
    test_mac_array_runner()
