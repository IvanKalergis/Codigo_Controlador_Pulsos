import spinapi
from spinapi import Inst
spinapi.pb_set_debug(0)
spinapi.pb_select_board(0)
if spinapi.pb_init() != 0:
    print("Error initializing board: %s" % spinapi.pb_get_error())
    input("Please press a key to continue.")
    exit(-1)
spinapi.pb_core_clock(500)
spinapi.pb_start_programming(spinapi.PULSE_PROGRAM)
start=spinapi.pb_inst_pbonly(1,Inst.CONTINUE,0,100*spinapi.ms)
"""spinapi.pb_start_programming(spinapi.PULSE_PROGRAM)
start=spinapi.pb_inst_pbonly(int(self.PB_WIDTH[0][0]),Inst.LOOP,1,(self.PB_WIDTH[0][1])*spinapi.us)
print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[0][0]},Inst.LOOP,{1},({self.PB_WIDTH[0][1]})*spinapi.us)") # we only do one iteration because PB_WIDTH has all of the iterations
for i in range(1,len(self.PB_WIDTH)):# we start from one because we already did the 0 index
    if i!=len(self.PB_WIDTH) -1:
        print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.CONTINUE,0,({self.PB_WIDTH[i][1]})*spinapi.us)")
        spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.CONTINUE,0,(self.PB_WIDTH[i][1])*spinapi.us)
    else:
        print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.CONTINUE,0,({self.PB_WIDTH[i][1]})*spinapi.us)")
        spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.CONTINUE,0,(self.PB_WIDTH[i][1])*spinapi.us)
        print(f"spinapi.pb_inst_pbonly({self.PB_WIDTH[i][0]},Inst.END_LOOP,start,{self.PB_WIDTH[i][1]}")
        spinapi.pb_inst_pbonly(int(self.PB_WIDTH[i][0]),Inst.END_LOOP,start,self.PB_WIDTH[i][1])
spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,1*spinapi.us) # This instruction stops the pulse sequence. The duration is set to a very small value to ensure the stop instruction is executed almost immediately.
print(f"spinapi.pb_inst_pbonly(int(0),Inst.STOP,0,0.01*spinapi.us)")"""
spinapi.pb_inst_pbonly(0,Inst.BRANCH,start,200*spinapi.ms)
spinapi.pb_stop_programming()  # This function call signals the end of programming the pulse sequence. It tells the SpinAPI library that the sequence definition is complete and the pulse program can be finalized
spinapi.pb_reset() 
spinapi.pb_start()
print("Continuing will stop program execution\n");
input("Please press a key to continue.")
spinapi.pb_stop()
spinapi.pb_close()
