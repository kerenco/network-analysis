import networkx as nx
from utils import timer

def page_rank(gnx, f, ft):
    start = timer.start(ft,'Page Rank')
    page_rank_values = nx.pagerank(gnx, alpha=0.9)
    timer.stop(ft,start)

    for k in page_rank_values.keys():
        f.writelines(str(k) + ',' + str(page_rank_values[k]) + '\n')