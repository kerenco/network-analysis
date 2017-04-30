from datetime import datetime
import sys
import itertools
# from timeit import default_timer as timerp
from operator import itemgetter
from graph_features.utils import timer

debug = False

def calculte_motif_3_dictionaries(is_directed = True,motif_path=''):
    if(is_directed):
        f = open(motif_path + r'/3_nodes_data_directed_key.txt')
    else:
        f = open(motif_path + r'/3_nodes_data_undirected_key.txt')
    raws = f.readlines()
    motifs_3_vertices_dict = {}
    motifs_3_edges_dict = {}
    motif_edges_index = [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]]
    for r in raws:
        new_raw = r.replace('\r\n', '')
        clean_raw = new_raw.replace('\t', ',')
        s = clean_raw.split(',')
        if (s[0] == '-1'):
            break;
        if(is_directed):
            bit_string = format((int(s[1])), '06b')
            motifs_3_vertices_dict[bit_string] = int(s[0])
            motif_edges = []
            index = 0
            for b in  bit_string:
                if b == '1':
                    motif_edges.append(motif_edges_index[index])
                index += 1
            motifs_3_edges_dict[bit_string] = motif_edges
        else:
            motifs_3_vertices_dict[format((int(s[1])), '03b')] = int(s[0])
    if(debug):
        print motifs_3_vertices_dict
    motifs_3_dict ={}
    motifs_3_dict['v'] = motifs_3_vertices_dict
    motifs_3_dict['e'] = motifs_3_edges_dict
    return motifs_3_dict

def calculte_motif_4_dictionaries(is_directed = True,motif_path=''):
    if(is_directed):
        f = open(motif_path + r'/4_nodes_data_directed_key.txt')
    else:
        f = open(motif_path + r'/4_nodes_data_undirected_key.txt')
    raws = f.readlines()
    motifs_4_vertices_dict = {}
    motif_edges_index = [[0, 1], [0, 2], [0, 3], [1, 0], [1, 2], [1, 3], [2, 0], [2, 1], [2, 3], [3, 0], [3, 1], [3, 2]]
    motifs_4_edges_dict = {}
    for r in raws:
        new_raw = r.replace('\r\n', '')
        clean_raw = new_raw.replace('\t', ',')
        s = clean_raw.split(',')
        if (s[0] == '-1'):
            break;
        if(is_directed):
            bit_string = format((int(s[1])), '012b')
            motifs_4_vertices_dict[bit_string] = int(s[0])
            motif_edges = []
            index = 0
            for b in bit_string:
                if b == '1':
                    motif_edges.append(motif_edges_index[index])
                index += 1
            motifs_4_edges_dict[bit_string] = motif_edges
        else:
            motifs_4_vertices_dict[format((int(s[1])), '03b')] = int(s[0])
    motifs_4_dict = {}
    motifs_4_dict['v'] = motifs_4_vertices_dict
    motifs_4_dict['e'] = motifs_4_edges_dict
    return motifs_4_dict

def get_motif_veriation_list(motifs_number,is_directed,motif_path):
    if (motifs_number == 3):
        motifs_veriations = calculte_motif_3_dictionaries(is_directed,motif_path)
    if (motifs_number == 4):
        motifs_veriations = calculte_motif_4_dictionaries(is_directed,motif_path)
    return motifs_veriations

def initialize_motif_hist(g, motifs_veriations):
    motifs_vertices_hist = {}
    length = max(motifs_veriations['v'].values()) + 1
    for n in g.nodes():
        motifs_vertices_hist[n] = [0] * length

    motifs_edges_hist = {}
    length = max(motifs_veriations['v'].values()) + 1
    for e in g.edges():
        motifs_edges_hist[e] = [0] * length
    motif_hist ={}
    motif_hist['v'] = motifs_vertices_hist
    motif_hist['e'] = motifs_edges_hist
    return motif_hist

def neighbor(G,start):
    if (G.is_directed()):
        return itertools.chain(G.successors(start), G.predecessors(start))
    else:
        return G.neighbors(start)

def add_to_hist_by_subgraph(subg, comb, motifs_hist, motifs_veriations , calculate_edges=False):
    motifs_vertices_hist = motifs_hist['v']
    motifs_vertices_veriations = motifs_veriations['v']
    for n in comb:
        motifs_vertices_hist[n][motifs_vertices_veriations[subg]] += 1
    if(calculate_edges):
        motifs_edges_hist = motifs_hist['e']
        motifs_edges_veriation = motifs_veriations['e']
        for ver in motifs_edges_veriation[subg]:
            edge = (comb[ver[0]],comb[ver[1]])
            motifs_edges_hist[edge][motifs_vertices_veriations[subg]] += 1


count_timer = {'comp':0,'sub':0,'sub_old':0,'hist':0}
def get_sub_tree(g,root,veriation,motifs_veriations,motifsHist,edges_dict, visited_vertices, visited_index,calculate_edges):
    #### motif 3 ####
    #print 'root:',root
    if (veriation == (1,1)):
        neighbors = neighbor(g, root)
        neighbors, visited_neighbors = itertools.tee(neighbors)
        for n in visited_neighbors:
            visited_vertices[n] = visited_index
            visited_index += 1
        for n in neighbors:
            last_neighbors = neighbor(g, n)
            for l in last_neighbors:
                if(visited_vertices.has_key(l)):
                    if(visited_vertices[root] < visited_vertices[n] < visited_vertices[l]):
                        s = [root,n,l]
                        combination_calc(edges_dict,g, motifsHist, motifs_veriations, s,calculate_edges)
                else:
                    visited_vertices[l] = visited_index
                    visited_index += 1
                    s = [root, n, l]
                    combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)
        return [visited_vertices, visited_index]
    if (veriation == (2,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            if (visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]]):
                e1 = comb[0]+','+comb[1]
                e2 = comb[1]+','+comb[0]
                if(not (edges_dict.has_key(e1) or edges_dict.has_key(e2))):
                    s = [root,comb[0],comb[1]]
                    combination_calc(edges_dict,g, motifsHist, motifs_veriations, s, calculate_edges)

    #### motif 4 ####
    if (veriation == (1,1,1)):
        neighbors_first_deg = neighbor(g, root)
        neighbors_first_deg, visited_neighbors,len_a = itertools.tee(neighbors_first_deg,3)
        neighbors_first_deg = list(neighbors_first_deg)
        for n in visited_neighbors:
            visited_vertices[n] = 1
        for comb in itertools.combinations(list(neighbors_first_deg), 3):
            # print '3,0,0'
            s = [root, comb[0], comb[1], comb[2]]
            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)

        for n1 in neighbors_first_deg:
            # print 'n1:',n1
            neighbors_sec_deg = neighbor(g,n1)
            neighbors_sec_deg, visited_neighbors, len_b = itertools.tee(neighbors_sec_deg,3)
            neighbors_sec_deg =list(neighbors_sec_deg)
            for n in visited_neighbors:
                if(not visited_vertices.has_key(n)):
                    visited_vertices[n] = 2
            for n2 in neighbors_sec_deg:
                # print 'n2:',n2
                for n11 in neighbors_first_deg:
                    # print 'n11:',n11
                    # print 'visited_vertices[n2]:',visited_vertices[n2]
                    if(visited_vertices[n2] == 2 and n1 != n11):
                        # print '2,1,0'
                        s = [root, n1, n11, n2]
                        combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)

            for comb in itertools.combinations(neighbors_sec_deg,2):
                if(visited_vertices[comb[0]] == 2 and visited_vertices[comb[1]] == 2):
                    # print '1,2,0'
                    s = [root, n1, comb[0], comb[1]]
                    combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)

            for n2 in neighbors_sec_deg:
                for n3 in neighbor(g,n2):
                    if (not visited_vertices.has_key(n3)):
                        visited_vertices[n3] = 3
                        if(visited_vertices[n2] == 2):
                            # print 'a1,1,1'
                            s = [root, n1, n2, n3]
                            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)
                    else:
                        if(visited_vertices[n3] == 3 and visited_vertices[n2] == 2):
                            # print 'b1,1,1'
                            s = [root, n1, n2, n3]
                            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)
        return [visited_vertices, visited_index]
    # if (veriation == (1,2,0)):
    #     for n1 in neighbor(g, root):
    #         neighbors = neighbor(g,n1)
    #         for comb in itertools.combinations(neighbors, 2):
    #             if (visited_vertices[n1] < visited_vertices[comb[0]] < visited_vertices[comb[1]]):
    #                 e1 = comb[0] + ',' + comb[1]
    #                 e2 = comb[1] + ',' + comb[0]
    #                 e3 = comb[0] + ',' + root
    #                 e4 = root + ',' + comb[0]
    #                 e5 = root + ',' + comb[1]
    #                 e6 = comb[1] + ',' + root
    #                 if(not(edges_dict.has_key(e1) or edges_dict.has_key(e2) or
    #                        edges_dict.has_key(e3) or edges_dict.has_key(e4)
    #                    or edges_dict.has_key(e5) or edges_dict.has_key(e6))):
    #                     s = [root,n1, comb[0], comb[1]]
    #                     print veriation
    #                     combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)
    # if (veriation == (3,0,0)):
    #     neighbors = neighbor(g, root)
    #     print root,list(neighbors)
    #     for comb in itertools.combinations(neighbors, 3):
    #         if(visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]] < visited_vertices[comb[2]]):
    #             # print 'dddd'
    #             e1 = comb[0] + ',' + comb[1]
    #             e2 = comb[1] + ',' + comb[0]
    #             e3 = comb[0] + ',' + comb[2]
    #             e4 = comb[2] + ',' + comb[0]
    #             e5 = comb[2] + ',' + comb[1]
    #             e6 = comb[1] + ',' + comb[2]
    #             # print e1,e2,e3,e4,e5,e6
    #             if (not (edges_dict.has_key(e1) or edges_dict.has_key(e2) or
    #                          edges_dict.has_key(e3) or edges_dict.has_key(e4)
    #                      or edges_dict.has_key(e5) or edges_dict.has_key(e6))):
    #                 s = [root, comb[0], comb[1], comb[2]]
    #                 print veriation
    #                 combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)
    # if (veriation == (2,1,0)):
    #     neighbors = neighbor(g, root)
    #     for comb in itertools.combinations(neighbors, 2):
    #         e1 = comb[0] + ',' + comb[1]
    #         if not edges_dict.has_key(e1):
    #             e2 = comb[1] + ',' + comb[0]
    #             if not edges_dict.has_key(e2):
    #                 neighbors_l = [neighbor(g, x) for x in comb]
    #                 for l in tuple(set(itertools.chain(*neighbors_l))):
    #                     print root,comb[0],comb[1],l
    #                     if (visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]] < visited_vertices[l]):
    #                         s = (root, comb[0], comb[1], l)
    #                         print veriation
    #                         combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, calculate_edges)

def combination_calc(edges_dict,g, motifsHist, motifs_veriations, comb, calculate_edges):
    # print 'comb',comb
    # start_comb = timerp()
    #if(debug): start_sub = timerp()
    subg = mySubgraphStr(edges_dict,g, comb)
    #if (debug): start_hist = timerp()
    add_to_hist_by_subgraph(subg, comb, motifsHist, motifs_veriations,calculate_edges)
    #if (debug): end = timerp()
    # if (debug):
    #     count_timer['comp'] += start_sub - start_comb
    #     count_timer['sub'] += start_hist - start_sub
    #     count_timer['hist'] += end - start_hist
    #     print count_timer
    #

def mySubgraphStr(edges_dict,g,comb):
    # subg = directed_sub_graph(comb, edges_dict)
    if(g.is_directed()):
        subg = directed_sub_graph(comb, edges_dict)
    else:
        subg = undirected_sub_graph(comb, edges_dict)
    return subg

def undirected_sub_graph(comb, edges_dict):
    subg = ''
    for (a, b) in itertools.combinations(comb, 2):
        e = a + ',' + b
        if (edges_dict.has_key(e)):
            subg = subg + '1'
        else:
            subg = subg + '0'
    return subg

def directed_sub_graph(comb, edges_dict):
    subg = ''
    for (a, b) in itertools.permutations(comb, 2):
        e = a + ',' + b
        if (edges_dict.has_key(e)):
            subg = subg + '1'
        else:
            subg = subg + '0'
    return subg

def find_motifs_3(g,motif_path,calculate_edges):
    motifs_veriations = get_motif_veriation_list(3,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    edges_dict = init_edges_dict(g)
    len_nodes = len(list(g.nodes()))
    index = 0
    start = datetime.now()
    degree_list = order_by_degree(g)

    for degree in degree_list:
        n = degree[0]
        visited_vertices = {}
        visited_index = 0
        visited_vertices[n] = 0
        visited_index +=1
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        if(not debug):
            sys.stdout.write('\r' + p)
        #print p
        [visited_vertices, visited_index] = get_sub_tree(g, n, (1, 1), motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index,calculate_edges)
        if(debug):
            print 'end11'
        get_sub_tree(g, n, (2, 0), motifs_veriations, motifsHist,edges_dict, visited_vertices, visited_index,calculate_edges)
        if(debug):
            print 'end22'
        g.remove_node(n)
        if(debug):
            print 'end'
        index = index + 1.0

    end = datetime.now()
    print str(end - start)
    print end
    return motifsHist


def order_by_degree(g):
    nodes = g.nodes()
    degree_list = []
    for n in nodes:
        degree_list.append((n, len(list(neighbor(g,n)))))
    degree_list = sorted(degree_list, key=itemgetter(1), reverse=True)
    return degree_list


def find_motifs_4(g,motif_path,calculate_edges):
    motifs_veriations = get_motif_veriation_list(4,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    edges_dict = init_edges_dict(g)
    len_nodes = len(list(g.nodes()))
    index = 0
    start = datetime.now()

    degree_list = order_by_degree(g)

    for degree in degree_list:
        n = degree[0]
        visited_vertices = {}
        visited_index = 0
        visited_vertices[n] = 0
        visited_index += 1
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        if (not debug):
            sys.stdout.write('\r' + p)
        start_node = datetime.now()
        [visited_vertices, visited_index] = get_sub_tree(g, n, (1, 1, 1),motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index,calculate_edges)
        if(debug):
            print 'finish (1,1,1)  ' + str(datetime.now())
        g.remove_node(n)
        index = index + 1.0

    end = datetime.now()
    print str(end - start)
    print end
    return motifsHist

def init_edges_dict(g):
    edges_dict = {}
    if(g.is_directed()):
        for e in g.edges():
            t = e[0] + ',' + e[1]
            edges_dict[t] = True
    else:
        for e in g.edges():
            t1 = e[0] + ',' + e[1]
            t2 = e[1] + ',' + e[0]
            edges_dict[t1] = True
            edges_dict[t2] = True
    return edges_dict

def find_all_motifs(f, ft, gnx, motif_path, motifs_number= 3,calculate_edges = True):
    gnx_copy = gnx.copy()
    start = timer.start(ft, 'Find Motifs ' + str(motifs_number) + ' ')

    if motifs_number == 3:
        motifs_hist = find_motifs_3(gnx_copy,motif_path, calculate_edges)
    if motifs_number == 4:
        motifs_hist = find_motifs_4(gnx_copy,motif_path, calculate_edges)

    timer.stop(ft, start)
    # print motifs_hist['v']
    # print motifs_hist['e']
    print 'start write to file:  ' + str(datetime.now())
    motifs_vertices_hist = motifs_hist['v']
    for i in motifs_vertices_hist:
        line = str(i)
        for h in motifs_vertices_hist[i]:
            line = line + ',' + str(h)
        f.writelines(line + '\n')
    print 'finish write to file:  ' + str(datetime.now())

    if calculate_edges:
        path = f.name.split('.txt')[0]
        f_edges = open(path + '_directed_edges.txt', 'wb')
        motifs_edges_hist = motifs_hist['e']
        for e in motifs_edges_hist:
            line = e[0]+','+e[1]+' '
            for h in motifs_edges_hist[e]:
                line = line + ',' + str(h)
            f_edges.writelines(line + '\n')
        f_edges.close()
    return motifs_hist