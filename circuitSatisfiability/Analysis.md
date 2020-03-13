# Circuit Satisfiability
Execution time decreases roughly linearly as the amount of processes increase. With a single process, it takes about 356 seconds to run Circuit Satisfiability. With two, it is about twice as fast, with three, about three times as fast, and, with four, about four times as fast. The decreasing time gains can be explained by the overhead of processes. <br>

The overhead appears to be fairly consistent; <br>

$\dfrac{356}{2} = 178 s$

Execution time for two processes is 182 seconds, it seems that it takes about 5 seconds to create a new process.

$\dfrac{356}{3} = 118 s$

Execution time for three processes is 127 seconds, it seems that it takes about 10 seconds to create two new processes. 

$\dfrac{356}{4} = 89 s$

Execution time for four processes is 101 seconds, it seems that it takes about 12 to create three new processes. 

All but the four process-run follow the same pattern: it takes about 5 seconds to create a new process.

