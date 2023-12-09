#### 5143-P03
#### 5143 CPU Scheduling Simulation

#### Group Members


- Divya Podila
- Soundarya Boyeena
- Rakesh Rapalli

#### Overview:
This is a project written in python that implements a CPU Scheduling Simulation.
This project will implement a Simulation of CPU for different Scheduling Algorithms like "FCFS", "Priority Based" and "Round Robin" to -
-Maximizing throughput (the total amount of work completed per time unit)
-Minimizing wait time (time from work becoming ready until the first point it begins execution) (We define it slightly differently)
-Minimizing latency or response time (time from work becoming ready until it is finished)
-maximizing fairness (equal CPU time to each process, or more generally appropriate times according to the priority and workload of each process).
-In practice, these goals often conflict (e.g. throughput versus latency), thus a scheduler will implement a suitable compromise.
The scheduler will attempt to accomplish the above goals by moving a process around through a series of states. Of course each process has its own unique set of needs (IO intensive, CPU intensive for example), and the scheduler cannot change what the process needs or when it needs it. Its power is in determining when a process gets access to a resource, the most important of which is the CPU. If it's smart about the order in which it allows access, then the above goals can be met.
#### Instructions

import all the packages:
- dearpygui.dearpygui
- sys
- threading
- time

Then run the Sim.py

***Command***:
 ***python sim.py sched=PB  cpus=4 ios=2 input=cpu_intense_500.dat timedelay=0.1***
 
 -Arguments:
 
 -> sched Type:
 
          = RR for RoundRobin Scheduling  (Enter "RR" in caps only since, Case sensitive)
 
          = PB for Priority Based Scheduling (Enter "PB" in caps only)
          
          = FCFS for First Come First Serve Scheduling (Enter "FCFS" in caps only)
          
          = If sched type is not given, by default "FCFS" will be simulated.
          
 -> cpus and ios = Select any number of cpus and ios ( if no value is given , default values "4" and "2" wil be considered)
 
 -> input =  input file (file.dat) format
 
 -> timedelay =  Enter desired time delay, between 0.01 to 1 0.01 being slowest speed of simulation and 1 being fastest speed

 ***DearPyGUI***


 ***DearPyGui Simulation Window***
 ![image](https://github.com/divyapodila/5143-Opsys-101/blob/main/Assignments/P03/DearPyGUI_Simulation.png)
