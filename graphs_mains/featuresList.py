
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
