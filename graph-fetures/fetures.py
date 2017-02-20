import initGraph
import ReadFeatureFile
import os
from datetime import datetime

from algo import general
import ReadFeatureFile
from algo import betweennessCentrality
# from algo import motifs
from algo import closenessCentrality
from algo import flow
from algo import bfs
from algo import attractorBasin
from algo import myMotifs
from algo import k_core
from algo import louvain
from algo import pageRank
from algo import fiedlerVector
from algo import hierarchyEnergy



def calc_fetures(file_input,motif_path,outputDirectory,directed,fetures_list,weighted=True):
    ######
    # 1 - Degrees
    # 2 - betweenes
    # 3 - closeness
    # 4 - bfs moments
    # 5 - flow
    # 6 - A.B
    # 7 - motif3
    # 8 - motif4
    # 9 - k-core
    # 10 - louvain
    # 11 - page_rank
    # 12 - hierarchyEnerg
    ######

    ########### load graph from file ##########
    print (str(datetime.now()) +' start reload graph')
    # [ggt,   gnx] = initGraph.init_graph(draw = False);
    gnx = initGraph.init_graph(draw=False,file_name = file_input,directed=directed);
    print (str(datetime.now()) +' finish reload graph')

    map_fetures = {}
    wdir = r'./../../graph-fetures'

    if ('general' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/general.txt') or os.stat(str(wdir) + r'/output/general.txt').st_size == 0:
            f = open(outputDirectory + r'/output/general.txt', 'w')
            ft = open(outputDirectory + r'/times/general_times.txt', 'w')
            map_general = general.general_information(gnx, f, ft);
            f.close()
            ft.close()
        else:
            map_general = ReadFeatureFile.fileToMap(str(wdir) + r'/output/general.txt')
        print (str(datetime.now()) +' finish general information')
        map_fetures[1] = map_general

    if ('betweenness' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/betweeneseCentrality.txt') or os.stat(
                        str(wdir) + r'/output/betweeneseCentrality.txt').st_size == 0:
            f = open(outputDirectory + r'./output/betweeneseCentrality.txt', 'w')
            ft = open(outputDirectory  +  r'./times/betweeneseCentrality_times.txt', 'w')
            map_betweenness = betweennessCentrality.betweenness_centrality(gnx,f,ft, normalized=False);
            f.close()
            ft.close()
        else:
            map_betweenness = ReadFeatureFile.fileToMap(str(wdir) + r'/output/betweeneseCentrality.txt')
        print str(datetime.now()) +' finish betweeneseCentrality'
        map_fetures[2] = map_betweenness

    if ('closeness' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/closenessCentrality.txt') or os.stat(str(wdir) + r'/output/closenessCentrality.txt').st_size == 0:
            f = open(outputDirectory + r'/output/closenessCentrality.txt', 'w')
            ft = open(outputDirectory + r'/times/closenessCentrality_times.txt', 'w')
            map_closeness =closenessCentrality.closeness_centrality(f,ft,gnx)
            f.close()
            ft.close()
        else:
            map_closeness = ReadFeatureFile.fileToMap(str(wdir) + r'/output/closenessCentrality.txt')
        print str(datetime.now()) +' finish Closeness Centrality'
        map_fetures[3] = map_closeness

    if('bfsmoments' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/bfsMoments.txt') or os.stat(str(wdir) + r'/output/bfsMoments.txt').st_size == 0:
            f = open(outputDirectory + r'/output/bfsMoments.txt', 'w')
            ft = open(outputDirectory + r'/times/bfsMoments_times.txt', 'w')
            map_bfs = bfs.bfs_distance_distribution(f, ft, gnx)
            f.close()
            ft.close()
        else:
            map_bfs = ReadFeatureFile.fileToMap(str(wdir) + r'/output/bfsMoments.txt')
        print str(datetime.now()) +' finish BFS Moments distribution'
        map_fetures[4] = map_bfs

    if('flow' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/flowMesure.txt') or os.stat(str(wdir) + r'/output/flowMesure.txt').st_size == 0:
            f = open(outputDirectory + r'/output/flowMesure.txt', 'w')
            ft = open(outputDirectory + r'/times/flowMesure_times.txt', 'w')
            map_flow = flow.flow_mesure(f,ft,gnx)
            f.close()
            ft.close()
        else:
            map_flow = ReadFeatureFile.fileToMap(str(wdir) + r'/output/flowMesure.txt')
        print str(datetime.now()) +' finish flow mesure'
        map_fetures[5] = map_flow

    if('ab' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/attractionBasin.txt') or os.stat(str(wdir) + r'/output/attractionBasin.txt').st_size == 0:
            f = open(outputDirectory + r'/output/attractionBasin.txt', 'w')
            ft = open(outputDirectory + r'/times/attractionBasin_times.txt', 'w')
            map_attracttor = attractorBasin.attractor_basin(gnx,f,ft)
            f.close()
            ft.close()
        else:
            map_attracttor = ReadFeatureFile.fileToMap(str(wdir) + r'/output/attractionBasin.txt')
        print str(datetime.now()) +' finish attraction basin'
        map_fetures[6] = map_attracttor

    if('motif3' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/motifs3.txt') or os.stat(str(wdir) + r'/output/motifs3.txt').st_size == 0:
            print str(datetime.now()) +' start motifs 3'
            f = open(outputDirectory + r'/output/motifs3.txt', 'w')
            ft = open(outputDirectory + r'/times/motifs3_times.txt', 'w')
            map_motif3 = myMotifs.find_all_motifs(f, ft, gnx,motif_path = r'./../../graph-fetures/algo/motifVariations', motifs_number= 3)
            f.close()
            ft.close()
        else:
            map_motif3 = ReadFeatureFile.fileToMap(str(wdir) + r'/output/motifs3.txt')
        print str(datetime.now()) + ' finish motifs 3'
        map_fetures[7] = map_motif3

    if('motif4' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/motifs4.txt') or os.stat(str(wdir) + r'/output/motifs4.txt').st_size == 0:
            print str(datetime.now()) +' start motifs 4'
            f = open(outputDirectory + r'/output/motifs4.txt', 'w')
            ft = open(outputDirectory + r'/times/motifs4_times.txt', 'w')
            map_motif4 = myMotifs.find_all_motifs(f, ft, gnx,motif_path = r'./../../graph-fetures/algo/motifVariations', motifs_number= 4)
            f.close()
            ft.close()
        else:
            map_motif4 = ReadFeatureFile.fileToMap(str(wdir) + r'/output/motifs4.txt')
        print str(datetime.now()) + ' finish motifs 4'
        map_fetures[8] = map_motif4

    if('kcore' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/k-core.txt') or os.stat(str(wdir) + r'/output/k-core.txt').st_size == 0:
            print str(datetime.now()) + ' start k-core'
            f = open(outputDirectory + r'/output/k-core.txt', 'w')
            ft = open(outputDirectory + r'/times/k-core_times.txt', 'w')
            map_kcore = k_core.k_core(f,ft,gnx)
            f.close()
            ft.close()
        else:
            map_kcore = ReadFeatureFile.fileToMap(str(wdir) + r'/output/k-core.txt')
        print str(datetime.now()) + ' finish k_core'
        map_fetures[9] = map_kcore

    if ('louvain' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/louvain.txt') or os.stat(
                        str(wdir) + r'/output/louvain.txt').st_size == 0:
            print str(datetime.now()) + ' start louvain'
            f = open(outputDirectory + r'/output/louvain.txt', 'w')
            ft = open(outputDirectory + r'/times/louvain_times.txt', 'w')
            map_louvain = louvain.louvainCommunityDetection(f, ft, gnx)
            f.close()
            ft.close()
        else:
            map_louvain = ReadFeatureFile.fileToMap(str(wdir) + r'/output/louvain.txt')
        print str(datetime.now()) + ' finish louvain'
        map_fetures[10] = map_louvain

    if ('page_rank' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/pageRank.txt') or os.stat(
                        str(wdir) + r'/output/pageRank.txt').st_size == 0:
            f = open(outputDirectory + r'./output/pageRank.txt', 'w')
            ft = open(outputDirectory + r'./times/pageRank_times.txt', 'w')
            map_pageRank = pageRank.page_rank(gnx, f, ft)
            f.close()
            ft.close()
        else:
            map_pageRank = ReadFeatureFile.fileToMap(str(wdir) + r'/output/pageRank.txt')
        print (str(datetime.now()) + ' finish page rank')
        map_fetures[11] = map_pageRank

    if('fiedler_vector' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/fiedlerVector.txt') or os.stat(
                        str(wdir) + r'/output/fiedlerVector.txt').st_size == 0:
            f = open(outputDirectory + r'./output/fiedlerVector.txt', 'w')
            ft = open(outputDirectory + r'./times/fiedlerVector_times.txt', 'w')
            map_fiedlerVector = fiedlerVector.fiedlerVector(gnx, f, ft)
            f.close()
            ft.close()
        else:
            map_fiedlerVector = ReadFeatureFile.fileToMap(str(wdir) + r'/output/fiedlerVector.txt')
        print (str(datetime.now()) + ' finish fiedler vector')
        map_fetures[12] = map_fiedlerVector

    if('hierarchy_energ' in fetures_list):
        if not os.path.isfile(str(wdir) + r'/output/hierarchyEnerg.txt') or os.stat(
                        str(wdir) + r'/output/hierarchyEnerg.txt').st_size == 0:
            f = open(outputDirectory + r'./output/hierarchyEnerg.txt', 'w')
            ft = open(outputDirectory + r'./times/hierarchyEnerg_times.txt', 'w')
            map_hierarchyEnerg = hierarchyEnergy.hierarchyEnerg(gnx,f,ft)
            f.close()
            ft.close()
        else:
            map_hierarchyEnerg = ReadFeatureFile.fileToMap(str(wdir) + r'/output/fiedlerVector.txt')
        print (str(datetime.now()) +' finish hierarchyEnerg')
        map_fetures[13] = map_hierarchyEnerg

    return gnx, map_fetures
    # print str(datetime.now()) +' start motifs 3'
    # f = open(r'./output/motifs3.txt', 'w')
    # ft = open(r'./times/motifs3_times.txt', 'w')
    # motifs.find_all_motifs(f, ft, ggt, motifs_number= 3)
    # f.close()
    # ft.close()
    # print str(datetime.now()) +' finish motifs 3'

    # '''
    # f = open(r'./output/cycles.txt', 'w')
    # ft = open(r'./times/cycles_times.txt', 'w')
    # topology.find_all_circuits(f, ft, ggt)
    # f.close()
    # ft.close()
    # print str(datetime.now()) +' finish cycles'''


# m = calc_fetures(file_input = r'c:\users\keren\Documents\github\network-analysis\data\firms_1996.txt'
#                        ,outputDirectory=r'c:\users\keren\Documents\github\network-analysis\graph-fetures'
#                         ,motif_path=r'C:\Users\Keren\Documents\GitHub\network-analysis\graph-fetures\algo\motifvariations'
#                        ,directed=False
#                        ,weighted=False
#                        ,fetures_list=['general','closeness','bfsmoments','motif3','kcore', 'louvain'])


