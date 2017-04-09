import networkx.linalg.algebraicconnectivity as nx
from graph_features.utils import timer

def fiedlerVector(gnx, f, ft):
    start = timer.start(ft,'fiedler_vector')
    fiedlerVector = nx.fiedler_vector(gnx)
    timer.stop(ft,start)
    fiedlerMap = {}
    for i in range(len(fiedlerVector)):
        f.writelines(str(gnx.nodes()[i]) + ',' + str(fiedlerVector[i]) + '\n')
        fiedlerMap[gnx.nodes()[i]] = fiedlerVector[i]
    return fiedlerMap