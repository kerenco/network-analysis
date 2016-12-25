import networkx as nx
from utils import timer


def flow_mesure(f, ft, gnx):

    start = timer.start(ft, 'Flow Mesure')

    flow_list = calculate_flow_index(gnx)

    timer.stop(ft, start)

    for n in flow_list:
        f.writelines(str(n[0])+','+str(n[1]) + '\n')


def calculate_flow_index(gnx):
    nodes = gnx.nodes()
    flow_list = []
    for n in nodes:
        count_in_nodes = float(len(nx.descendants(gnx, n)))
        count_out_nodes = float(len(nx.ancestors(gnx, n)))
        flow_node = count_out_nodes / (count_in_nodes + count_out_nodes)
        flow_list.append((n, flow_node))

    return flow_list
