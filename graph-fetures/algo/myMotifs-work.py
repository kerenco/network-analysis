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
import random

debug = False

def calculte_motif_3_dictionaries(is_directed = True,motif_path=''):
    if(is_directed):
        f = open(motif_path + r'/3_nodes_data_directed_key.txt')
    else:
        f = open(motif_path + r'/3_nodes_data_undirected_key.txt')
    raws = f.readlines()
    motifs_3_dict = {}
    motifs_3_final_dict = {}
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
        motifs_3_final_dict[int(s[0])] = 0
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
        motifs_4_dict[format((int(s[1])), '012b')] = int(s[0])
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
        return itertools.chain(G.successors(start), G.predecessors(start))
    else:
        return G.neighbors(start)

def add_to_hist_by_subgraph(subg,comb,motifsHist,motifs_veriations):
    for n in comb:
        motifsHist[n][motifs_veriations[subg]] = motifsHist[n][motifs_veriations[subg]]  + 1

count_timer = {'comp':0,'sub':0,'sub_old':0,'hist':0}
def get_sub_tree(g,root,veriation,motifs_veriations,motifsHist,comb_visited,edges_dict=[]):
    #### motif 3 ####
    if (veriation == (1,1)):
        neighbors = neighbor(g, root)
        for n in neighbors:
            last_neighbors = neighbor(g, n)
            for l in last_neighbors:
                s = set((l,n,root))
                combination_calc(edges_dict,g, motifsHist, motifs_veriations, s,comb_visited,motif_size = 3)
    if (veriation == (2,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            s = set((comb + (root,)))
            combination_calc(edges_dict,g, motifsHist, motifs_veriations, s,comb_visited, motif_size = 3)

    #### motif 4 ####
    if (veriation == (1,1,1)):
        for n1 in neighbor(g, root):
            for n2 in neighbor(g,n1):
                for n3 in neighbor(g,n2):
                    s = set((root,n1,n2,n3))
                    combination_calc(edges_dict,g, motifsHist, motifs_veriations, s, comb_visited, motif_size=4)
    if (veriation == (1,2,0)):
        for n1 in neighbor(g, root):
            neighbors = neighbor(g,n1)
            for comb in itertools.combinations(neighbors, 2):
                s = set((comb + (n1,) + (root,)))
                combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, comb_visited, motif_size=4)
    if (veriation == (3,0,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 3):
            s = set((comb + (root,)))
            combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, comb_visited, motif_size=4)
    if (veriation == (2,1,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            for x in comb:
                last_neighbors = neighbor(g,x)
                for l in last_neighbors:
                        s = set((comb + (l,) + (root,)))
                        combination_calc(edges_dict, g, motifsHist, motifs_veriations, s, comb_visited, motif_size=4)

def combination_calc(edges_dict,g, motifsHist, motifs_veriations, s,comb_visited, motif_size):
    start_comb = timerp()
    if (len(s) == motif_size):
        comb = tuple(sorted(s))
        if(not comb_visited.has_key(comb)):
            comb_visited[comb] = True
            if(debug): start_sub = timerp()
            subg = mySubgraphStr(edges_dict,g, comb)
            if (debug): start_hist = timerp()
            add_to_hist_by_subgraph(subg, comb, motifsHist, motifs_veriations)
            if (debug): end = timerp()
            if (debug):
                count_timer['comp'] += start_sub - start_comb
                count_timer['sub'] += start_hist - start_sub
                count_timer['hist'] += end - start_hist
                print count_timer

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
    for n in g.nodes():
        comb_visited = {}
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        if(not debug):
            sys.stdout.write('\r' + p)
        #print p
        get_sub_tree(g, n, (1, 1), motifs_veriations, motifsHist, comb_visited,edges_dict)
        if(debug):
            print 'end11'
        get_sub_tree(g, n, (2, 0), motifs_veriations, motifsHist, comb_visited,edges_dict)
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

def find_motifs_4(g,motif_path):
    motifs_veriations = get_motif_veriation_list(4,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    edges_dict = init_edges_dict(g)
    len_nodes = len(list(g.nodes()))
    index = 0
    start = datetime.now()
    for n in g.nodes():
        comb_visited = {}
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        sys.stdout.write('\r' + p)
        get_sub_tree(g, n, (1, 1, 1),motifs_veriations, motifsHist, comb_visited,edges_dict)
        get_sub_tree(g, n, (2, 1, 0),motifs_veriations, motifsHist, comb_visited,edges_dict)
        get_sub_tree(g, n, (1, 2, 0),motifs_veriations, motifsHist, comb_visited,edges_dict)
        get_sub_tree(g, n, (3, 0, 0),motifs_veriations, motifsHist, comb_visited,edges_dict)
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