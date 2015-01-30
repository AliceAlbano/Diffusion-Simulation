import matplotlib.pyplot as plt
from matplotlib import rc

#Plot a curve representing the number of nodes in each state over time
def plot_curve_nb_nodes(time_list,nb_nodes_state,state_list,file_res,nb_node_max) :
	plt.clf()
	rc('axes', labelsize=20,titlesize=20)
	for state in state_list :
		plt.plot(time_list, nb_nodes_state[state],linewidth =4,label=state)
	figsize = (20,20)

	plt.ylabel("Number of nodes")
	plt.ylim(ymax = nb_node_max + 1 )
	plt.xlim(xmax = time_list[-1] + 1)
	plt.xlabel("Time")
	plt.legend(loc='upper left')
	plt.title("Number of nodes in each state")
	plt.savefig("nodes_states_" + file_res)

#Plot a curve representing the percentage of nodes in each state over time
def plot_curve_percentage_nodes(time_list,nb_nodes_state,list_nb_total_nodes,state_list,file_res,nb_node_max) :
	plt.clf()
	rc('axes', labelsize=20,titlesize=20)
	percentage = {}
	#Percentages calcul
	for state in state_list :
		percentage[state] = []
		j = 0
		for t in time_list :
			if list_nb_total_nodes[j] != 0 :
				percentage[state] += [100.0*(float(nb_nodes_state[state][j]) / float(list_nb_total_nodes[j]))]
			else :
				percentage[state] += [0]
			j += 1
			
	for state in state_list :
		plt.plot(time_list, percentage[state],linewidth =4,label=state)
	figsize = (20,20)

	plt.ylabel("Percentage of nodes")
	plt.xlim(xmax = time_list[-1] + 1)
	plt.xlabel("Time")
	plt.legend(loc='upper left')
	plt.title("Percentage of nodes in each state")
	plt.savefig("percentage_nodes_states_" + file_res)

#Plot a curve for each community. Each curve represents the number of nodes in each state over time.
def plot_curve_community(time_list,nb_nodes_state,state_list,file_res,id_comm,nb_node_max) :
	plt.clf()
	rc('axes', labelsize=20,titlesize=20)
	for state in state_list :
		plt.plot(time_list, nb_nodes_state[state],linewidth =4,label=state)
	figsize = (20,20)

	plt.ylabel("Number of nodes")
	plt.ylim(ymax = nb_node_max + 1 )
	plt.xlim(xmax = time_list[-1] + 1)
	plt.xlabel("Time")
	plt.legend(loc='upper left')
	plt.title("Number of nodes in each state for the community " + str(id_comm))
	plt.savefig("community_" + str(id_comm) + "_nodes_states_" + file_res)

#Plot a curve for a given state, representing the percentage of nodes in this state in each community.
def plot_curve_percentage_state(result_list,state,file_res):
	plt.clf()
	rc('axes', labelsize=20,titlesize=20)
	i = 0 
	while i < len(result_list) :
		plt.plot(result_list[i],result_list[i+1],linewidth =4,label="community " + result_list[i+2])
		i += 3
	figsize = (20,20)

	plt.ylabel("Percentage of nodes")
	plt.xlabel("Time")
	plt.legend(loc='upper right')
	plt.title("Percentage of nodes in the state " + str(state) + " for each community ")
	plt.savefig("percentage_state_" + str(state) + "_in_each_comm_" + file_res)
