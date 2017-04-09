import os
import graphs_drawing
from graph_features import initGraph

currentDirectory = str(os.getcwd())
#examples for drawing roi-graph.txt

graph_file = currentDirectory + r'/../data/roi-graph.txt'
gnx = initGraph.init_graph(draw=False,file_name = graph_file,directed=True,Connected =True);

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
