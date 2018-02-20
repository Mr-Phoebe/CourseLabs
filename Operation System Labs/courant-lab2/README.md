Process Scheduler
===

All code written in C++.

Input
---

- AT: Arrival Time
- TC: Total Cost, the total time for CPU running
- CB: CPU Burst, real time for one CPU Burst is uniformly distributed in [1, CB].
- IO: IO Burst, real time for one IO Burst is uniformly distributed in [1, IO].

AT TC CB IO
00 5  3  5
04 10 4  5

Running
---

- type:
	- F: First come ,first served
	- S: Shortest job, first served
	- R: Round Robin

compile: g++ scheduler.gpp
run____: ./a.out [-v] -s[type] [inputfile] [randfile]

Or, use `run.sh` for test.

```
./run.sh [FSR]
```

Follows format given by assignment instructions^^.