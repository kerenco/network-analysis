import networkx as nx
# import utils.gnxToGgt as ut

import matplotlib.pyplot as plt
import os;

def init_graph(draw = False):
    #file_name =  os.getcwd() + r"/data/graph.txt"
    #file_name =  os.getcwd() + r"/data/roi-graph.txt"
    # file_name =  os.getcwd() + r"/data/big-graph.txt"
    # (size- nodes - 352797)
    file_name =os.getcwd() + r"/data/roi-graph.txt"
    f = open(file_name,'r')
    lines = f.read();
    lst = lines.split('\n')
    str_edges = [x.split(',') for x in lst]
    edges = [(int(x[0]),int(x[1])) for x in str_edges]
    gnx = nx.DiGraph()
    for e in edges:
        if (e[0] == -1 and e[1] == -1):
            break;
        gnx.add_edges_from([e])
    ggt = ut.nx2gt(gnx);
    #drawing the graph
    if(draw):
      nx.draw_networkx(gnx)
      plt.savefig('graph.png')
    return [ggt,gnx];


def init_graph_networkx(draw = False, directed = True):
    file_name = os.getcwd() + r"/data/roi-graph.txt"
    f = open(file_name, 'r')
    lines = f.read();
    lst = lines.split('\n')
    str_edges = [x.split(',') for x in lst]
    edges = [(int(x[0]), int(x[1])) for x in str_edges]
    if(directed ):
        gnx = nx.DiGraph()
    else:
        gnx = nx.Graph()
    for e in edges:
        if (e[0] == -1 and e[1] == -1):
            break;
        gnx.add_edges_from([e])
    # drawing the graph
    if (draw):
        nx.draw_networkx(gnx)
        plt.savefig('graph.png')
    return gnx;





