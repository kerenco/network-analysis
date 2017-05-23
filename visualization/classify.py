import math
import networkx as nx
import matplotlib.pyplot as plt

#links - string of 0s(the edge does not exist) and 1s(the edge exists)
#links does not include self edges(the length for graph with 3 nodes is 6)
#isDirected - True if the graph is directed, False if it is not
def classify(links, isDirected, fileName):
    size = int(math.ceil(math.sqrt(len(links))))
    matrix = [[0 for x in range(size)] for y in range(size)]
    k = 0
    G = nx.DiGraph()
    G.add_nodes_from(range(size))
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = int(links[k])
                if links[k] == '1':
                    G.add_edge(i, j)
                k = k + 1
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=isDirected)
    plt.axis('off')
    plt.savefig(fileName)