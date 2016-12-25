from graph_tool.all import *
from utils import timer


def betweenness_centrality(ggt, f, ft, normalized=False):
    b_prop = ggt.new_vertex_property('float')
    ggt.vp.bc = b_prop;

    start = timer.start(ft, 'Betweenness Centrality')
    graph_tool.centrality.betweenness(ggt, vprop=b_prop, norm=normalized)
    timer.stop(ft, start)

    for v in ggt.vertices():
        f.writelines(ggt.vp.id[v] + ',' + str(ggt.vp.bc[v]) + '\n')

    graph_tool.centrality.betweenness(ggt,norm=False)
    nx.betweenness_centrality(gnx, normalized=False)