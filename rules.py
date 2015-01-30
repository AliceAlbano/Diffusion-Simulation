import random

#Search all neighbors present at time t of a node n
def neigh(n,t,presence,graph_oriented):
	neighborhood = set([])
	if t in presence :
		for link in presence[t][1] :
			if link[0] == n and graph_oriented == "no" :
				neighborhood.add(link[1])
			if link[1] == n :
				neighborhood.add(link[0])
	return neighborhood

#Search all neighbors present at time t of a node n for a weighted graph
def neigh_weight(n,t,presence_weight,graph_oriented):
	neighborhood = set([])
	if t in presence_weight :
		for link in presence_weight[t][1] :
			if link[0] == n and graph_oriented == "no" :
				neighborhood.add((link[1],link[2]))
			if link[1] == n :
				neighborhood.add((link[0],link[2]))
	return neighborhood

# For a given probability returns 1 if the test success (node is contaminated), and 0 otherwise
def contamination_test(proba) :
	a = random.random()
	if a > proba :
		return 0
	else :
		return 1

#Change of states when the transition is dependant of neighborhood and is modelised by a probability. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the probability of a change of state, and state_of_nodes and inistate contain the states of each node
def change_neigh_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
			if inistate[n] == state1 :
				neighbors = neigh(n,time,presence,graph_oriented)
				for v in neighbors :
#					print(v,inistate[v])
					if inistate[v] == state2 :
#						print("neigh, conta test",n,v)
						a = contamination_test(tr_value)
						if a == 1 :
							if n in state_of_nodes[state1] :
								state_of_nodes[state1].remove(n)
							if state2 in state_of_nodes :
								state_of_nodes[state2].add(n)
							else :
								state_of_nodes[state2] = set([n])

def change_neigh_proba_weight(presence_weight, time, state1, state2, state_of_nodes,inistate,graph_oriented) :
	#for each node present at t = time
	if time in presence_weight :
		for n in presence_weight[time][0] :
			if inistate[n] == state1 :
#				print("aaaa")
				neighbors = neigh_weight(n,time,presence_weight,graph_oriented)
				for v in neighbors :
#					print(v,inistate[v])
					if inistate[v[0]] == state2 :
#						print("neigh, conta test")
						a = contamination_test(v[1])
						if a == 1 :
							if n in state_of_nodes[state1] :
								state_of_nodes[state1].remove(n)
							if state2 in state_of_nodes :
								state_of_nodes[state2].add(n)
							else :
								state_of_nodes[state2] = set([n])

#Change of states when the transition is dependant of neighborhood and is modelised by a percentage. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the percentage of neighbors in state2 for changing state, and state_of_nodes and inistate contain the states of each node
def change_neigh_percentage(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
#			print("inside change_neigh_percentage, n = ",n)
			if inistate[n] == state1 :
				neighbors = neigh(n,time,presence,graph_oriented)
				nb_neighbors = len(neighbors)
				nb_neighbors_state2 = 0
				for v in neighbors :
					if inistate[v] == state2 :
						nb_neighbors_state2 += 1
				if float(nb_neighbors_state2)*100.0 / float(nb_neighbors) >= tr_value :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

def change_neigh_percentage_weight(presence_weight, time, state1, state2, state_of_nodes,inistate,graph_oriented) :
	#for each node present at t = time
	if time in presence_weight :
		for n in presence_weight[time][0] :
			if inistate[n] == state1 :
				neighbors = neigh_weight(n,time,presence_weight,graph_oriented)
				nb_neighbors = len(neighbors)
				nb_neighbors_state2 = 0
				threshold = 0
				for v in neighbors :
					if inistate[v[0]] == state2 :
						threshold = v[1]
						nb_neighbors_state2 += 1
				if float(nb_neighbors_state2)*100.0 / float(nb_neighbors) >= threshold :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

#Change of states when the transition is dependant of neighborhood and is modelised by a number of infected neighbors. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the number of neighbors in state2 required for changing state, and state_of_nodes and inistate contain the states of each node
def change_neigh_number(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented) :
	if time in presence :
		#for each node present at t = time
		for n in presence[time][0] :
			if inistate[n] == state1 :
				neighbors = neigh(n,time,presence,graph_oriented)
				nb_neighbors_state2 = 0
				for v in neighbors :
					if inistate[v] == state2 :
						nb_neighbors_state2 += 1
				if nb_neighbors_state2 >= tr_value :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

#Change of states when the transition isn't dependant of the graph and is modelised by a probability.
def change_none_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
			if inistate[n] == state1 :
				a = contamination_test(tr_value)
				if a == 1 :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

#Change of states when the transition is dependant of community and is modelised by a percentage. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the percentage of neighbors in state2 for changing state, and state_of_nodes and inistate contain the states of each node. Community contains the list of nodes for each community at time t, and comm_file_desc is a file descriptor on the community file.
def change_comm_percentage(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
			if inistate[n] == state1 :
				comm_id_n = None
				if time in community :
					for comm_id in community[time] :
						if n in community[time][comm_id] :
							comm_id_n = comm_id
							break;
					if comm_id_n == None :
						neighbors = set([])
					else :
						neighbors_in_community = community[time][comm_id_n]
						neighbors_present = set([])
						for node in neighbors_in_community :
							if node in presence[time][0] and node != n:
								neighbors_present.add(node)
						neighbors = neighbors_in_community.intersection(neighbors_present)
				else :
					neighbors = set([])
				nb_neighbors = len(neighbors)
				nb_neighbors_state2 = 0
				for v in neighbors :
					if inistate[v] == state2 :
						nb_neighbors_state2 += 1
				if nb_neighbors > 0 and float(nb_neighbors_state2)*100.0 / float(nb_neighbors) >= tr_value :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

#Change of states when the transition is dependant of community and is modelised by a probability. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the probability of a change of state, and state_of_nodes and inistate contain the states of each node
def change_comm_proba(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
			if inistate[n] == state1 :
				comm_id_n = None
				if time in community :
					for comm_id in community[time] :
						if n in community[time][comm_id] :
							comm_id_n = comm_id
							break;
					if comm_id_n == None :
						neighbors = set([])
					else :
						neighbors_in_community = community[time][comm_id_n]
						neighbors_present = set([])
						for node in neighbors_in_community :
							if node in presence[time][0] and node != n:
								neighbors_present.add(node)
						neighbors = neighbors_in_community.intersection(neighbors_present)
				else :
					neighbors = set([])
				for v in neighbors :
					if inistate[v] == state2 :
						a = contamination_test(tr_value)
						if a == 1 :
							if n in state_of_nodes[state1] :
								state_of_nodes[state1].remove(n)
							if state2 in state_of_nodes :
								state_of_nodes[state2].add(n)
							else :
								state_of_nodes[state2] = set([n])


#Change of states when the transition is dependant of community and is modelised by a number. presence contains the list of nodes and links present at each time step, state1 is the original state, state2 is the target state, tr_value is the percentage of neighbors in state2 for changing state, and state_of_nodes and inistate contain the states of each node. Community contains the list of nodes for each community at time t, and comm_file_desc is a file descriptor on the community file.
def change_comm_number(presence, time, state1, state2, tr_value, state_of_nodes,inistate,graph_oriented,community,comm_file_desc) :
	#for each node present at t = time
	if time in presence :
		for n in presence[time][0] :
			if inistate[n] == state1 :
				comm_id_n = None
				if time in community :
					for comm_id in community[time] :
						if n in community[time][comm_id] :
							comm_id_n = comm_id
							break;
					if comm_id_n == None :
						neighbors = set([])
					else :
						neighbors_in_community = community[time][comm_id_n]
						neighbors_present = set([])
						for node in neighbors_in_community :
							if node in presence[time][0] and node != n:
								neighbors_present.add(node)
						neighbors = neighbors_in_community.intersection(neighbors_present)
				else :
					neighbors = set([])
				nb_neighbors = len(neighbors)
				nb_neighbors_state2 = 0
				for v in neighbors :
					if inistate[v] == state2 :
						nb_neighbors_state2 += 1
				if nb_neighbors_state2 >= tr_value :
					if n in state_of_nodes[state1] :
						state_of_nodes[state1].remove(n)
					if state2 in state_of_nodes :
						state_of_nodes[state2].add(n)
					else :
						state_of_nodes[state2] = set([n])

