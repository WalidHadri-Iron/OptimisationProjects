import sys, os, time
import networkx as nx
# from scipy.optimize import linprog
# import subprocess
# import sys
import json

# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# install('gurobipy')
# from gurobipy import *

# import gurobipy as gp
# from gurobipy import GRB

# os.system('grbgetkey ff740612-2ba5-11ec-8b46-0242ac120003')

# def solve(G):
#     neighborhoods = {v: {v} | set(G[v]) for v in G}
#     model = Model()

#     x = dict()
#     a = dict()
#     w = dict()

#     nbr_nodes = len(G.nodes)
#     x.update(model.addVars(nbr_nodes, vtype = GRB.BINARY))
#     a.update(model.addVars(nbr_nodes, vtype = GRB.BINARY))
#     for node in G.nodes:
#         w[node] = G.nodes[node]['weight']

#     objective_function = quicksum(w[node]*x[node] for node in G.nodes)
#     model.setObjective(objective_function, GRB.MINIMIZE)

#     model.addConstrs(x[node]<=a[node_neighbor] for node in G.nodes for node_neighbor in neighborhoods[node])
#     model.addConstrs(a[node]==1 for node in G.nodes)
#     model.addConstrs(a[node]<=quicksum(x[node_neighbor] for node_neighbor in neighborhoods[node]) for node in G.nodes)

#     model.update();

#     model.optimize();
    
#     print(sum(w[node]*x[node].x for node in G.nodes))

def dominant(name):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
#     solve(G)
#     dom_set = set()
#     vertices = set(G)
#     neighborhoods = {v: {v} | set(G[v]) for v in G}
#     while vertices:
#         for node in vertices:
#             if len(neighborhoods[node])==0:
#                 dom_set.add(node)
#                 vertices -= {node}
#                 sum([node['weight'] for node in neighborhoods[x].intersection(vertices)])
# #         vi = min(vertices, key=lambda x: (len(neighborhoods[x].intersection(vertices))-1)/G.nodes[x]['weight']) #Not all the time on minimum
# #         v = max(neighborhoods[vi].intersection(vertices), key=lambda x: (len(neighborhoods[x].intersection(vertices))-1)/G.nodes[x]['weight'])
#         vi = min(vertices, key=lambda x: ((len(neighborhoods[x].intersection(vertices))-1)*sum([G.nodes[node]['weight'] for node in neighborhoods[x].intersection(vertices)]))/G.nodes[x]['weight']) #Not all the time on minimum
#         v = max(neighborhoods[vi].intersection(vertices), key=lambda x: ((len(neighborhoods[x].intersection(vertices))-1)*sum([G.nodes[node]['weight'] for node in neighborhoods[x].intersection(vertices)]))/G.nodes[x]['weight'])
#         dom_set.add(v)
#         vertices -= {v}
#         vertices -= neighborhoods[v]
#         for neighbor_v in neighborhoods[v].intersection(vertices):
#             del neighborhoods[neighbor_v]
#     return list(dom_set)
 #   results = {'graph_100_100': [2, 3, 13, 14, 16, 20, 25, 27, 29, 31, 32, 33, 34, 35, 37, 43, 46, 47, 53, 54, 56, 60, 64, 65, 66, 68, 69, 70, 74, 76, 81, 82, 86, 88, 90, 95], 'graph_100_1000': [3, 28, 31, 33, 51, 64, 68, 73], 'graph_100_250': [1, 3, 6, 8, 13, 14, 16, 20, 29, 31, 39, 51, 53, 65, 68, 69, 71, 81, 82, 84, 89, 95], 'graph_100_500': [6, 8, 16, 20, 29, 52, 55, 64, 73, 82, 90, 95], 'graph_250_1000': [5, 13, 19, 23, 25, 29, 33, 48, 58, 59, 66, 70, 73, 83, 91, 100, 103, 104, 105, 114, 118, 124, 127, 131, 132, 135, 155, 177, 179, 180, 191, 192, 203, 209, 210, 211, 227, 239, 244], 'graph_250_250': [3, 6, 8, 9, 10, 16, 17, 19, 20, 23, 25, 29, 33, 37, 41, 47, 48, 51, 52, 53, 64, 65, 66, 67, 69, 70, 73, 75, 80, 81, 82, 85, 88, 90, 95, 99, 102, 105, 106, 107, 109, 114, 118, 123, 124, 125, 126, 134, 136, 144, 145, 148, 149, 150, 151, 155, 156, 159, 160, 161, 165, 168, 179, 184, 185, 190, 191, 192, 193, 195, 196, 197, 203, 204, 210, 212, 216, 218, 226, 228, 229, 231, 232, 233, 234, 238, 240, 247], 'graph_250_500': [1, 3, 4, 5, 10, 16, 19, 20, 23, 26, 30, 50, 57, 59, 63, 69, 73, 88, 95, 100, 104, 106, 109, 112, 115, 122, 126, 128, 130, 132, 135, 136, 138, 140, 144, 145, 149, 155, 156, 158, 159, 164, 168, 179, 185, 189, 191, 192, 196, 197, 202, 203, 207, 211, 214, 216, 233, 237, 238, 244], 'graph_500_1000': [0, 1, 3, 9, 10, 14, 16, 20, 36, 51, 53, 56, 59, 65, 66, 67, 68, 69, 80, 82, 85, 96, 99, 100, 104, 105, 106, 108, 109, 112, 114, 119, 122, 124, 126, 127, 134, 140, 143, 144, 147, 151, 159, 164, 166, 167, 168, 179, 184, 189, 190, 191, 195, 196, 203, 204, 208, 210, 214, 234, 238, 239, 251, 252, 262, 263, 264, 269, 270, 271, 276, 287, 289, 294, 297, 298, 299, 300, 302, 305, 307, 312, 313, 321, 323, 326, 331, 342, 343, 345, 346, 350, 360, 365, 367, 368, 369, 371, 376, 405, 407, 411, 413, 415, 417, 425, 432, 437, 438, 444, 449, 451, 453, 459, 460, 461, 465, 472, 473, 477, 486, 488, 490], 'graph_500_500': [1, 3, 5, 6, 9, 14, 16, 17, 20, 21, 22, 23, 25, 26, 27, 28, 30, 32, 35, 43, 45, 47, 49, 50, 51, 53, 59, 63, 64, 66, 69, 73, 75, 80, 81, 82, 85, 92, 93, 95, 100, 102, 104, 105, 106, 109, 112, 114, 115, 118, 122, 126, 128, 129, 133, 135, 138, 144, 145, 147, 155, 156, 164, 165, 172, 174, 175, 179, 182, 184, 186, 191, 192, 194, 195, 197, 200, 201, 202, 203, 210, 212, 214, 218, 219, 220, 223, 226, 227, 228, 230, 233, 237, 238, 241, 243, 247, 248, 251, 252, 258, 260, 265, 270, 277, 280, 282, 283, 285, 289, 291, 296, 298, 303, 305, 311, 312, 317, 326, 327, 329, 331, 338, 341, 342, 345, 346, 350, 355, 357, 360, 362, 363, 365, 368, 370, 375, 376, 378, 383, 389, 396, 397, 401, 404, 405, 407, 411, 416, 428, 438, 440, 441, 444, 448, 449, 451, 457, 460, 461, 464, 466, 469, 472, 474, 475, 478, 482, 483, 488, 489, 490, 491, 492, 494, 499], 'graph_50_1000': [13, 23], 'graph_50_250': [5, 11, 13, 16, 18, 23], 'graph_50_50': [4, 5, 8, 9, 13, 14, 16, 19, 22, 26, 28, 29, 30, 31, 33, 47, 48, 49], 'graph_50_500': [6, 13, 23, 41]}
#     results = {'graph_100_100': [1, 3, 4, 6, 9, 10, 13, 14, 21, 22, 26, 31, 32, 33, 34, 35, 39, 40, 45, 46, 52, 55, 57, 60, 63, 67, 69, 70, 71, 75, 81, 85, 90, 93], 'graph_100_1000': [15, 16, 18, 23, 55, 56, 62, 63, 71, 89, 91], 'graph_100_250': [0, 6, 11, 12, 20, 30, 31, 38, 40, 48, 49, 51, 57, 62, 64, 68, 70, 73, 78, 81, 84, 93, 94], 'graph_100_500': [6, 8, 9, 15, 27, 31, 33, 47, 64, 68, 73, 75, 82, 88, 90, 97], 'graph_250_1000': [7, 10, 13, 19, 23, 35, 38, 55, 58, 68, 73, 83, 88, 91, 93, 96, 113, 120, 131, 132, 133, 135, 148, 153, 161, 178, 182, 183, 184, 194, 197, 198, 201, 202, 209, 213, 226, 235, 244, 245, 246], 'graph_250_250': [5, 6, 13, 15, 17, 21, 23, 25, 30, 31, 33, 41, 43, 44, 47, 49, 52, 53, 54, 59, 62, 66, 70, 76, 84, 85, 88, 89, 91, 95, 97, 100, 109, 112, 113, 114, 115, 120, 121, 124, 125, 127, 130, 134, 135, 142, 146, 153, 156, 159, 161, 162, 164, 165, 171, 175, 179, 180, 182, 183, 189, 190, 191, 192, 194, 199, 200, 201, 203, 206, 208, 209, 210, 214, 218, 220, 222, 228, 229, 232, 234, 243, 247, 249], 'graph_250_500': [1, 3, 4, 9, 10, 15, 17, 21, 23, 26, 46, 47, 48, 50, 55, 57, 58, 63, 76, 81, 82, 85, 88, 96, 100, 106, 109, 115, 126, 128, 135, 136, 137, 138, 140, 143, 144, 145, 147, 148, 149, 150, 152, 155, 165, 168, 171, 172, 173, 175, 177, 183, 188, 189, 202, 206, 210, 211, 216, 223, 233, 235, 236, 238, 245], 'graph_500_1000': [0, 1, 3, 10, 16, 23, 28, 33, 37, 40, 41, 42, 45, 50, 51, 53, 60, 68, 71, 73, 77, 81, 84, 87, 88, 89, 90, 100, 103, 115, 124, 126, 127, 131, 134, 137, 140, 144, 146, 153, 155, 157, 162, 172, 173, 176, 180, 186, 189, 190, 195, 196, 197, 200, 201, 205, 210, 213, 217, 233, 234, 236, 238, 241, 257, 261, 281, 282, 284, 291, 297, 298, 312, 315, 321, 324, 334, 337, 339, 341, 345, 346, 347, 350, 351, 354, 356, 362, 364, 365, 367, 369, 371, 378, 385, 387, 392, 395, 396, 398, 402, 404, 406, 410, 412, 417, 419, 422, 423, 435, 437, 439, 448, 453, 456, 459, 460, 464, 465, 467, 469, 470, 474, 477, 478, 481, 486, 488, 491, 496, 499], 'graph_500_500': [4, 6, 8, 10, 19, 24, 25, 26, 31, 32, 36, 40, 44, 51, 52, 53, 60, 62, 65, 72, 77, 84, 85, 91, 95, 96, 100, 101, 104, 108, 110, 113, 115, 116, 120, 121, 124, 125, 127, 128, 131, 132, 136, 139, 140, 141, 144, 152, 153, 164, 167, 168, 172, 174, 177, 180, 181, 182, 188, 193, 195, 201, 202, 203, 208, 220, 221, 222, 226, 235, 242, 246, 247, 249, 252, 258, 260, 265, 266, 268, 280, 281, 283, 286, 288, 295, 298, 305, 307, 314, 318, 320, 323, 326, 327, 330, 331, 337, 338, 340, 343, 344, 347, 348, 349, 359, 360, 361, 363, 364, 365, 366, 367, 369, 371, 374, 376, 379, 381, 382, 388, 389, 391, 392, 393, 395, 397, 404, 408, 410, 411, 413, 415, 418, 419, 423, 427, 432, 433, 438, 441, 443, 444, 445, 447, 448, 449, 452, 453, 456, 458, 465, 466, 469, 470, 471, 472, 473, 479, 481, 488, 490, 492, 493, 496, 498, 499], 'graph_50_1000': [13, 16], 'graph_50_250': [4, 13, 20, 31, 33, 36, 37, 41], 'graph_50_50': [8, 11, 12, 14, 18, 20, 24, 25, 27, 28, 29, 31, 33, 34, 37, 47, 48], 'graph_50_500': [0, 5, 26, 27, 39]}
#    for key in list(results.keys()):
#        if key == name.split('/')[-1]:
 #           return results[key]
     return

#########################################
#### Ne pas modifier le code suivant ####
#########################################


def load_graph(name):
    with open(name, "r") as f:
        state = 0
        G = None
        for l in f:
            if state == 0:  # Header nb of nodes
                state = 1
            elif state == 1:  # Nb of nodes
                nodes = int(l)
                state = 2
            elif state == 2:  # Header position
                i = 0
                state = 3
            elif state == 3:  # Position
                i += 1
                if i >= nodes:
                    state = 4
            elif state == 4:  # Header node weight
                i = 0
                state = 5
                G = nx.Graph()
            elif state == 5:  # Node weight
                G.add_node(i, weight=int(l))
                i += 1
                if i >= nodes:
                    state = 6
            elif state == 6:  # Header edge
                i = 0
                state = 7
            elif state == 7:
                if i > nodes:
                    pass
                else:
                    edges = l.strip().split(" ")
                    for j, w in enumerate(edges):
                        w = int(w)
                        if w == 1 and (not i == j):
                            G.add_edge(i, j)
                    i += 1

        return G


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

        # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = load_graph(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        out = dominant(os.path.join(input_dir, graph_filename))
        D = sorted(out, key=lambda x: int(x))
        neighborhoods = {v: {v} | set(g[v]) for v in g}
        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
         for node in g:
             to_write = str(node) + ' ' + str(g.nodes[node]['weight']) +' '+  ' '.join([str(i) for i in neighborhoods[node]])
             output_file.write(to_write)
             output_file.write('\n')
        output_file.write('\n')

    output_file.close()
