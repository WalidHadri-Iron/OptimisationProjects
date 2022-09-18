import gurobipy as gp

def set_objective_function(model, f, q, w, trucks, graph, saving_factor=1, transit_delay_factor=1):
    #Define the related costs, refer to the mathematical model
    fuel_cost = gp.quicksum(graph.get_edge_data(edge[0],edge[1])['cost']*f[truck,edge[0],edge[1]] for edge in graph.edges for truck in trucks)
    platoon_benefit =gp.quicksum(graph.get_edge_data(edge[0],edge[1])['cost']*q[truck1, truck2,edge[0],edge[1]] for edge in graph.edges for truck1 in trucks for truck2 in trucks)
    delay_cost =gp.quicksum(w)

    objective_function = fuel_cost - saving_factor*platoon_benefit + transit_delay_factor*delay_cost
    model.setObjective(objective_function, gp.GRB.MINIMIZE)
    model.update()
    return model
