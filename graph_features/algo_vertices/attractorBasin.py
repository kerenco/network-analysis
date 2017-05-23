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
    # print("attractor_basin",attractor_basin)
    return attractor_basin


def initialize_attraction_basin_dist(gnx):
    attractor_basin_out_dist,attractor_basin_in_dist, avg_in, avg_out = initialize_variables(gnx)
    ####for each node we are calculating the the out and in distances for the other nodes in the graph
    # print(gnx.nodes())
    dists = weight.all_pairs_dijkstra_path_length(gnx, len(gnx.nodes()), weight='weight')
    for n in gnx.nodes():
        try:
            count_out_dist = {}
            count_in_dist = {}
            out_nodes = nx.descendants(gnx, n)
            in_nodes = nx.ancestors(gnx, n)
            for d in out_nodes:
                if dists[n][d] not in count_out_dist.keys():
                    count_out_dist[dists[n][d]] = 1
                else:
                    count_out_dist[dists[n][d]] += 1
            for d in in_nodes:
                if dists[d][n] not in count_in_dist.keys():
                    count_in_dist[dists[d][n]] = 1
                else:
                    count_in_dist[dists[d][n]] += 1
            attractor_basin_out_dist.append(count_out_dist)
            count_out_dist = {}  ####clearing "count_out_dist" for the next node in the loop
            attractor_basin_in_dist.append(count_in_dist)
            count_in_dist = {}  ####clearing "count_in_dist" for the next node in the loop
        except:
            attractor_basin_out_dist.append({})
            attractor_basin_in_dist.append({})
    ####calculte "avg_out" and "avg_in" for each distance from the details of all the nodes
    avg_out=calc_avg_for_dist(len(gnx.nodes()),attractor_basin_out_dist)
    avg_in =calc_avg_for_dist(len(gnx.nodes()),attractor_basin_in_dist)
    attractor_basin_details=[attractor_basin_out_dist,avg_out,attractor_basin_in_dist, avg_in]
    return attractor_basin_details


def initialize_variables(gnx):
    avg_in = []
    avg_out = []
    attractor_basin_out_dist=[]
    attractor_basin_in_dist=[]
    return attractor_basin_out_dist, attractor_basin_in_dist, avg_in, avg_out


def calc_final_attraction_basin(attractor_basin_details, gnx):
    #print (attractor_basin_details)
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
        for m in in_dist.keys():####calculating the numerator of the attraction_basin expression
            numerator = numerator + (in_dist[m] / avg_in[m]) * alpha ** (-m)
        for k in out_dist.keys():####calculating the denominator of the attraction_basin expression
            denominator = denominator + (out_dist[k] / avg_out[k]) * alpha ** (-k)
        ####calculate the value of 'attraction_basin' of the node n and inssert it to attractor_basin list
        if (denominator == 0):
            attractor_basin[n] = -1
        else:
            attractor_basin[n] = numerator / denominator
    return attractor_basin


def calc_avg_for_dist(num_of_nodes_in_gragh,count_dist):
    #### arange the details in "count_dist" to be with unique distance in the array "all_dist_count"
    all_dist_count={}
    avg_for_dist={}
    for i in range (0,len(count_dist)):
        for j in count_dist[i].keys():
            if (j not in all_dist_count.keys()):
                all_dist_count[j]=count_dist[i][j]
            else: ####if the detail is already in all_dist_count, then we sum the appearance of it
                all_dist_count[j]+=count_dist[i][j]
    ####calculating for each distance the average
    for l in all_dist_count.keys():
        avg=float(all_dist_count[l])/num_of_nodes_in_gragh
        avg_for_dist[l]=avg
    return avg_for_dist