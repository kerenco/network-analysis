import os
import sys
# from machineLearing import LearningPhase
# import FeturesMatrix
# import numpy as np
# from TagsLoader import TagsLoader
import multiprocessing



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
f = import_path(currentDirectory + r'/../../../graph-fetures/fetures.py')

# 1 - Degrees
# 2 - betweenes
# 3 - closeness
# 4 - bfs moments
# 5 - flow
# 6 - A.B
# 7 - motif3
# 8 - motif4
# 9 - k-core
# 10 - louvain
# 11 - page_rank
# 12 - fiedler_vector

wdir = os.getcwd()

directed_weighted = ['general','closeness','bfsmoments','flow','ab','kcore','page_rank','hierarchy_energ','motif3','load_centrality','average_neighbor_degree'] #no betweenness,motif4,eccentricity,communicability_centrality
undirected_weighted = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','hierarchy_energ','motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector
directed_unweighted = ['general','betweenness','closeness','bfsmoments','flow','ab','kcore','louvain','page_rank','fiedler_vector','hierarchy_energ','motif3','load_centrality','average_neighbor_degree'] #no motif4,eccentricity,communicability_centrality
undirected_unweighted = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','hierarchy_energ','motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector


directed_features = ['general','betweenness','closeness','bfsmoments','flow','ab','kcore','page_rank','motif3'
    ,'load_centrality','average_neighbor_degree','hierarchy_energy','eccentricity'] #no motif4,'hierarchy_energy','eccentricity'
undirected = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','fiedler_vector',
    'motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector,'hierarchy_energy'
edges = ['edge_flow', 'edge_betweenness']


fast_directed_weighted =['general','kcore','page_rank'] #louvain,motif3

if __name__ == "__main__":
    for i in range(1,2):
        if(i<10):
            snap = '000'+str(i)
        else:
            snap = '00' + str(i)
        print snap

        # snap = '0001'
        file_in = str(wdir) + r'/../../../data/directed/live_journal/'+snap+r'/input/graph.txt'

        output_dir = str(wdir) + r'/../../../data/directed/live_journal/'+snap+r'/features'
        # os.mkdir(output_dir+'//output')
        # os.mkdir(output_dir+'//times')


        processes = []
        q = multiprocessing.Queue()
        lock = multiprocessing.Lock()
        for feature in directed_features:
            file_input = file_in
            motif_path = str(wdir) + r'/../../../graph-fetures/algo/motifVariations'
            outputDirectory = output_dir
            directed = True
            takeConnected = True
            fetures_list = [feature]
            print fetures_list
            return_map = False

            processes.append(multiprocessing.Process(target=f.calc_fetures_vertices,args=(file_input,motif_path,outputDirectory,directed,takeConnected,directed_features,return_map)))

        for pr in processes:
            pr.start()

        for pr in processes:
            pr.join()

        result = f.calc_fetures_vertices(file_input,motif_path,outputDirectory,directed,takeConnected,directed_features,return_map=True)

        print result[1].keys()
