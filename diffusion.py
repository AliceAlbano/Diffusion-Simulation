import random
from parser import *
from rules import *
import sys

if len(sys.argv) != 4 and len(sys.argv) != 5 :
	print("This program takes 3 or 4 arguments (in this order): the xml file containing the diffusion model, the graph file, the initial states file (and in option, the file containing the dynamic communities)")
	sys.exit()

if len(sys.argv) == 5 :
	comm_file = sys.argv[4]
else :
	comm_file = ""
model_file = sys.argv[1]
graph_file = sys.argv[2]
initial_states_file = sys.argv[3]

model = model_file.split(".")[0]
result = "result_" + model + "_" + graph_file

#statelist contains the states of the diffusion model
statelist=[]
#edgelist contains the transitions (and rules) between the states of the diffusion model
edgelist=[]

#dictionnary containing for each time (key), a dictionnary containing for each community (key named by id), the set of nodes present in this community at this instant. (for instantce community[time0][comm1] = set([1, 5, 6]))
community = {}
#presence is a dictionnary containing, for each time step (key), the list of nodes and links present in the graph at this time step. (format : presence[t0] = [set([nodes at t0]), set([links at t0])].
presence = {}

#same as presence, but for each link, contains its weight
presence_weight = {}

#Dictionnary containing for each node (key), its initial state in the diffusion process
inistate = {}

#Dictionnary containing, for each state (key), the list of nodes in this state
state_of_nodes = {}
# first time step in the graph
t_begin_graph = 0
# last time step in the graph
t_end_graph = 0

#time between two steps of the diffusion
timestep = 1

#file containing the trace of the diffusion
f_res = result


# Update the states of the nodes in inistate using the content of state_of_nodes
def update(inistate,state_of_nodes) :
	for state in state_of_nodes :
		for n in state_of_nodes[state] :
			inistate[n] = state

#write the trace of the diffusion at the time t in the res descriptor of file
def write_trace(state_of_nodes,t,res) :
	res.write("time " + str(t) + "\n")
	for state in state_of_nodes :
		res.write("state " + str(state) + "\n")
		for n in state_of_nodes[state]:
			res.write(str(n) + "\n")

#Simulation of the diffusion process
def diffusion(statelist,edgelist,presence,presence_weight,inistate,time,state_of_node,graph_desc_file,graph_oriented,community,comm_file_desc,t_old):	
	read_graph_light(graph_desc_file,presence,presence_weight,t_end_graph,time,graph_weighted)
	if comm_file_desc != None :
		read_community(comm_file_desc,community,t_end_graph,time,t_old)
#	print(presence)
	#For each transition between states
	for chg_state in edgelist :
		state1 = str(chg_state.attributes["source"].value)
		state2 = str(chg_state.attributes["target"].value)
		rule = str(chg_state.attributes["rule"].value)
		tr = str(chg_state.attributes["transition"].value)
		tr_rule = tr.split(" ")[0]
		tr_value = tr.split(" ")[1]
#		tr_value = float(tr.split(" ")[1])
		if rule == "neighborhood" : 
			if tr_rule == "probability":
				if tr_value == "weight" :
					change_neigh_proba_weight(presence_weight, time, state1, state2, state_of_nodes,inistate,graph_oriented)
				else :
					tr_value = float(tr_value)
					change_neigh_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented)
		
			elif tr_rule == "percentage" :
				if tr_value == "weight" :
					change_neigh_percentage_weight(presence_weight, time, state1, state2, state_of_nodes,inistate,graph_oriented)
				else :
					tr_value = float(tr_value)
					change_neigh_percentage(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented)
		
			elif tr_rule == "number" :
				tr_value = float(tr_value)
				change_neigh_number(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented)
			else :
				print("Accepted rules are probability, percentage and number")
				sys.exit()

		elif rule == "none" :
			if tr_rule == "probability":
				tr_value = float(tr_value)
				change_none_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented)

			else :
				print("Only a proability transition when it is independant from the graph")
				sys.exit()

		elif rule == "community" :
			if comm_file_desc == None :
				print("No community file")
				sys.exit()
			else :
				if tr_rule == "percentage" :
					tr_value = float(tr_value)
					change_comm_percentage(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc)

				elif tr_rule == "number" :
					tr_value = float(tr_value)
					change_comm_number(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc)

				elif tr_rule == "probability":
					tr_value = float(tr_value)
					change_comm_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc)

				else :
					print("Accepted transition are percentage, number and probability")
					sys.exit()

		else :
			print("Accepted rules are none, neighborhood and community")
			sys.exit()
			

parser(model_file,statelist,edgelist)
#parser('si.xml',statelist,edgelist)
i = 0
#for state in statelist :
#	print state.attributes["id"].value
t_end_graph = read_graph(graph_file,t_end_graph)
graph_desc_file = open(graph_file,'r')
lign = graph_desc_file.readline()
if comm_file == "" :
	comm_file_desc = None 
else : 
	comm_file_desc = open(comm_file,'r')
l = lign.split("=")
if "no" in l[1] :
	graph_oriented = "no"
else :
	graph_oriented = "yes"
lign = graph_desc_file.readline()
l = lign.split("=")
if "no" in l[1] :
	graph_weighted = "no"
else :
	graph_weighted = "yes"

print("oriented",graph_oriented)
print("weighted", graph_weighted)
initial_states(initial_states_file,inistate,state_of_nodes)
res = open(f_res,'w')
t_begin_diffusion = t_begin_graph
t_end_diffusion = t_end_graph
t = t_begin_diffusion
t_old = t
while t <= t_end_diffusion :
	print("time",t)
	diffusion(statelist, edgelist, presence, presence_weight,inistate,t,state_of_nodes,graph_desc_file,graph_oriented,community,comm_file_desc,t_old)
	write_trace(state_of_nodes,t,res)
	update(inistate,state_of_nodes)
	t_old = t
	t += timestep
print(state_of_nodes)
