import gurobipy as gp

def create_decision_variables(trucks, graph):
    #initiliase the model
    model = gp.Model()
    
    #Define the decision variables with the saming naming as in the mathematical model
    f = dict()
    for edge in graph.edges:
        f.update(model.addVars(trucks, [edge[0]], [edge[1]], vtype = gp.GRB.BINARY))

    q = dict()
    for edge in graph.edges:
        q.update(model.addVars(trucks, trucks,[edge[0]], [edge[1]], vtype = gp.GRB.BINARY))

    e = dict()
    for edge in graph.edges:
        e.update(model.addVars(trucks,[edge[0]], [edge[1]], vtype = gp.GRB.CONTINUOUS))
    w = model.addVars(trucks, list(graph.nodes), vtype = gp.GRB.CONTINUOUS)
    model.update()
    return model, f, q, e, w
