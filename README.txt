-----------------------------------------------------------------------------
Diffusion simulation in dynamic networks
Python 3
-----------------------------------------------------------------------------

Author   : Alice Albano
Email    : albano_alice@yahoo.fr
Location : Paris, France
Time	 : January 2014

-----------------------------------------------------------------------------

Disclaimer:
If you find a bug, please send a bug report to albano_alice@yahoo.fr
including if necessary the input file and the parameters that caused the bug.
You can also send me any comment or suggestion about the program.

Note that the program is expecting a friendly use and therefore does not make
much verifications about the arguments.

-----------------------------------------------------------------------------

The diffusion simulation happens in two different parts :
- first, the simulation itself, which gives a result file
- second, the analysis of the result file

This README gives an example for a simple use of the programm. For more details instructions and informations, see the file manual.pdf

Before running a simulation, you need to have three files (or four if you use communities):
1. 	The graph file (must be sorted by increasing "begin_link")
	Format:
	oriented = no/yes
	weighted = no/yes
	node1 node2 begin_link end_link optional_weight
	node2 node3 begin_link end_link optional_weight
	...

	example in the file graph.txt

2. 	The file containing the diffusion model (described in xml)
	Format:
	<model>
		<states>
			<state id="state1"/>
			<state id="state2" />
			<state id="state3" />
		</states>
		<edges>
			<edge source = "state1" target = "state2" rule = "rule1" transition = "transition_rule1" />
			<edge source = "state2" target = "state3" rule = "ruel2" transition = "transition_rule2" />
		</edges>
	</model>

	example in the file sir.xml
	This format allows you to define your own diffusion model. To see more details about acceptes rules and transition rules, see the Manual.pdf.

3.	The file containing the initial state of each node in the graph.
	Format:
	node1 state1
	node2 state2
	node3 state1
	...
	
	example in ini_states.txt

4. 	Optionnally, if you want to use dynamic communities for the simulation of the diffusion, you need a file describing these communities. File must be sorted by increasing "time_begin".
	Format:
	community1 node1 time_begin time_end
	community2 node2 time_begin time_end
	community2 node3 time_begin time_end
	...
	
	example in comm.txt

------------------------------------------------------------------------------

Diffusion simulation:

Run the diffusion.py program with your arguments :
python3 diffusion.py sir.xml graph.txt ini_states.txt

This products the results.txt file, containing the trace of the diffusion.

If you want to use communities for the simulation of the diffusion:
python3 diffusion.py sir.xml graph.txt ini_states.txt comm.txt

------------------------------------------------------------------------------

Analysis of the trace:

Run the trace_analysis programm:
python3 trace_analysis.py results.txt sir.xml

(Be careful to give the same diffusion model as in the simulation to have pertinent results.)
This progamm creates several curves in your current repository.

If you also want plots using communities:
python3 trace_analysis.py results.txt sir.xml comm.txt

------------------------------------------------------------------------------

This programm uses python3 and the matplotlib library (version for python3).

------------------------------------------------------------------------------
