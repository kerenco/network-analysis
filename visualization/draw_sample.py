import os, sys
import graphs_drawing

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

graph_file = currentDirectory + r'/../data/roi-graph.txt'
gnx = graph_init.init_graph(draw=False,file_name = graph_file,directed=True,Connected =True);

#the tags needs to be number 0-4
node_to_tag = {}
node_to_classification = {}
for node in gnx.nodes():
    if node in ['1','2','5']:
        node_to_tag[node] = 0
    else:
        node_to_tag[node] = 3
    if node in ['1' ,'2' ,'4']:
        node_to_classification[node] = 0
    else:
        node_to_classification[node] = 3

draw_file_name  = currentDirectory + r'/roi-graph.html'
graphs_drawing.draw_grah(gnx, draw_file_name, node_to_tag, node_to_classification)
