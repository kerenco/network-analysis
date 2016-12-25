import networkx as nx
import initGraph
import os
from datetime import datetime
import math
import sys
import time
import itertools
from utils import timer



#### read the types of motifs ####
def createGrpah3(is_directed,i1,i2,i3,i4,i5,i6):
    if(is_directed):
        g = nx.DiGraph()
        if (i1 == '1'):
            g.add_edge(1, 2)
        if (i2 == '1'):
            g.add_edge(1, 3)
        if (i3 == '1'):
            g.add_edge(2, 1)
        if (i4 == '1'):
            g.add_edge(2, 3)
        if (i5 == '1'):
            g.add_edge(3, 1)
        if (i6 == '1'):
            g.add_edge(3, 2)
    else:
        g = nx.Graph()
        if (i1 == '1'):
            g.add_edge(1, 2)
        if (i2 == '1'):
            g.add_edge(1, 3)
        if (i3 == '1'):
            g.add_edge(2, 3)
    return g

def createGrpah4(is_directed,i1, i2, i3, i4, i5, i6,i7,i8,i9,i10,i11,i12):
    if(is_directed):
        g = nx.DiGraph()
        if (i1 == '1'):
            g.add_edge(1, 2)
        if (i2 == '1'):
            g.add_edge(1, 3)
        if (i3 == '1'):
            g.add_edge(1, 4)
        if (i4 == '1'):
            g.add_edge(2, 1)
        if (i5 == '1'):
            g.add_edge(2, 3)
        if (i6 == '1'):
            g.add_edge(2, 4)
        if (i7 == '1'):
            g.add_edge(3, 1)
        if (i8 == '1'):
            g.add_edge(3, 2)
        if (i9 == '1'):
            g.add_edge(3, 4)
        if (i10 == '1'):
            g.add_edge(4, 1)
        if (i11 == '1'):
            g.add_edge(4, 2)
        if (i12 == '1'):
            g.add_edge(4, 3)
    else:
        g = nx.Graph()
        if (i7 == '1'):
            g.add_edge(1, 2)
        if (i8 == '1'):
            g.add_edge(1, 3)
        if (i9 == '1'):
            g.add_edge(1, 4)
        if (i10 == '1'):
            g.add_edge(2, 3)
        if (i11 == '1'):
            g.add_edge(2, 4)
        if (i12 == '1'):
            g.add_edge(3, 4)
    return g

def calculte_motif_3(is_directed = True,motif_path=''):
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
        motifs_3_dict[s[0]] = format((int(s[1])), '06b'), int(s[1])
    motifs_3_dict.pop('0')
    ls = []
    for veriation in motifs_3_dict.values():
        matrix = veriation[0]
        g = createGrpah3(is_directed,matrix[5], matrix[4], matrix[3], matrix[2], matrix[1], matrix[0])
        ls.append(g)
    return ls

def calculte_motif_4(is_directed = True,motif_path=''):
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
        motifs_4_dict[s[0]] = format((int(s[1])), '012b'), int(s[1])
    motifs_4_dict.pop('0')
    ls = []
    for veriation in motifs_4_dict.values():
        matrix = veriation[0]
        g = createGrpah4(is_directed,matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5], matrix[6], matrix[7],
                         matrix[8], matrix[9], matrix[10], matrix[11])
        ls.append(g)
    return ls

def get_motif_veriation_list(motifs_number,is_directed,motif_path):
    if (motifs_number == 3):
        motifs_veriations = calculte_motif_3(is_directed,motif_path)
    if (motifs_number == 4):
        motifs_veriations = calculte_motif_4(is_directed,motif_path)
    return motifs_veriations

def initialize_motif_hist(g, motifs_veriations):
    motifsHist = {}
    for n in g.nodes():
        motifsHist[n] = [0] * len(motifs_veriations)
    return motifsHist

def neighbor(G,start):
    if (G.is_directed()):
        return itertools.chain(G.successors(start), G.predecessors(start))
    else:
        return G.neighbors(start)

def add_to_hist_by_subgraph(subg,motifsHist,motifs_veriations):
    if(len(subg.nodes()) != len(motifs_veriations[0].nodes())):
        # print 'error'
        return
    for i in range(len(motifs_veriations)):
        if( nx.faster_could_be_isomorphic(subg,motifs_veriations[i]) ):
            if nx.is_isomorphic(subg, motifs_veriations[i]):
                for v in subg:
                    motifsHist[v][i] = motifsHist[v][i] + 1
                return

def get_sub_tree(g,root,veriation,motifs_veriations,motifsHist,comb_visited):
    if (veriation == (1,1)):
        neighbors = neighbor(g, root)
        for n in neighbors:
            last_neighbors = neighbor(g, n)
            for l in last_neighbors:
                comb = tuple(sorted((l,) + (n,)+(root,)))
                if(not comb_visited.has_key(comb)):
                    comb_visited[comb] = True
                    subg = g.subgraph(comb)
                    add_to_hist_by_subgraph(subg,motifsHist,motifs_veriations)
    if (veriation == (2,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            comb_new = tuple(sorted(comb + (root,)))
            if (not comb_visited.has_key(comb_new)):
                comb_visited[comb_new] = True
                subg = g.subgraph(comb_new)
                add_to_hist_by_subgraph(subg, motifsHist, motifs_veriations)
    if (veriation == (1,1,1)):
        for n1 in neighbor(g, root):
            for n2 in neighbor(g,n1):
                for n3 in neighbor(g,n2):
                    comb = tuple(sorted((root,) + (n1,) + (n2,)+(n3,)))
                    if (not comb_visited.has_key(comb)):
                        comb_visited[comb] = True
                        subg = g.subgraph(comb)
                        add_to_hist_by_subgraph(subg, motifsHist, motifs_veriations)

    if (veriation == (1,2,0)):
        for n1 in neighbor(g, root):
            neighbors = neighbor(g,n1)
            for comb in itertools.combinations(neighbors, 2):
                comb_new = tuple(sorted(comb + (n1,) + (root,)))
                if (not comb_visited.has_key(comb_new)):
                    comb_visited[comb_new] = True
                    subg = g.subgraph(comb_new)
                    add_to_hist_by_subgraph(subg, motifsHist, motifs_veriations)
    if (veriation == (3,0,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 3):
            comb_new = tuple(sorted(comb + (root,)))
            if (not comb_visited.has_key(comb_new)):
                comb_visited[comb_new] = True
                subg = g.subgraph(comb_new)
                add_to_hist_by_subgraph(subg, motifsHist, motifs_veriations)
    if (veriation == (2,1,0)):
        neighbors = neighbor(g, root)
        for comb in itertools.combinations(neighbors, 2):
            for x in comb:
                last_neighbors = neighbor(g,x)
                for l in last_neighbors:
                        comb_new = tuple(sorted(comb + (l,) + (root,)))
                        if (not comb_visited.has_key(comb_new)):
                            comb_visited[comb_new] = True
                            subg = g.subgraph(comb_new)
                            add_to_hist_by_subgraph(subg, motifsHist, motifs_veriations)

def find_motifs_3(g,motif_path):
    motifs_veriations = get_motif_veriation_list(3,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    len_nodes = len(list(g.nodes()))
    index = 0
    start = datetime.now()
    for n in g.nodes():
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        sys.stdout.write('\r' + p)
        comb_visited = {}
        get_sub_tree(g, n, (1, 1), motifs_veriations, motifsHist, comb_visited)
        get_sub_tree(g, n, (2, 0), motifs_veriations, motifsHist, comb_visited)
        g.remove_node(n)
        index = index + 1.0

    end = datetime.now()
    print str(end - start)
    print end
    return motifsHist

def find_motifs_4(g,motif_path):
    motifs_veriations = get_motif_veriation_list(4,g.is_directed(),motif_path)
    motifsHist = initialize_motif_hist(g, motifs_veriations)
    len_nodes = len(list(g.nodes()))
    index = 0
    start = datetime.now()
    for n in g.nodes():
        p = str(index) + ',' + str(len_nodes) + ': ' + str(index / len_nodes)
        sys.stdout.write('\r' + p)
        comb_visited = {}
        get_sub_tree(g, n, (1, 1, 1),motifs_veriations, motifsHist, comb_visited)
        get_sub_tree(g, n, (1, 2, 0),motifs_veriations, motifsHist, comb_visited)
        get_sub_tree(g, n, (2, 1, 0),motifs_veriations, motifsHist, comb_visited)
        get_sub_tree(g, n, (3, 0, 0),motifs_veriations, motifsHist, comb_visited)
        g.remove_node(n)
        index = index + 1.0

    end = datetime.now()
    print str(end - start)
    print end
    return motifsHist

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