import math
import networkx as nx
import matplotlib.pyplot as plt

# k = Optimal distance between nodes(if None the distance is set to 1/sqrt(n) where n is the number of nodes),
# pos = positions for nodes(if None, then use random initial positions),
# weight = the edge attribute that holds the numerical value used for the edge weight. (if None, then all edge weights are 1),
# scale = scale factor for positions,
# center = coordinate pair around which to center the layout.
def paint(G, colors, guesses, fileName, k=None, pos=None, weight='weight', scale=1.0, center=None):
    color_list = {0: 'blue', 1: 'red', 2: 'black', 3: 'green', 4: 'yellow', 5: 'palegreen', 6: 'violet', 7: 'purple', 8: 'aqua', 9: 'orange'}
    size = len(colors)
    pos=nx.spring_layout(G, k=k, pos=pos, weight=weight, scale=scale, center=center)
    node_colors = [color_list.values()[color] for node, color in colors.items()]
    plt.figure(figsize=(20.0, 10.0))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=[500 for node in range(size)])
    nx.draw_networkx_edges(G,pos)
    guessed_colors = [color_list.values()[color] for node, color in guesses.items()]
    Gg = nx.DiGraph()
    Gg.add_nodes_from(range(size))
    nx.draw_networkx_nodes(Gg, pos, node_color=guessed_colors, node_size=[200 for node in range(size)])
    plt.title('inside = guess, outside = real color')
    plt.axis('off')
    plt.savefig(fileName)