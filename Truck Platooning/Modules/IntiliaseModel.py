import networkx as nx
import numpy as np
import random


def initiliase_model(nbr_trucks, nbr_nodes):
    trucks = list(range(1,nbr_trucks+1))

    nodes_coords = np.random.randint(-20,20,(nbr_nodes,2)).tolist()

    # Defining the graph
    graph = nx.DiGraph()
    #Adding nodes to the graph
    for i in range(len(nodes_coords)):
        graph.add_node(i+1, coords=nodes_coords[i])
    #Initiliase the time and cost matrix randomnly
    matrix_time = np.random.randint(1,20,(nbr_nodes,nbr_nodes))
    matrix_cost = np.random.randint(1,50,(nbr_nodes,nbr_nodes))
    #Set the diagonals to 0, so that the cost to travel from i to i (same node) is 0 for time and cost
    np.fill_diagonal(matrix_time, 0)
    np.fill_diagonal(matrix_cost, 0)
    #Randomly set the cost for time and cost between two nodes to 0, this is made to make the graph less linked so it would look more like a real ways network
    for i in range(nbr_nodes):
        set_to_zero = random.sample(list(range(nbr_nodes)), nbr_nodes//3)
        for j in set_to_zero:
            matrix_time[i,j] = 0
            matrix_cost[i,j] = 0
    #Define on the graph for each edge the corresponding cost and time
    for i in range(len(matrix_time)):
        for j in range(len(matrix_time[i])):
            if matrix_time[i][j] != 0:
                graph.add_edge(i+1, j+1, time=matrix_time[i][j], cost=matrix_cost[i][j])
    
    #Set random origin and destination nodes for trucks
    origin_nodes = [random.randint(1,nbr_nodes) for i in range(nbr_trucks)]
    origin_time = [random.randint(1,5) for i in range(nbr_trucks)]
    destination_nodes = []
    destination_time = []
    for i in range(nbr_trucks):
        #For each truck make sure that from the origin node we can reach the destination node so that the problem could be feasible
        origin_node = origin_nodes[i]
        reachable_nodes = [node for node in list(nx.descendants(graph, 1)) if node != origin_node]
        destination_node = random.choice(reachable_nodes)
        destination_nodes.append(destination_node)
        path = nx.shortest_path(graph, origin_node, destination_node, weight="time")
        time_cost = 0
        #Keep track of the time cost to reach the destination node from the origin node so that the destination time that we set randomly would be more that the required time
        for i in range(len(path)-1):
            time_cost += graph.get_edge_data(path[i], path[i+1])['time']
        destination_time.append(random.randint(time_cost + 7, 100))

    #Store all the information related to the trucks in one dictionary
    info_trucks = dict()
    for i in range(nbr_trucks):
        info_trucks[trucks[i]] = {"Origin Node": origin_nodes[i], "Destination Node":destination_nodes[i], "Origin Time": origin_time[i],"Destination Time": destination_time[i]}

    M = max([info_trucks[x]['Destination Time'] for x in info_trucks]) - max([info_trucks[x]['Origin Time'] for x in info_trucks])
    
    return nbr_trucks, trucks, nbr_nodes, nodes_coords, graph, matrix_time, matrix_cost, info_trucks, M
