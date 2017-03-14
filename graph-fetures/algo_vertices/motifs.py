import graph_tool as gt
from utils import timer
from datetime import datetime
import os



def find_all_motifs(f, ft, ggt, motifs_number):
    motifs_veriations = get_motif_veriation_list(motifs_number)

    start = timer.start(ft, 'Find Motifs ' + str(motifs_number) + ' ')
    result = gt.clustering.motifs(ggt, motif_list=motifs_veriations, k=motifs_number, return_maps=True)
    timer.stop(ft, start)

    return parse_motif_result(f, ft, ggt, motifs_number, result,motifs_veriations)


def parse_motif_result(f, ft, ggt, motifs_number, result,motifs_veriations):
    mapProperiesIndex = 2;
    mapProp = result[mapProperiesIndex];

    print '1. ' + str(datetime.now())
    motifsHist = initialize_motif_hist(ggt, motifs_veriations)

    print '2. ' + str(datetime.now())
    write_to_file_all_types_of_motifs(ft, result)

    print '3. ' + str(datetime.now())
    motifsByType = calculate_motifs_histogram2(ggt, mapProp, motifsHist, motifs_number)
    print '4. ' + str(datetime.now())
    write_to_file_motif_hist(f, motifsHist)
    return motifsHist, motifsByType


def write_to_file_motif_hist(f, motifs_hist):
    print 'start write to file' + str(datetime.now())
    for i in motifs_hist:
        line = str(i)
        for h in motifs_hist[i]:
            line = line + ',' + str(h)
        f.writelines(line + '\n')
    print 'finish write to file' + str(datetime.now())

def calculate_motifs_histogram2(ggt, map_properties, motifs_hist, motifs_number):
    motifsByType={}
    typeIndex = 0
    for prop in map_properties:
        print str(typeIndex) + '- '+str(len(prop))
        typeIndex +=1
    typeIndex =0
    for prop in map_properties:
        print str(typeIndex) + '- '+str(len(prop)) + '. - ' + str(datetime.now())
        for p in prop:
            if(p!=0):
                for v in p.a:
                    vi = ggt.vp.id[v]
                    motifs_hist[vi][typeIndex] +=1
        typeIndex += 1
    return motifsByType

def calculate_motifs_histogram(ggt, map_properties, motifs_hist, motifs_number):
    typeIndex = 0
    motifsByType = {}
    for prop in map_properties:
        for p in prop:
            countVertices = 0;
            propMotifs = [];
            for v in ggt.vertices():
                if (p != 0 and p[v] != 0):
                    vi = ggt.vp.id[ggt.vertex(p[v])]
                    propMotifs.append(vi)
                    motifs_hist[vi][typeIndex] += 1;
                    countVertices = countVertices + 1;
                countMotifs = []
            if (countVertices != motifs_number):
                vi = ggt.vp.id[ggt.vertex(0)]
                propMotifs.append(vi)
                motifs_hist[vi][typeIndex] += 1;
            countMotifs.append(propMotifs)
        motifsByType[typeIndex] = countMotifs;
        typeIndex += 1
        countMotifs = [];
    return motifsByType

def write_to_file_all_types_of_motifs(ft, result):
    ft.writelines('\nMotifs grups (isomorphisms):\n')
    for g in result[0]:
        ft.writelines(str(g) + '\n')
        for v in g.vertices():
            for e in v.out_edges():
                ft.writelines(str(e))
        ft.writelines('\n')

def initialize_motif_hist(ggt, motifs_veriations):
    motifsHist = {}
    for v in ggt.vertices():
        motifsHist[ggt.vp.id[v]] = [0] * len(motifs_veriations)

    return motifsHist

def get_motif_veriation_list(motifs_number):
    if (motifs_number == 3):
        motifs_veriations = calculte_motif_3()
    if (motifs_number == 4):
        motifs_veriations = calculte_motif_4()
    return motifs_veriations


#### read the types of motifs ####
def createGrpah3(i1,i2,i3,i4,i5,i6):
    g = gt.Graph(directed=True)
    a = g.add_vertex()
    b = g.add_vertex()
    c = g.add_vertex()
    if(i1 == '1' ):
        g.add_edge(a,b)
    if (i2 == '1'):
        g.add_edge(a,c)
    if (i3 == '1'):
        g.add_edge(b,a)
    if (i4 == '1'):
        g.add_edge(b,c)
    if (i5 == '1'):
        g.add_edge(c,a)
    if (i6 == '1'):
        g.add_edge(c,b)
    return g

def createGrpah4(i1, i2, i3, i4, i5, i6,i7,i8,i9,i10,i11,i12):
    g = gt.Graph(directed=True)
    a = g.add_vertex()
    b = g.add_vertex()
    c = g.add_vertex()
    d = g.add_vertex()
    if (i1 == '1'):
        g.add_edge(a, b)
    if (i2 == '1'):
        g.add_edge(a, c)
    if (i3 == '1'):
        g.add_edge(a, d)
    if (i4 == '1'):
        g.add_edge(b, a)
    if (i5 == '1'):
        g.add_edge(b, c)
    if (i6 == '1'):
        g.add_edge(b, d)
    if (i7 == '1'):
        g.add_edge(c, a)
    if (i8 == '1'):
        g.add_edge(c, b)
    if (i9 == '1'):
        g.add_edge(c, d)
    if (i10 == '1'):
        g.add_edge(d, a)
    if (i11 == '1'):
        g.add_edge(d, b)
    if (i12 == '1'):
        g.add_edge(d, c)
    return g

def calculte_motif_3():
    f = open(os.getcwd() + r'/algo_vertices/motifVariations/3_nodes_data_directed_key.txt')
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
        g = createGrpah3(matrix[5], matrix[4], matrix[3], matrix[2], matrix[1], matrix[0])
        ls.append(g)
    return ls

def calculte_motif_4():
    f = open(os.getcwd() + r'/algo_vertices/motifVariations/4_nodes_data_directed_key.txt')
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
        g = createGrpah4(matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5], matrix[6], matrix[7],
                         matrix[8], matrix[9], matrix[10], matrix[11])
        ls.append(g)
    return ls
