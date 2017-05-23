from compute_isomap import compute_isomap
from graph_features import initGraph
import os

graph_name = 'DIP'
directed = True
base_path = os.getcwd()
if(directed):
    base_path = base_path +'/../../../data/directed/'+graph_name
else:
    base_path = base_path + '/../../../data/undirected/' +graph_name

file_input = base_path +'/input/'+graph_name+'.txt'
distance_matrix_file_name = base_path +'/results/'+graph_name+'_full_distance_matrix.txt'

#### load the graph undirected!!!! ######
gnx = initGraph.init_graph(draw=False,file_name = file_input,directed=False,Connected = True)
n_neighbors = 5
dim = 20
embedding_output_file = base_path+'/features/output/mds_nodes.txt'
compute_isomap(gnx, n_neighbors, dim, distance_matrix_file_name, embedding_output_file)
