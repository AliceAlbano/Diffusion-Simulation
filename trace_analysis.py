import sys
from parser import nb_states
from parser import read_community
from plots import *

#Arguments gestion
if len(sys.argv) != 3 and len(sys.argv) != 4 : 
	print("This programm needs the trace of the diffusion and the model file (in this order), and optionnally the file containing the communities")
	sys.exit()

file_trace = sys.argv[1]
xml_file = sys.argv[2]
if len(sys.argv) == 4 :
	file_comm = sys.argv[3]
nbstates = nb_states(xml_file)

file_res = xml_file.split(".")[0] + ".png"

#Format the data to obtain one list for the time, and one list for each state (number of nodes). t_end is the last timestep in the trace, nb_node contains for each time, and for each state, the number of nodes in this state at this time. state_list contains the list of the states in the diffusion model
#Returns the nb_nodes_state structure which can be used to plot the curve of the number of nodes in each state over time
def format_nb_nodes_state(t_end, nb_node, state_list):
	t = 0
	time = []
	nb_nodes_state = {}
	while t <= t_end :
		if t in nb_node :
			time += [t]
			for state in state_list :
				if state in nb_node[t] :
					if state in nb_nodes_state :
						nb_nodes_state[state] += [nb_node[t][state]]
					else :
						nb_nodes_state[state] = [nb_node[t][state]]
				else :
					if state in nb_nodes_state :
						nb_nodes_state[state] += [0]
					else: 
						nb_nodes_state[state] = [0]

		t += 1

	return nb_nodes_state

#Plot the curve representing the number of nodes in each state as a function of time. file_trace is the file containing the diffusion trace, nb_states is an int equal to the number of states in the diffusion model, and file_res is the file name for the plot.
#Also plot the percentage of nodes in each state as a function of time.
def nb_nodes_in_state(file_trace,nb_states,file_res):
	f_trace = open(file_trace,'r')
	state_list =[]
	time = []
	nb_node = {}
	nb_node_max = 0
	list_nb_total_nodes = []
	#Read the results file, and extract the information to plot the curve
	line = f_trace.readline()
	while line != "" :
		l = line.split(" ")
		if len(l) > 1 :
			#If the current line in the trace indicates the time, updates the time list
			if l[0] == "time" :
				t = int(l[1])
				t_end = t
				time += [t]
				if t not in nb_node :
					nb_node[t] = {}
				if len(time) > 1 :
					list_nb_total_nodes += [nb_total_nodes]
				else :
					list_nb_total_nodes += [0]
				nb_total_nodes = 0

			#If the current line in the trace indicates the state, updates the state list
			elif l[0] == "state" :
				state = l[1][:-1]
				if state not in state_list :
					state_list += [state]
				if state not in nb_node[t] :
					nb_node[t][state] = 0
			else :
				print("bad syntax file")

		#If the current line in the trace indicates a node, updates the nb_node dictionnary according to current time and state of the node
		elif len(l) == 1 :
			nb_node[t][state] += 1
			#nb_node_max is used for the plot in order to have a decent scale
			if int(l[0]) > nb_node_max:
				nb_node_max = int(l[0])
			nb_total_nodes += 1
			if len(time) == 1 :
				list_nb_total_nodes[0] = nb_total_nodes
		else :
			print("bad syntax")
		line = f_trace.readline()

	nb_nodes_state = format_nb_nodes_state(t_end, nb_node, state_list)

	# plot the curve	
	plot_curve_nb_nodes(time,nb_nodes_state,state_list,file_res,nb_node_max)
	plot_curve_percentage_nodes(time,nb_nodes_state,list_nb_total_nodes,state_list,file_res,nb_node_max)
	
	f_trace.close()


#Format the data to obtain one list for the time, and one list for each state (number of nodes), for a given community. comm contains the data, state_list contains the list of the states in the diffusion model, and id_comm is the identifiant of the community.
#Returns the result_list which has two elements : first is the time list, and second is the nb_nodes_state structure. These can be used to plot the curve of the number of nodes in each state over time for a given community
def format_nb_nodes_state_community(comm,state_list,id_comm) :
	nb_nodes_state = {}
	time_list = []
	for t in sorted(comm[id_comm].keys()) :
		time_list += [t]
		for state in state_list :
			if state in nb_nodes_state :
				if state in comm[id_comm][t] :
					nb_nodes_state[state] += [comm[id_comm][t][state]]
				else :
					nb_nodes_state[state] += [0]
			else :
				if state in comm[id_comm][t] :
					nb_nodes_state[state] = [comm[id_comm][t][state]]
				else :
					nb_nodes_state[state] = [0]
	result_list = [time_list,nb_nodes_state]
	return result_list

#Plot the curves riepresenting the number of nodes in each state for each community as a function of time. file_trace is the file containing the diffusion trace,  nb_states is an int equal to the number of states in the diffusion model, file_comm is the file containing the communities, and file_res is the name for the curve file.
def nb_nodes_in_community(file_trace,nb_states,file_comm,file_res):

	f_trace = open(file_trace,'r')
	f_comm = open(file_comm,'r')
	state_list =[]
	t_old = 0
	time = []
	nb_node_max = 0
	#Read the results file timestep by timestep. For each timestep, read the community file
	line = f_trace.readline()
	community = {}
	comm = {}
	while line != "" :
		l = line.split(" ")
		if len(l) > 1 :
			if l[0] == "time" :
			#If the current line in the trace indicates the time, updates the community structure by reading the community file
				t = int(l[1])
				t_end = t
				time += [t]
				read_community(f_comm,community,t,t,t_old)
				t_old = t
				for id_comm in community[t] :
					if id_comm not in comm :
						comm[id_comm] = {}
					if t not in comm[id_comm] :
						comm[id_comm][t] = {}

			elif l[0] == "state" :
			#If the current line in the trace indicates the state, updates the state list
				state = l[1][:-1]
				if state not in state_list :
					state_list += [state]
				for id_comm in community[t] :
					for state_tmp in state_list :
						if state_tmp not in comm[id_comm][t] :
							comm[id_comm][t][state_tmp] = 0

			else :
				print("bad syntax file")
		elif len(l) == 1 :
		#If the current lines indicates a node, updates the comm dictionnary with the state of the node and its community at the current time
			n = int(l[0])
			for id_comm in community[t] :
				#search for the community of the node
				if n in community[t][id_comm] :
					if id_comm not in comm :
						comm[id_comm] = {}
					if t not in comm[id_comm] :
						comm[id_comm][t] = {}
					for state_tmp in state_list :
						if state_tmp not in comm[id_comm][t] :
							comm[id_comm][t][state_tmp] = 0
					comm[id_comm][t][state] += 1
					break;
			if int(l[0]) > nb_node_max:
				nb_node_max = int(l[0])
		else :
			print("bad syntax")
		line = f_trace.readline()


	for id_comm in comm :
		result_list = format_nb_nodes_state_community(comm,state_list,id_comm)
		plot_curve_community(result_list[0],result_list[1],state_list,file_res,id_comm,nb_node_max)

	f_comm.close()
	f_trace.close()

#Returns a dictionnary containing, for each time, and for each community, the total number of node at this time in this community.
def total_nodes_in_community(file_comm):
	nb_nodes_in_comm = {}
	line = file_comm.readline()
	while line != "":
		l = line.split(" ")
		id_comm = int(l[0])
		n = int(l[1])
		begin = int(l[2])
		end = int(l[3])
		
		t = begin
		while t <= end :
		
			if t not in nb_nodes_in_comm :
				nb_nodes_in_comm[t] = {}

			if id_comm not in nb_nodes_in_comm[t] :
				nb_nodes_in_comm[t][id_comm] = 0

			nb_nodes_in_comm[t][id_comm] += 1
			t += 1

		line = file_comm.readline()

	return nb_nodes_in_comm

#Format the data to obtain one list for the time, and one list for each state (percentage of nodes), for a given community. comm contains the data, state_list contains the list of the states in the diffusion model, and id_comm is the identifiant of the community.
#Returns the result_list which has several elements : first is the time list, and then for a given staten, the percentage of nodes in this state in the given community. These can be used to plot the curve of the percentage of nodes in a given state over time for all communities.
def format_percentage_nodes_state_community(comm,state,nb_nodes_in_comm) :
	nb_nodes= {}
	time_list = {}
	for id_comm in comm :
		if id_comm not in time_list : 
			time_list[id_comm] = []
		for t in sorted(comm[id_comm].keys()) :
			time_list[id_comm] += [t]

			if id_comm not in nb_nodes :
				nb_nodes[id_comm] = []
			if state not in comm[id_comm][t] :
				nb_nodes[id_comm] += [0]
			else :
				if t not in nb_nodes_in_comm :
					nb_nodes[id_comm] += [0]
				else :
					if id_comm not in nb_nodes_in_comm[t] :
						nb_nodes[id_comm] += [0]
					else :
						if nb_nodes_in_comm[t][id_comm] != 0 :
							nb_nodes[id_comm] += [float(comm[id_comm][t][state])*100.0 / float(nb_nodes_in_comm[t][id_comm])]
						else :
							nb_nodes[id_comm] += [0]
	
	result_list = []
	for id_comm in nb_nodes :
		result_list += [time_list[id_comm]]
		result_list += [nb_nodes[id_comm]]
		result_list += [str(id_comm)]
	return result_list

#Plot the curves riepresenting the percentage of nodes in a state for every community as a function of time. file_trace is the file containing the diffusion trace,  nb_states is an int equal to the number of states in the diffusion model, file_comm is the file containing the communities, and file_res is the name for the curve file.
#For each state, plot a curve representing the percentage of nodes in this state in each community as a function of time. file_trace is the file containing the diffusion trace,  nb_states is an int equal to the number of states in the diffusion model, file_comm is the file containing the communities, and file_res is the name for the curve file.
def percentage_nodes_in_each_community(file_trace,nb_states,file_comm,file_res):

	f_trace = open(file_trace,'r')
	f_comm = open(file_comm,'r')
	nb_nodes_in_comm = total_nodes_in_community(f_comm)
	f_comm.close()
	f_comm = open(file_comm,'r')

	state_list =[]
	t_old = 0
	time = []
	#Read the results file timestep by timestep. For each timestep, read the community file
	line = f_trace.readline()
	community = {}
	comm = {}
	while line != "" :
		l = line.split(" ")
		if len(l) > 1 :
			if l[0] == "time" :
			#If the current line in the trace indicates the time, updates the community structure by reading the community file
				t = int(l[1])
				t_end = t
				time += [t]
				read_community(f_comm,community,t,t,t_old)
				t_old = t
				for id_comm in community[t] :
					if id_comm not in comm :
						comm[id_comm] = {}
					if t not in comm[id_comm] :
						comm[id_comm][t] = {}

			elif l[0] == "state" :
			#If the current line in the trace indicates the state, updates the state list
				state = l[1][:-1]
				if state not in state_list :
					state_list += [state]
				for id_comm in community[t] :
					for state_tmp in state_list :
						if state_tmp not in comm[id_comm][t] :
							comm[id_comm][t][state_tmp] = 0

			else :
				print("bad syntax file")
		elif len(l) == 1 :
		#If the current lines indicates a node, updates the comm dictionnary with the state of the node and its community at the current time
			n = int(l[0])
			for id_comm in community[t] :
				#search for the community of the node
				if n in community[t][id_comm] :
					if id_comm not in comm :
						comm[id_comm] = {}
					if t not in comm[id_comm] :
						comm[id_comm][t] = {}
					for state_tmp in state_list :
						if state_tmp not in comm[id_comm][t] :
							comm[id_comm][t][state_tmp] = 0
					comm[id_comm][t][state] += 1
					break;
		else :
			print("bad syntax")
		line = f_trace.readline()


	for state in state_list :
		result_list = format_percentage_nodes_state_community(comm,state,nb_nodes_in_comm)
		plot_curve_percentage_state(result_list,state,file_res)

	f_comm.close()
	f_trace.close()

nb_nodes_in_state(file_trace,nb_states,file_res)
if len(sys.argv) == 4 :
	nb_nodes_in_community(file_trace,nb_states,file_comm,file_res)
	percentage_nodes_in_each_community(file_trace,nb_states,file_comm,file_res)

