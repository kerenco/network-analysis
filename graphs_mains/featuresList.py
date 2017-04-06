
directed_features = ['general','betweenness','closeness','bfsmoments','flow','ab','kcore','page_rank','motif3', 'motif4'
    ,'load_centrality','average_neighbor_degree','hierarchy_energy','eccentricity']

undirected = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','fiedler_vector',
    'motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree']

edges = ['edge_flow', 'edge_betweenness']
class featuresList:
    def __init__(self, directed, analysisType):
        if directed and analysisType=='nodes':
            self.features = directed_features
        elif directed and analysisType=='edges':
            self.features = directed_features + edges
            self.features.remove('betweenness')
        elif not directed and analysisType=='nodes':
            self.features = undirected
        elif not directed and analysisType=='edges':
            self.features = undirected
            self.features.remove('betweenness')
        else:
            print "Error: could not find the matching features for this type of graph and analysis"


    def getFeatures(self):
        return self.features

# import os
# import sys
# # import LearningPhase
# # import FeturesMatrix
# import numpy as np
# # from TagsLoader import TagsLoader
# import multiprocessing
# from operator import itemgetter
#
# directed_features = ['general', 'betweenness', 'closeness', 'bfsmoments', 'flow', 'ab', 'kcore', 'page_rank', 'motif3',
#                      'motif4'
#     , 'load_centrality', 'average_neighbor_degree', 'hierarchy_energy', 'eccentricity']
#
# undirected = ['general', 'betweenness', 'closeness', 'bfsmoments', 'kcore', 'louvain', 'page_rank', 'fiedler_vector',
#               'motif3', 'eccentricity', 'load_centrality', 'communicability_centrality', 'average_neighbor_degree']
#
# edges = ['edge_flow', 'edge_betweenness']
#
#
# class featuresCalculator:
#     def __init__(self, graph_file, outputDir, directed, analysisType):
#         self.wdir = os.getcwd()
#         self.outputDir = outputDir
#         self.graph_file = graph_file
#         self.directed = directed
#         self.featuresFile = self.import_path(str(self.wdir) + r'/../../../graph-fetures/fetures.py')
#         self.motif_path = str(self.wdir) + r'/../../../graph-fetures/algo_vertices/motifVariations'
#         if directed and analysisType == 'nodes':
#             self.features = directed_features
#         elif directed and analysisType == 'edges':
#             self.features = directed_features + edges
#             self.features.remove('betweenness')
#         elif not directed and analysisType == 'nodes':
#             self.features = undirected
#         elif not directed and analysisType == 'edges':
#             self.features = undirected
#             self.features.remove('betweenness')
#         else:
#             print "Error: could not find the matching features for this type of graph and analysis"
#
#     def import_path(self, fullpath):
#         """
#         Import a file with full path specification. Allows one to
#         import from anywhere, something __import__ does not do.
#         """
#         path, filename = os.path.split(fullpath)
#         filename, ext = os.path.splitext(filename)
#         sys.path.append(path)
#         module = __import__(filename)
#         reload(module)  # Might be out of date
#         del sys.path[-1]
#         return module
#
#     def calculateFeaturesNodes(self):
#         processes = []
#         q = multiprocessing.Queue()
#         lock = multiprocessing.Lock()
#
#         for feature in self.features:
#             takeConnected = True
#             fetures_list = [feature]
#             print fetures_list
#             return_map = False
#
#             processes.append(multiprocessing.Process(target=self.featuresFile.calc_fetures_vertices, args=(
#                 self.graph_file, self.motif_path, self.outputDir, self.directed, takeConnected, fetures_list,
#                 return_map)))
#
#         for pr in processes:
#             pr.start()
#
#         for pr in processes:
#             pr.join()
#
#         result = self.featuresFile.calc_fetures_vertices(self.graph_file, self.motif_path, self.outputDir,
#                                                          directed=self.directed, takeConnected=True
#                                                          , fetures_list=self.features, return_map=True)
#         return result
#
#
# calculator = featuresCalculator(str(os.getcwd()) + r'/../../../data/directed/wiki-rfa/input/wiki.txt',
#                                 str(os.getcwd()) + r'/../../../data/directed/wiki-rfa/features',
#                                 True, 'edges')
# calculator.calculateFeaturesNodes()