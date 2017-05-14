import networkx as nx
from graph_features.utils import timer
from networkx.algorithms.shortest_paths import weighted as weight


def attractor_basin(gnx, f, ft):
    if(not gnx.is_directed()):
        return
    start = timer.start(ft, 'Attractor Basin')
    attractor_dict = calc_attractor_basin(gnx)
    timer.stop(ft, start)
    for k in attractor_dict.keys():
        f.writelines(str(k) + ',' + str(attractor_dict[k]) + '\n')
    return attractor_dict


def calc_attractor_basin(gnx):
    attractor_basin_details= initialize_attraction_basin_dist(gnx)####arrange the details for the calcultions
    attractor_basin = calc_final_attraction_basin(attractor_basin_details,gnx)
    return attractor_basin


def initialize_attraction_basin_dist(gnx):
    attractor_basin_out_dist,attractor_basin_in_dist, avg_in, avg_out = initialize_variables(gnx)
    ####for each node we are calculating the the out and in distances for the other nodes in the graph
    for n in gnx.nodes():
        try:
            in_dist = []
            out_dist = []
            out_nodes=nx.descendants(gnx,n)
            in_nodes=nx.ancestors(gnx,n)
            if (len(out_nodes) != 0):
                out_dist=[weight.dijkstra_path_length(gnx, n, d, weight='weight')for d in out_nodes]
            if(len(in_nodes)!=0):
                in_dist=[weight.dijkstra_path_length(gnx, d, n, weight='weight')for d in in_nodes]
            count_out_dist = [[j, out_dist.count(j)] for j in out_dist]
            count_in_dist=[[j,in_dist.count(j)]for j in in_dist]
            attractor_basin_out_dist.append(list(count_out_dist))
            count_out_dist.clear()####clearing "count_out_dist" for the next node in the loop
            attractor_basin_in_dist.append(list(count_in_dist))
            count_in_dist.clear() ####clearing "count_in_dist" for the next node in the loop
        except:
            attractor_basin_out_dist.append(list())
            attractor_basin_in_dist.append(list())
    ####calculte "avg_out" and "avg_in" for each distance from the details of all the nodes
    avg_out= calc_avg_for_dist(nx.number_of_nodes(gnx),attractor_basin_out_dist)
    avg_in = calc_avg_for_dist(nx.number_of_nodes(gnx),attractor_basin_in_dist)
    attractor_basin_details=[attractor_basin_out_dist,avg_out,attractor_basin_in_dist, avg_in]
    return attractor_basin_details


def initialize_variables(gnx):
    avg_in = []
    avg_out = []
    attractor_basin_out_dist=[]
    attractor_basin_in_dist=[]
    return attractor_basin_out_dist, attractor_basin_in_dist, avg_in, avg_out


def calc_final_attraction_basin(attractor_basin_details, gnx):
    attractor_basin = {}
    avg_out=attractor_basin_details[1]
    avg_in = attractor_basin_details[3]
    for n in gnx.nodes():####running on all the nodes and calculate the value of 'attraction_basin'
        alpha = 2;
        index =gnx.nodes().index(n)
        out_dist = attractor_basin_details[0][index]
        in_dist = attractor_basin_details[2][index]
        numerator = 0
        denominator = 0
        for m in in_dist:####calculating the numerator of the attraction_basin expression
             for avg_in_dist in avg_in:
                if (m[0]==avg_in_dist[0]):
                    numerator = numerator + (m[1] / avg_in_dist[1]) * alpha ** (-m[0])
                    break
        for k in out_dist:####calculating the denominator of the attraction_basin expression
            for avg_out_dist in avg_out:
                if (k[0]==avg_out_dist[0]):
                    denominator = denominator + (k[1] / avg_out_dist[1]) * alpha ** (-k[0])
                    break
        ####calculate the value of 'attraction_basin' of the node n and inssert it to attractor_basin list
        if (denominator == 0):
            attractor_basin[n] = -1
        else:
            attractor_basin[n] = numerator / denominator
    return attractor_basin


def calc_avg_for_dist(num_of_nodes_in_gragh,count_dist):
    #### arange the details in "count_dist" to be with unique distance in the array "all_dist_count"
    all_dist_count=[]
    avg_for_dist=[]
    for place in count_dist:
        for i in place:
            if len(all_dist_count)>0:
                for j in all_dist_count:
                    if (i[0] == j[0]):
                        all_dist_count[ all_dist_count.index(j) ][1] += i[1]
                        break
                    if(j==  all_dist_count[-1]):
                        all_dist_count.append([i[0],i[1]])
                        break
            else:
                all_dist_count.append([i[0], i[1]])

    ####calculating for each distance the average
    for l in all_dist_count:
        avg=float(l[1])/num_of_nodes_in_gragh
        avg_for_dist.append([l[0],avg])
    return avg_for_dist