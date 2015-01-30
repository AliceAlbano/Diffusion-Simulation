from xml.dom import minidom

#Reads the graph for nodes present at t = time. Deletes presence[time -1].
def read_graph_light(graph_desc_file,presence,presence_weight,t_end_graph,time,graph_weighted):
	if not time in presence :
		presence[time] =  [ set([]),set([]) ] 
		presence_weight[time] = [ set([]),set([])]
	line = graph_desc_file.readline()
	d = time 
	while line != "" and d == time :
		l = line.split(" ")
		n1 = int(l[0])
		n2 = int(l[1])
		d = int(l[2])
		f = int(l[3])
		if graph_weighted == "yes" :
			w = float(l[4])
		t = d
		while t <= f :
			if not t in presence :
				presence[t] =  [ set([]),set([]) ] 
				presence_weight[t] = [set([]),set([])]
			if graph_weighted == "yes" :
				presence_weight[t][0].add(n1)
				presence_weight[t][0].add(n2)
				presence_weight[t][1].add((n1,n2,w))
			else :	
				presence[t][0].add(n1)
				presence[t][0].add(n2)
				presence[t][1].add((n1,n2))
			t += 1
		if d != time :
			break;	
		line = graph_desc_file.readline()

	if (time -1) in presence :
		del presence[time - 1]
	if (time - 1) in presence_weight :
		del presence_weight[time - 1]

#Reads the graph and returns the last timestep
def read_graph(graph_file,t_end_graph):
	src = open(graph_file,'r')
	line = src.readline()
	while line != "" :
		l = line.split(" ")
		if len(l) >= 4 :
			f = int(l[3])
			
			if f > t_end_graph :
				t_end_graph = f
		line = src.readline()
	src.close()
	return t_end_graph

#Parse the xml file with the definition of the diffusion model.
def parser(xmlfile,statelist,edgelist) :
	xmldoc = minidom.parse(xmlfile)
	#First, extraction of the different states in the model
	statelist += xmldoc.getElementsByTagName('state')
	if len(statelist) == 0 :
		print("At least one state is needed for the definition of the model")
	#Second, extraction of the transition between the states
	edgelist += xmldoc.getElementsByTagName('edge')
	if len(edgelist) == 0 :
		print("At least one state is needed for the definition of the model")

#Returns the number of states of a model defined n xmlfile
def nb_states(xmlfile) :
	xmldoc = minidom.parse(xmlfile)
	statelist = xmldoc.getElementsByTagName('state')
	return len(statelist)

#Read the file containing the initial states of each node for the diffusion process and fills the inistate dictionnary and the state_of_nodes_dictionnary
def initial_states(file_ini_states,inistate,state_of_nodes):
	src = open(file_ini_states,'r')
	line = src.readline()
	while line != "" :
		l = line.split(" ")
		n = int(l[0])
		state = l[1][:-1]
		inistate[n] = state
		if state in state_of_nodes :
			state_of_nodes[state].add(n)
		else :
			state_of_nodes[state] = set([])
			state_of_nodes[state].add(n)
		line = src.readline()

#Reads the communities for the graph for nodes present at t = time. Deletes community[time -1].
def read_community(comm_file_desc,community,t_end_graph,time,t_old):
	if not time in community :
		community[time] =  {}
	line = comm_file_desc.readline()
	d = time 
	while line != "" :
		if  d == time :
			l = line.split(" ")
			comm_id = int(l[0])
			n1 = int(l[1])
			d = int(l[2])
			f = int(l[3])
			t = d
			while t <= f :
				if not t in community :
					community[t] =  {}
				if comm_id in community[t] :
					community[t][comm_id].add(n1)
				else :
					community[t][comm_id] = set([n1])
				t += 1
		if d > time :
			break;	
		line = comm_file_desc.readline()

	j = t_old
	while j <= time - 1 :
		if j in community :
			del community[j]
		j += 1

