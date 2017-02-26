import networkx as nx
import initGraph
import os
from datetime import datetime
import math
import sys
import time
import itertools
from itertools import izip
from utils import timer
import matplotlib.pyplot as plt
from timeit import default_timer as timerp
from operator import itemgetter

debug = False

def calculte_motif_3_dictionaries(is_directed = True,motif_path=''):
    if(is_directed):
        f = open(motif_path + r'/3_nodes_data_directed_key.txt')
    else:
        f = open(motif_path + r'/3_nodes_data_undirected_key.txt')
    raws = f.readlines()
    motifs_3_dict = {}
    for r in raws:
        new_raw = r.replace('\r\n', '')
        clean_raw = new_raw.replace('\t', ',')
        s = clean_raw.split(',')
        if (s[0] == '-1'):
            break;
        if(is_directed):
            motifs_3_dict[format((int(s[1])), '06b')] = int(s[0])
        else:
            motifs_3_dict[format((int(s[1])), '03b')] = int(s[0])
    if(debug):
        print motifs_3_dict
    return motifs_3_dict

def calculte_motif_4_dictionaries(is_directed = True,motif_path=''):
    if(is_directed):
        f = open(motif_path + r'/4_nodes_data_directed_key.txt')
    else:
        f = open(motif_path + r'/4_nodes_data_undirected_key.txt')
    raws = f.readlines()
    motifs_4_dict = {}
    for r in raws:
        new_raw = r.replace('\r\n', '')
        clean_raw = new_raw.replace('\t', ',')
        s = clean_raw.split(',')
        if (s[0] == '-1'):
            break;
        if (is_directed):
            motifs_4_dict[format((int(s[1])), '012b')] = int(s[0])
        else:
            motifs_4_dict[format((int(s[1])), '03b')] = int(s[0])
    return motifs_4_dict

def get_motif_veriation_list(motifs_number,is_directed,motif_path):
    if (motifs_number == 3):
        motifs_veriations = calculte_motif_3_dictionaries(is_directed,motif_path)
    if (motifs_number == 4):
        motifs_veriations = calculte_motif_4_dictionaries(is_directed,motif_path)
    return motifs_veriations

def initialize_motif_hist(g, motifs_veriations):
    motifsHist = {}
    length = max(motifs_veriations.values()) + 1
    for n in g.nodes():
        motifsHist[n] = [0] * length
    return motifsHist

def neighbor(G,start):
    if (G.is_directed()):
        return itertools.chain(set(G.successors(start))| set(G.predecessors(start)))
    else:
        return G.neighbors(start)

def add_to_hist_by_subgraph(subg,comb,motifsHist,motifs_veriations):
    for n in comb:
        motifsHist[n][motifs_veriations[subg]] += 1

count_timer = {'comp':0,'sub':0,'sub_edges':0,'hist':0}
def get_sub_tree(g,root,veriation,motifs_veriations,motifsHist,edges_dict, visited_vertices, visited_index):
    #### motif 3 ####
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
                        combination_calc(edges_dict,g, motifsHist, motifs_veriations, s,motif_size = 3)
                else:
                    visited_vertices[l] = visited_index
                    visited_index += 1
                    s = [root, n, l]
                    combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=3)
        return [visited_vertices, visited_index]
    if (veriation == (2,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            if (visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]]):
                e1 = comb[0]+','+comb[1]
                e2 = comb[1]+','+comb[0]
                if(not (edges_dict.has_key(e1) or edges_dict.has_key(e2))):
                    s = [root,comb[0],comb[1]]
                    combination_calc(edges_dict,g, motifsHist, motifs_veriations, s, motif_size = 3)

    #### motif 4 ####
    if (veriation == (1,1,1)):
        neighbors_first_deg = neighbor(g, root)
        neighbors_first_deg, visited_neighbors,len_a = itertools.tee(neighbors_first_deg,3)
        for n in visited_neighbors:
            visited_vertices[n] = visited_index
            visited_index += 1
        # first_deg = len(list(len_a));
        # print 'neighbors_first_deg:  ',first_deg
        for n1 in neighbors_first_deg:
            neighbors_sec_deg = neighbor(g,n1)
            neighbors_sec_deg, visited_neighbors, len_b = itertools.tee(neighbors_sec_deg,3)
            for n in visited_neighbors:
                if(not visited_vertices.has_key(n)):
                    visited_vertices[n] = visited_index
                    visited_index += 1
            # first_deg -= 1
            # print str(first_deg) + ':neighbors_sec_deg:  ', len(list(len_b))
            for n2 in neighbors_sec_deg:
                for n3 in neighbor(g,n2):
                    if (visited_vertices.has_key(n3)):
                        if (visited_vertices[root] < visited_vertices[n1] < visited_vertices[n2] < visited_vertices[n3]):
                            s = [root, n1, n2, n3]
                            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=4)
                    else:
                        visited_vertices[n3] = visited_index
                        visited_index += 1
                        s = [root, n1, n2, n3]
                        combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=4)
        return [visited_vertices, visited_index]
    if (veriation == (1,2,0)):
        for n1 in neighbor(g, root):
            neighbors = neighbor(g,n1)
            for comb in itertools.combinations(neighbors, 2):
                if (visited_vertices[root] < visited_vertices[n1] < visited_vertices[comb[0]] < visited_vertices[comb[1]]):
                    e1 = comb[0] + ',' + comb[1]
                    if not edges_dict.has_key(e1):
                        e2 = comb[1] + ',' + comb[0]
                        if not edges_dict.has_key(e2):
                            e3 = comb[0] + ',' + root
                            if not edges_dict.has_key(e3):
                                e4 = root + ',' + comb[0]
                                if not edges_dict.has_key(e4):
                                    e5 = root + ',' + comb[1]
                                    if not edges_dict.has_key(e5):
                                        e6 = comb[1] + ',' + root
                                        if not edges_dict.has_key(e6):
                                            s = [root,n1, comb[0], comb[1]]
                                            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=4)
    if (veriation == (3,0,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 3):
            if(visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]] < visited_vertices[comb[2]]):
                e1 = comb[0] + ',' + comb[1]
                if not edges_dict.has_key(e1):
                    e2 = comb[1] + ',' + comb[0]
                    if not edges_dict.has_key(e2):
                        e3 = comb[0] + ',' + comb[2]
                        if not edges_dict.has_key(e3):
                            e4 = comb[2] + ',' + comb[0]
                            if not edges_dict.has_key(e4):
                                e5 = comb[2] + ',' + comb[1]
                                if not edges_dict.has_key(e5):
                                    e6 = comb[1] + ',' + comb[2]
                                    if not edges_dict.has_key(e6):
                                        s = [root, comb[0], comb[1], comb[2]]
                                        combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=4)
    if (veriation == (2,1,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            e1 = comb[0] + ',' + comb[1]
            if not edges_dict.has_key(e1):
                e2 = comb[1] + ',' + comb[0]
                if not edges_dict.has_key(e2):
                    for x in comb:
                        last_neighbors = neighbor(g,x)
                        for l in last_neighbors:
                                if (visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]] < visited_vertices[l]):
                                        s = [root, comb[0], comb[1], l]
                                        combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, motif_size=4)

def combination_calc(edges_dict,g, motifsHist, motifs_veriations, comb, motif_size):
    # start_comb = timerp()
    # if(debug):
    # start_sub = timerp()
    # print comb
    subg = mySubgraphStr(edges_dict,g, comb)
    # if (debug):
    # start_hist = timerp()
    add_to_hist_by_subgraph(subg, comb, motifsHist, motifs_veriations)
    # if (debug):
    # end = timerp()
    # if (debug):
    # count_timer['comp'] += start_sub - start_comb
    # count_timer['sub'] += start_hist - start_sub
    # count_timer['hist'] += end - start_hist
    #     print count_timer
    #
def mySubgraphStr(edges_dict,g,comb):
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

def find_motifs_3(g,motif_path):
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
        [visited_vertices, visited_index] = get_sub_tree(g, n, (1, 1), motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index)
        if(debug):
            print 'end11'
        get_sub_tree(g, n, (2, 0), motifs_veriations, motifsHist,edges_dict, visited_vertices, visited_index)
        if(debug):
            print 'end22'
        g.remove_node(n)
        if(debug):
            print 'end'
        # print n,degree[1],datetime.now() - start_node
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


def find_motifs_4(g,motif_path):
    motifs_veriations = get_motif_veriation_list(4,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    edges_dict = init_edges_dict(g)
    len_nodes = len(list(g.nodes()))
    start = datetime.now()
    index = 0
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
        [visited_vertices, visited_index] = get_sub_tree(g, n, (1, 1, 1),motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index)
        finish_step1 = datetime.now()
        # print 'finish step 1: ' + str(finish_step1 - start_node)
        # print count_timer
        #print 'finish (1,1,1)  ' + str(datetime.now())
        get_sub_tree(g, n, (2, 1, 0),motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index)
        finish_step2 = datetime.now()
        # print 'finish step 2: ' + str(finish_step2 - finish_step1)
        # print count_timer
        #print 'finish (2,1,0)  ' + str(datetime.now())
        get_sub_tree(g, n, (1, 2, 0),motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index)
        finish_step3 = datetime.now()
        # print 'finish step 3: '  + str(finish_step3 - finish_step2)
        # print count_timer
        #print 'finish (1,2,0)  ' + str(datetime.now())
        get_sub_tree(g, n, (3, 0, 0),motifs_veriations, motifsHist,edges_dict,visited_vertices, visited_index)
        # print 'finish step 4: ' + str(datetime.now() - finish_step3)
        # print count_timer
        #print 'finish (3,0,0)  ' + str(datetime.now())
        # print n +',' +str(degree[1]) +','+ str(datetime.now() - start_node)
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

def find_all_motifs(f, ft, gnx, motif_path, motifs_number= 3):
    gnx_copy = gnx.copy()
    start = timer.start(ft, 'Find Motifs ' + str(motifs_number) + ' ')

    if motifs_number == 3:
        motifsHist = find_motifs_3(gnx_copy,motif_path)
    if motifs_number == 4:
        motifsHist = find_motifs_4(gnx_copy,motif_path)

    timer.stop(ft, start)

    print 'start write to file:  ' + str(datetime.now())
    for i in motifsHist:
        line = str(i)
        for h in motifsHist[i]:
            line = line + ',' + str(h)
        f.writelines(line + '\n')
    print 'finish write to file:  ' + str(datetime.now())

    return motifsHist