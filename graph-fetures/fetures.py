import initGraph
from datetime import datetime

from algo import general
# from algo import betweennessCentrality
# from algo import motifs
from algo import closenessCentrality
from algo import flow
from algo import bfs
from algo import attractorBasin
from algo import myMotifs




def calc_fetures(file_input,outputDirectory,directed,fetures_list,weighted=True):
    ######
    # 1 - Degrees
    # 2 - betweenes
    # 3 - closeness
    # 4 - bfs moments
    # 5 - flow
    # 6 - A.B
    # 7 - motif3
    # 8 - motif4
    ######

    ########### load graph from file ##########
    print (str(datetime.now()) +' start reload graph')
    # [ggt,   gnx] = initGraph.init_graph(draw = False);
    gnx = initGraph.init_graph(draw=False,file_name = file_input,directed=directed);
    print (str(datetime.now()) +' finish reload graph')

    map_fetures = {}

    if (1 in fetures_list):
        f = open(outputDirectory + r'./output/general.txt', 'w')
        ft = open(outputDirectory + r'./times/general_times.txt', 'w')
        map_general = general.general_information(gnx, f, ft);
        f.close()
        ft.close()
        print (str(datetime.now()) +' finish general information')
        map_fetures[1] = map_general
    # if (2 in fetures_list):
    #     f = open(outputDirectory + r'./output/betweeneseCentrality.txt', 'w')
    #     ft = open(outputDirectory +1 +  r'./times/betweeneseCentrality_times.txt', 'w')
    #     betweennessCentrality.betweenness_centrality(ggt,f,ft, normalized=False);
    #     f.close()
    #     ft.close()
    #     print str(datetime.now()) +' finish betweeneseCentrality'

    if (3 in fetures_list):
        f = open(outputDirectory + r'./output/closenessCentrality.txt', 'w')
        ft = open(outputDirectory + r'./times/closenessCentrality_times.txt', 'w')
        map_closeness =closenessCentrality.closeness_centrality(f,ft,gnx)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish Closeness Centrality'
        map_fetures[3] = map_closeness

    if(4 in fetures_list):
        f = open(outputDirectory + r'./output/bfsMoments.txt', 'w')
        ft = open(outputDirectory + r'./times/bfsMoments_times.txt', 'w')
        map_bfs = bfs.bfs_distance_distribution(f, ft, gnx)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish BFS Moments distribution'
        map_fetures[4] = map_bfs

    if(5 in fetures_list):
        f = open(outputDirectory + r'./output/flowMesure.txt', 'w')
        ft = open(outputDirectory + r'./times/flowMesure_times.txt', 'w')
        map_flow = flow.flow_mesure(f,ft,gnx)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish flow mesure'
        map_fetures[5] = map_flow

    if(6 in fetures_list):
        f = open(outputDirectory + r'./output/attractionBasin.txt', 'w')
        ft = open(outputDirectory + r'./times/attractionBasin_times.txt', 'w')
        map_attracttor = attractorBasin.attractor_basin(gnx,f,ft)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish attraction basin'
        map_fetures[6] = map_attracttor

    if(7 in fetures_list):
        print str(datetime.now()) +' start motifs 3'
        f = open(outputDirectory + r'./output/motifs3.txt', 'w')
        ft = open(outputDirectory + r'./times/motifs3_times.txt', 'w')
        map_motif3 = myMotifs.find_all_motifs(f, ft, gnx, motifs_number= 3)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish motifs 3'
        map_fetures[7] = map_motif3

    if(8 in fetures_list):
        print str(datetime.now()) +' start motifs 4'
        f = open(outputDirectory + r'./output/motifs4.txt', 'w')
        ft = open(outputDirectory + r'./times/motifs4_times.txt', 'w')
        map_motif4 = myMotifs.find_all_motifs(f, ft, gnx, motifs_number= 4)
        f.close()
        ft.close()
        print str(datetime.now()) +' finish motifs 4'
        map_fetures[8] = map_motif4


    return map_fetures
    # print str(datetime.now()) +' start motifs 3'
    # f = open(r'./output/motifs3.txt', 'w')
    # ft = open(r'./times/motifs3_times.txt', 'w')
    # motifs.find_all_motifs(f, ft, ggt, motifs_number= 3)
    # f.close()
    # ft.close()
    # print str(datetime.now()) +' finish motifs 3'


    '''f = open(r'./output/motifs4.txt', 'w')
    ft = open(r'./times/motifs4_times.txt', 'w')
    motifs.find_all_motifs(f, ft, ggt, motifs_number= 4)
    f.close()
    ft.close()
    print str(datetime.now()) +' finish motifs 4'''''

    '''
    f = open(r'./output/cycles.txt', 'w')
    ft = open(r'./times/cycles_times.txt', 'w')
    topology.find_all_circuits(f, ft, ggt)
    f.close()
    ft.close()
    print str(datetime.now()) +' finish cycles'''



fetures = calc_fetures(file_input = r'c:\users\keren\Documents\github\network-analysis\graph-fetures\data\roi-graph.txt',outputDirectory=r'c:\users\keren\Documents\github\network-analysis\graph-fetures',directed=True,weighted=False,fetures_list=[1,3,4,5,6,7,8])
for k in fetures:
    print k, fetures[k]