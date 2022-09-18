from gurobipy import *
import networkx as nx
import gurobipy as gp

def solve_model(model, trucks, graph, nodes_coords, f, matrix_time, time_limit=10):

    try:
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('---- Finding optimal in solution in the time limit: ', time_limit)
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        model.setParam('TimeLimit',time_limit)

        model.optimize()
        visited_edges = [a for a in f if f[a].x==1]


        graph_out = nx.DiGraph()
        for i in range(len(nodes_coords)):
            graph_out.add_node(i+1, coords=nodes_coords[i])

        for i in range(len(matrix_time)):
            for j in range(len(matrix_time[i])):
                if matrix_time[i][j] != 0:
                    graph_out.add_edge(i+1, j+1, trucks = [])
        for edge in visited_edges:
            graph_out[edge[1]][edge[2]]['trucks'] = graph_out[edge[1]][edge[2]]['trucks'] + [edge[0]]


        return graph_out, graph
    except:
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('No solution found in this time limit, looking for the first feasible solution')
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        model.setParam('TimeLimit',10**23)
        model.setParam('SolutionLimit',1)

        model.optimize()
        visited_edges = [a for a in f if f[a].x==1]


        graph_out = nx.DiGraph()
        for i in range(len(nodes_coords)):
            graph_out.add_node(i+1, coords=nodes_coords[i])

        for i in range(len(matrix_time)):
            for j in range(len(matrix_time[i])):
                if matrix_time[i][j] != 0:
                    graph_out.add_edge(i+1, j+1, trucks = [])
        for edge in visited_edges:
            graph_out[edge[1]][edge[2]]['trucks'] = graph_out[edge[1]][edge[2]]['trucks'] + [edge[0]]


        return graph_out, graph