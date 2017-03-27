import networkx as nx
import os,sys
import random
def sample_nodes(gnx, n):
    nodes = gnx.nodes()
    set_of_nodes = set()
    while len(set_of_nodes) < n:
        set_of_nodes.add(random.choice(nodes))
    sub = gnx.subgraph(set_of_nodes)
    if nx.is_directed(gnx):
        maximal_connected = max(nx.weakly_connected_component_subgraphs(sub), key=len)
    else:
        maximal_connected = max(nx.connected_component_subgraphs(sub), key=len)
    print maximal_connected.nodes()
    print maximal_connected.edges()
    print len(maximal_connected.edges())
    print len(maximal_connected.nodes())
    return maximal_connected


def sample_edges(gnx, n):
    edges = gnx.edges()
    set_of_edges = set()
    while len(set_of_edges) < n:
        set_of_edges.add(random.choice(edges))
    if nx.is_directed(gnx):
        sub = nx.DiGraph()
        sub.add_edges_from(set_of_edges)
        maximal_connected = max(nx.weakly_connected_component_subgraphs(sub), key=len)
    else:
        sub = nx.Graph()
        sub.add_edges_from(set_of_edges)
        maximal_connected = max(nx.connected_component_subgraphs(sub), key=len)
    print maximal_connected.nodes()
    print maximal_connected.edges()
    print len(maximal_connected.edges())
    print len(maximal_connected.nodes())
    return maximal_connected


def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module

currentDirectory = str(os.getcwd())
#examples for drawing roi-graph.txt
graph_init = import_path(currentDirectory + r'/../graph-fetures/initGraph.py')

graph_file = currentDirectory + r'/../data\directed\citeseer\input\citeseer.txt'
gnx = graph_init.init_graph(draw=False,file_name = graph_file,directed=True,Connected =True);

sample_edges(gnx,500)
sample_nodes(gnx,500)