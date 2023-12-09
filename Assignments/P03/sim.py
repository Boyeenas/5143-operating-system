import time
import threading
import sys
import dearpygui.dearpygui as dpg



class Queue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        #return ",".join(self.queue)
        return ",".join([str(p.pid) for p in self.queue])

    def is_empty(self):
        return len(self.queue)==0

    def addPCB(self,pcb):
        self.queue.append(pcb)
    
    def removePCB(self):
        item = self.queue[0]
        del self.queue[0]
        return item

    def decrement(self):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call decrementIoBurst
        pass
    
    def incrememnt(self,what='waittime'):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call incrementwaittime
        if what =='waittime':
            for pcb in self.queue:
                pcb.waitQueueTime+=1
        elif what == 'readytime':
            for pcb in self.queue:
                pcb.readyQueueTime+=1
        
        pass


class PB_Queue(Queue):
    def __init__(self):
        super().__init__()

    def addPCB(self, pcb):
        super().addPCB(pcb)
        self.queue=sorted(self.queue,key=lambda x :x.priority)
    

class SysClock:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
        if not 'clock' in self.__dict__: 
            self.clock = 0
    

class CPU:
    def __init__(self):
        self.busy = False
        self.runningPCB = None

    def decrementCurrentProcess(self):
        self.runningPCB.decrementCpuBurst()
    
    def loadProcess(self,pcb):
        self.runningPCB = pcb

    def testKickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            pass
            # kick it off the cpu


class IO:
    def __init__(self):
        self.busy = False
        self.runningPCB = None

    def decrementCurrentProcess(self):
        self.runningPCB.decrementCpuBurst()
    
    def loadProcess(self,pcb):
        self.runningPCB = pcb

    def testKickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            pass
            # kick it off the cpu


class PCB:
    def __init__(self,pid,bursts,at,priority):
        self.pid = pid     
        self.priority = priority     # 0
        self.arrivalTime = at
        self.bursts = bursts    # 5 3  2 2  2 3  3 3 3 2 3 3 4 2 5 2 5 3 3 3 4
        self.currBurst = 'CPU'
        self.currBurstIndex = 0
        self.Quantum =0
        self.cpuBurst = 0
        self.ioBurst = 0
        self.readyQueueTime = 0
        self.waitQueueTime = 0
        self.turnAroundTime = 0

    def decrementCpuBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        self.currBurstIndex += 1
    
    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]
    
class Simulator:
    def __init__(self,datfile,n_cpu=1,n_io=1,sched='FCFS',timeSlice=2):
        self.datfile = datfile
        self.sched=sched
        self.timeSlice=timeSlice
        self.new = Queue()
        if sched=="PB":
            self.wait = PB_Queue()
        else:
            self.wait = Queue()
        self.running = []
        self.io = []
        if sched=="PB":
            self.ready = PB_Queue()
        else:
            self.ready = Queue()
        self.terminated = Queue()
        self.clock = SysClock()

        for i in range(n_cpu):
            self.running.append(CPU())
        
        for i in range(n_io):
            self.io.append(IO())
        self.messages=""
        self.work=0

        self.readData()

    def __str__(self):
        s = ""
        s += "datfile: " + self.datfile + "\n"
        s += "new queue: " + str(self.new) + "\n"
        s += "ready queue: " + str(self.ready) + "\n"
        s += "running: " + str(self.running.runningPCB.pid if self.running.runningPCB else None) + "\n"
        s += "wait queue: " + str(self.wait) + "\n"
        s += "terminated queue: " + str(self.terminated) + "\n"
        return s

    def log(self,message):
        if message!="":
            self.messages+="\n"
        self.messages+=f"At t:{self.clock.clock} {message}"

    def readData(self):
        with open(self.datfile) as f:
            self.data = f.read().split("\n")

        for process in self.data:
            if len(process) > 0:
                parts = process.split(' ')
                arrival = int(parts[0])
                pid = parts[1]
                priority = int(parts[2].strip("p"))
                bursts = [int(x) for x in parts[3:]]
                pcb = PCB(pid, bursts, arrival, priority)
                self.new.addPCB(pcb)
        
        self.new.queue=sorted(self.new.queue,key=lambda x : x.arrivalTime)

    def run_simulation(self):
        
        self.ready.incrememnt("readytime")
        self.wait.incrememnt("waittime")
        for pcb in self.ready.queue:
            pcb.turnAroundTime+=1
        for pcb in self.wait.queue:
            pcb.turnAroundTime+=1
        for cpu in self.running:
            if cpu.runningPCB:
                cpu.runningPCB.turnAroundTime+=1
        for io in self.io:
            if io.runningPCB:
                io.runningPCB.turnAroundTime+=1


        # Move processes from NEW to READY based on arrival time
        self.move_to_ready_from_new()

        # Run the CPU
        self.run_cpu()
        self.handle_io_bursts()
        self.clock.clock += 1

        # Handle IO bursts
        #self.handle_io_bursts()


    def move_to_ready_from_new(self):
        while not self.new.is_empty() and self.new.queue[0].arrivalTime <= self.clock.clock:
            process = self.new.removePCB()
            self.ready.addPCB(process)
            self.log(f"job p{process.pid} entered ready queue")


    def run_cpu(self):
        for i,cpu in enumerate(self.running):
            if cpu.runningPCB:
                cpu.decrementCurrentProcess()
                cpu.runningPCB.Quantum+=1
                cpu.runningPCB.cpuBurst+=1
                self.work+=1
                    
                if cpu.runningPCB.getCurrentBurstTime() == 0:
                    self.handle_cpu_completion(cpu)
                elif self.sched=="RR" and cpu.runningPCB.Quantum>=self.timeSlice:
                    self.ready.addPCB(cpu.runningPCB)
                    self.log(f"job p{cpu.runningPCB.pid} entered ready queue")
                    cpu.runningPCB.Quantum=0
                    cpu.runningPCB=None

        for i,cpu in enumerate(self.running):
            if not cpu.runningPCB and not self.ready.is_empty():
                process = self.ready.removePCB()
                cpu.loadProcess(process)
                self.log(f"job p{process.pid} obtained cpu:{i+1}")

                process.Quantum=0
        for i,cpu in enumerate(self.running):
            if self.sched=="PB":
                if not self.ready.is_empty():
                    if cpu.runningPCB:
                        if self.ready.queue[0].priority < cpu.runningPCB.priority:
                            pr=self.ready.removePCB()
                            self.ready.addPCB(cpu.runningPCB)
                            self.log(f"job p{cpu.runningPCB.pid} entered ready queue")
                            cpu.runningPCB=pr
                            self.log(f"job p{pr.pid} obtained cpu:{i+1}")

    def handle_cpu_completion(self,cpu):
        process = cpu.runningPCB

        process.incrementBurstIndex()

        if process.currBurstIndex < len(process.bursts):

               
                self.wait.addPCB(process)
                self.log(f"job p{process.pid} entered wait queue")


        else:
            process.currBurst = 'TERMINATED'
            self.terminated.addPCB(process)
            self.log(f"job p{process.pid} entered terminated queue")


        cpu.runningPCB = None

    def handle_io_bursts(self):
        

        for i,io in enumerate(self.io):
            if io.runningPCB:
                io.runningPCB.ioBurst+=1
                self.work+=1


                io.decrementCurrentProcess()
                if io.runningPCB.getCurrentBurstTime() == 0:
                    self.handle_io_completion(io)
        for i,io in enumerate(self.io):
            if not io.runningPCB and not self.wait.is_empty():
                process = self.wait.removePCB()
                io.loadProcess(process)
                self.log(f"job p{process.pid} obtained io:{i+1}")
        
        for i,io in enumerate(self.io):
            if self.sched=="PB":
                if not self.wait.is_empty() and io.runningPCB:
                    if self.wait.queue[0].priority < io.runningPCB.priority:
                        pr=self.wait.removePCB()
                        self.wait.addPCB(io.runningPCB)
                        self.log(f"job p{io.runningPCB.pid} entered wait queue")

                        io.runningPCB=pr
                        self.log(f"job p{pr.pid} obtained io:{i+1}")

       
    def handle_io_completion(self,io):
        process = io.runningPCB

        
        process.incrementBurstIndex()
        #process.cpuBurst += process.cpuBurst

        if process.currBurstIndex < len(process.bursts):

 
                self.ready.addPCB(process)
                self.log(f"job p{process.pid} entered ready queue")


        else:
            process.currBurst = 'TERMINATED'
            self.terminated.addPCB(process)
            self.log(f"job p{process.pid} entered terminated queue")


        io.runningPCB = None
    def isOver(self):
        for cpu in self.running:
            if cpu.runningPCB:
                return False
        for io in self.io:
            if io.runningPCB:
                return False
        return self.new.is_empty() and self.ready.is_empty() and self.wait.is_empty()



class QueueTable:
    def __init__(self,Title,queue):
        self.tag=Title
        self.queue=queue
        self.rows=[]
        self.lastlen=0
        with dpg.group():
            dpg.add_text(Title)
            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, no_host_extendX=True,no_host_extendY=True,
                    borders_innerV=True, borders_outerV=True, borders_outerH=True,row_background=True,
                    borders_innerH=True,tag=Title,height=280,scrollY=True,width=630
                    ):

                # use add_table_column to add columns to the table,
                # table columns use slot 0
                
                dpg.add_table_column(label="Arrival Time")
                dpg.add_table_column(label="Proc Id")
                dpg.add_table_column(label="Priority")
                dpg.add_table_column(label="CPU Burst")
                dpg.add_table_column(label="IO Burst")
                dpg.add_table_column(label="Ready Time")
                dpg.add_table_column(label="Wait Time")
                dpg.add_table_column(label="TAT")

                for i in range(1000):
                    r=[]
                    with dpg.table_row():

                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))

                    self.rows.append(r)
    def refresh(self,fast=False):

        if self.lastlen>len(self.queue.queue):
            for i,row in enumerate(self.rows[len(self.queue.queue):self.lastlen]):
                for cell in row:
                    dpg.set_value(item=cell,value="")
        iterateover=self.queue.queue
        if fast and len(self.queue.queue)>15:
            iterateover=self.queue.queue[:15]
            
        for i,pcb in enumerate(iterateover):
                dpg.set_value(item=self.rows[i][0],value=str(pcb.arrivalTime))
                dpg.set_value(item=self.rows[i][1],value=str(pcb.pid))
                dpg.set_value(item=self.rows[i][2],value=str(pcb.priority))
                dpg.set_value(item=self.rows[i][3],value=str(pcb.cpuBurst))
                dpg.set_value(item=self.rows[i][4],value=str(pcb.ioBurst))
                dpg.set_value(item=self.rows[i][5],value=str(pcb.readyQueueTime))
                dpg.set_value(item=self.rows[i][6],value=str(pcb.waitQueueTime))
                dpg.set_value(item=self.rows[i][7],value=str(pcb.turnAroundTime))
        if fast:
            self.lastlen=min(16,len(self.queue.queue))
        else:
            self.lastlen=len(self.queue.queue)
    

class CPUIOTable:
    def __init__(self,Title,cpus,sched="FCFS"):
        
        self.cpus=cpus
        self.rows=[]
        self.Title=Title
        self.devices=len(cpus)
        self.sched=sched

        with dpg.group():
            dpg.add_text(Title)
            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, no_host_extendX=True,no_host_extendY=True,
                    borders_innerV=True, borders_outerV=True, borders_outerH=True,row_background=True,
                    borders_innerH=True,tag=Title,height=180,scrollY=True,width=630
                    ):

                # use add_table_column to add columns to the table,
                # table columns use slot 0
                dpg.add_table_column(label=Title)
                dpg.add_table_column(label="Arrival Time")
                dpg.add_table_column(label="Proc Id")
                dpg.add_table_column(label="Priority")
                dpg.add_table_column(label="CPU Burst")
                dpg.add_table_column(label="IO Burst")
                dpg.add_table_column(label="Ready Time")
                dpg.add_table_column(label="Wait Time")
                dpg.add_table_column(label="TAT")
                if self.sched == "RR":
                    dpg.add_table_column(label="Q")


                for i in range(10):
                    r=[]
                    with dpg.table_row():

                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        r.append(dpg.add_text(""))
                        if self.sched == "RR":
                            r.append(dpg.add_text(""))



                    self.rows.append(r)
                
    def refresh(self):
       
        
        for i,cpu in enumerate(self.cpus):
                pcb=cpu.runningPCB
                dpg.set_value(item=self.rows[i][0],value=f"{self.Title} {i+1}")
                if pcb:
                    dpg.set_value(item=self.rows[i][1],value=str(pcb.arrivalTime))
                    dpg.set_value(item=self.rows[i][2],value=str(pcb.pid))
                    dpg.set_value(item=self.rows[i][3],value=str(pcb.priority))
                    dpg.set_value(item=self.rows[i][4],value=str(pcb.cpuBurst))
                    dpg.set_value(item=self.rows[i][5],value=str(pcb.ioBurst))
                    dpg.set_value(item=self.rows[i][6],value=str(pcb.readyQueueTime))
                    dpg.set_value(item=self.rows[i][7],value=str(pcb.waitQueueTime))
                    dpg.set_value(item=self.rows[i][8],value=str(pcb.turnAroundTime))
                    if self.sched == "RR":
                        dpg.set_value(item=self.rows[i][9],value=str(pcb.Quantum))

                else:
                    dpg.set_value(item=self.rows[i][1],value="")
                    dpg.set_value(item=self.rows[i][2],value="")
                    dpg.set_value(item=self.rows[i][3],value="")
                    dpg.set_value(item=self.rows[i][4],value="")
                    dpg.set_value(item=self.rows[i][5],value="")
                    dpg.set_value(item=self.rows[i][6],value="")
                    dpg.set_value(item=self.rows[i][7],value="")
                    dpg.set_value(item=self.rows[i][8],value="")
                    if self.sched == "RR":
                        dpg.set_value(item=self.rows[i][9],value="")








def parse_arguments():
    arguments = {}
    
    # Iterate through command-line arguments
    for arg in sys.argv[1:]:
        # Split each argument into key-value pairs
        key, value = arg.split('=')
        arguments[key] = value
    
    return arguments


def RUNSIMULATION():
    #while not sim.new.is_empty() or not sim.ready.is_empty() or sim.running.runningPCB or not sim.wait.is_empty():
    while not sim.isOver():
        if not Paused:
            a=time.time()
            if timedelay<0.09:
                new_table.refresh(True)
                ready_table.refresh(True)
                waiting_table.refresh(True)
                terminated_table.refresh(True)
                running_table.refresh()
                io_table.refresh()
                
            else:
                new_table.refresh()
                ready_table.refresh()
                waiting_table.refresh()
                terminated_table.refresh()
                running_table.refresh()
                io_table.refresh()

            dpg.set_value(item=f"CLOCK",value=f"CLOCK : {sim.clock.clock-1}     ")
            dpg.set_value(item=f"Activities",value=f"{sim.messages}")
            b=time.time()
            if timedelay>(b-a):
                time.sleep(timedelay-(b-a))
            
            sim.run_simulation()
        
    dpg.set_value(item=f"CLOCK",value=f"CLOCK : {sim.clock.clock-1}     ")
    dpg.set_value(item=f"Activities",value=f"{sim.messages}")
    dpg.set_value(item=f"THROUGHPUT",value=f"THROUGHPUT : {round(sim.work/sim.clock.clock,2)}")
    
    new_table.refresh()
    ready_table.refresh()
    waiting_table.refresh()
    terminated_table.refresh()
    running_table.refresh()
    io_table.refresh()


def Update_SIM(a):
    t = threading.Thread(target=RUNSIMULATION)
    t.start()

def togglePause():
    global Paused
    Paused=not Paused

new_table=None
ready_table=None
waiting_table=None
terminated_table=None
running_table=None
io_table=None
timedelay=0
Paused=False

if __name__ == "__main__":
    timeSlice=2
    arguments = parse_arguments()

    # Access values using keys
    sched = arguments.get('sched', "PR")
    if sched=="RR":
        timeSlice = int(arguments.get('timeslice', 2))
    cpus = int(arguments.get('cpus', 4))
    ios = int(arguments.get('ios', 2)) 
    input_file = arguments.get('input', 'small.dat')
    timedelay += float(arguments.get('timedelay', 1))

    
    sim = Simulator(input_file,n_cpu=cpus,n_io=ios,sched=sched,timeSlice=timeSlice)


    dpg.create_context()
    with dpg.handler_registry():
        dpg.add_key_press_handler(key=dpg.mvKey_Spacebar,callback=togglePause)
    with dpg.window(tag="Primary Window"):
        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Clock : 0     ",tag="CLOCK")
            dpg.add_text(default_value="THROUGHPUT : ---",tag="THROUGHPUT")
        with dpg.group(horizontal=True):
            with dpg.group():
                new_table=QueueTable("New Processes",sim.new)
                ready_table=QueueTable("Ready Processes",sim.ready)
                running_table=CPUIOTable("CPU",sim.running,sched=sched)
            with dpg.group():
                waiting_table=QueueTable("Waiting Processes",sim.wait)
                terminated_table=QueueTable("Terminated Processes",sim.terminated)
                io_table=CPUIOTable("IO",sim.io)
            with dpg.group():
                dpg.add_text(default_value="Activities")
                dpg.add_input_text(tag="Activities",readonly=True,multiline=True,height=800)
    # Parse command-line arguments
    


    dpg.set_frame_callback(1,Update_SIM)

    dpg.create_viewport(title='Cpu Scheduling - Simulation')
    dpg.setup_dearpygui()
    dpg.maximize_viewport()

    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()