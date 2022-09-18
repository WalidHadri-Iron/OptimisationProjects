import gurobipy as gp
    
    
def set_constraints(model, f, q, e, w, M, trucks, graph, nbr_trucks, info_trucks, Q=5):
    #For each constraint refer to the mathematical model
    #Constraint 1
    for truck in trucks:
        origin_node = info_trucks[truck]['Origin Node']
        destination_node = info_trucks[truck]['Destination Node']
        #Make sure that the origin and destination node are different
        if origin_node != destination_node:
            children = [n for n in graph.neighbors(origin_node)]
            parents = [n for n in graph.predecessors(destination_node) if n!=origin_node]
            #Consrtaints to make sure that the truck leaves the origin node and arrives to the destination node and the inflow and the outflow for destination and origin node respectively is 0
            model.addConstr(gp.quicksum(f[truck,origin_node,child] for child in children) == 1)
            model.addConstr(gp.quicksum(f[truck,parent,origin_node] for parent in [n for n in graph.predecessors(origin_node)]) == 0)
            model.addConstr(gp.quicksum(f[truck,parent,destination_node] for parent in parents) == 1)
            model.addConstr(gp.quicksum(f[truck,destination_node,child] for child in [n for n in graph.neighbors(destination_node)]) == 0)
            #Constraints for internal nodes
            for node in graph.nodes:
                if node != origin_node and node != destination_node:
                    children = [n for n in graph.neighbors(node)]
                    parents = [n for n in graph.predecessors(node)]
                    model.addConstr(gp.quicksum(f[truck,node,child] for child in children) == gp.quicksum(f[truck,parent,node] for parent in parents))
    #Constraint to make sure that the truck takes only one way on an edge
    for edge in graph.edges:
        if (edge[1],edge[0]) in graph.edges:
            model.addConstrs(f[truck,edge[0],edge[1]] + f[truck, edge[1], edge[0]] <= 1 for truck in trucks)
    #Constraint 2
    for edge in graph.edges:
        model.addConstrs(-M*(1-q[truck1,truck2, edge[0], edge[1]]) <= e[truck1, edge[0], edge[1]] - e[truck2, edge[0] ,edge[1]] for truck1 in trucks for truck2 in trucks)
        model.addConstrs(e[truck1, edge[0], edge[1]] - e[truck2, edge[0] ,edge[1]] <= M*(1-q[truck1,truck2, edge[0], edge[1]]) for truck1 in trucks for truck2 in trucks)

    # #Constraint 3
    for edge in graph.edges:
        for i in range(nbr_trucks-1):
            for j in range(i, nbr_trucks):
                model.addConstr(q[trucks[i],trucks[j], edge[0], edge[1]] == 0)
        model.addConstrs(gp.quicksum(q[truck1,truck2, edge[0], edge[1]] for truck1 in trucks) <= 1 for truck2 in trucks)

    #Constraint 4
    for edge in graph.edges:
        model.addConstrs(gp.quicksum(q[truck1,truck2, edge[0], edge[1]] for truck1 in trucks) <= (Q-1)*(1-gp.quicksum(q[truck2,truck1, edge[0], edge[1]] for truck1 in trucks)) for truck2 in trucks)

    #Constraint 5
    for edge in graph.edges:
        model.addConstrs(2*q[truck1, truck2, edge[0], edge[1]] <= f[truck1, edge[0], edge[1]] + f[truck2, edge[0], edge[1]] for truck1 in trucks for truck2 in trucks)

    #Constraint 6
    for truck in trucks:
        origin_node = info_trucks[truck]['Origin Node']
        origin_time = info_trucks[truck]['Origin Time']
        children = [n for n in graph.neighbors(origin_node)]
        model.addConstrs(-M*(1-f[truck, origin_node, child]) <= e[truck, origin_node, child] - origin_time - w[truck, origin_node] for child in children)
        model.addConstrs(e[truck, origin_node, child] - origin_time - w[truck, origin_node] <= M*(1-f[truck, origin_node, child]) for child in children)

    #Constraint 7
    for truck in trucks:
        destination_node = info_trucks[truck]['Destination Node']
        destination_time = info_trucks[truck]['Destination Time']
        parents = [n for n in graph.predecessors(destination_node)]
        model.addConstrs(-M*(1-f[truck, parent, destination_node]) <= destination_time - e[truck, parent, destination_node] - w[truck, destination_node] - graph.get_edge_data(parent,destination_node)['time']*f[truck, parent, destination_node] for parent in parents)
        model.addConstrs(destination_time - e[truck, parent, destination_node] - w[truck, destination_node] - graph.get_edge_data(parent,destination_node)['time']*f[truck, parent, destination_node] <= M*(1-f[truck, parent, destination_node]) for parent in parents)

    #Constraint 8
    for truck in trucks:
        origin_node = info_trucks[truck]['Origin Node']
        destination_node = info_trucks[truck]['Destination Node']
        for node_i in graph.nodes:
            if node_i != origin_node and node_i != destination_node:
                children = [n for n in graph.neighbors(node_i) if n!=origin_node and n!=destination_node]
                for node_j in children:
                    second_children = [n for n in graph.neighbors(node_j)]
                    for node_k in second_children:
                        model.addConstr(-M*(2-f[truck, node_i, node_j]-f[truck,node_j,node_k]) <= e[truck, node_j, node_k] - e[truck, node_i, node_j] - w[truck, node_j] - graph.get_edge_data(node_i, node_j)['time']*f[truck, node_i, node_j])
                        model.addConstr(e[truck, node_j, node_k] - e[truck, node_i, node_j] - w[truck, node_j] - graph.get_edge_data(node_i, node_j)['time']*f[truck, node_i, node_j] <= M*(2-f[truck, node_i, node_j]-f[truck,node_j,node_k]))

    # Constraint 9
    for edge in graph.edges:
        model.addConstrs(e[truck, edge[0], edge[1]] <= M*f[truck, edge[0], edge[1]] for truck in trucks)

    #Constraint 10
    for node in graph.nodes:
        children = [n for n in graph.neighbors(node)]
        parents = [n for n in graph.predecessors(node)]
        model.addConstrs(w[truck, node] <= M*(gp.quicksum(f[truck, node, child] for child in children) + gp.quicksum(f[truck, parent, node] for parent in parents)) for truck in trucks)

    model.update()
    
    return model
