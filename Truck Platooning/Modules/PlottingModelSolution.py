import networkx as nx
import matplotlib.pyplot as plt
import pylab

def plotting_graph_out(graph_out, graph, name_file="SolutionGraph.png"):
    if graph_out == -1:
        return
    plt.figure(3,figsize=(25,12)) 
    nx.draw_networkx(graph_out,pos=nx.get_node_attributes(graph_out,'coords'),node_size=1500, width=2)
    nx.draw_networkx_edge_labels(graph, pos=nx.get_node_attributes(graph_out,'coords'), edge_labels = nx.get_edge_attributes(graph_out,'trucks'), font_size=10, label_pos=0.3)
    pylab.savefig(name_file)
    