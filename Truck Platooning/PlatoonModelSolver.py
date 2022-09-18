from Modules.IntiliaseModel import *
from Modules.DecisionVariables import *
from Modules.Constrainsts import *
from Modules.ObjectiveFunction import *
from Modules.SolveModel import *
from Modules.PlottingModelSolution import *

#Initiliase the model, by generating the graph, the truck list, the nodes and the matrices for time cost and fuel cost 
nbr_trucks, trucks, nbr_nodes, nodes_coords, graph, matrix_time, matrix_cost, info_trucks, M = initiliase_model(25, 40)

#Create the decision variables and the model in gurobi
model, f, q, e, w = create_decision_variables(trucks, graph)

#Setting the objective function
model = set_objective_function(model, f, q, w, trucks, graph, saving_factor=1, transit_delay_factor=1)

#Setting the constraints
model = set_constraints(model, f, q, e, w, M, trucks, graph, nbr_trucks, info_trucks, Q=5)

#solve the model
graph_out, graph = solve_model(model, trucks, graph, nodes_coords, f, matrix_time, time_limit=20)

# Plotting the solution
plotting_graph_out(graph_out, graph, name_file="SolutionGraph.png")


### For Solving many problems

# couples = [(5,3), (4,5)]
# i = 0
# for couple in couples:
#     nbr_trucks, trucks, nbr_nodes, nodes_coords, graph, matrix_time, matrix_cost, info_trucks, M = initiliase_model(couple[0], couple[1])
#     model, f, q, e, w = create_decision_variables(trucks, graph)
#     model = set_objective_function(model, f, q, w, trucks, graph, saving_factor=1, transit_delay_factor=1)
#     model = set_constraints(model, f, q, e, w, M, trucks, graph, nbr_trucks, info_trucks, Q=5)
#     graph_out, graph = solve_model(model, trucks, graph, nodes_coords, f, matrix_time, time_limit=10)
#     plotting_graph_out(graph_out, graph, f'model_{i}.png')
#     plt.clf()
#     i+=1