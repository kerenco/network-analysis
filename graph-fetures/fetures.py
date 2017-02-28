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



def calc_fetures(file_input,motif_path,outputDirectory,directed,takeConnected = False,fetures_list=[]):
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
    print takeConnected
    gnx = initGraph.init_graph(draw=False,file_name = file_input,directed=directed,Connected =takeConnected);
    print (str(datetime.now()) +' finish reload graph')

    map_fetures = {}

    if ('general' in fetures_list):
        map_general = compute_specific_nav(gnx, outputDirectory,algo_name = 'general')
        map_fetures[1] = map_general

    if ('betweenness' in fetures_list):
        map_betweenness = compute_specific_nav(gnx,outputDirectory,algo_name='betweeneseCentrality')
        map_fetures[2] = map_betweenness

    if ('closeness' in fetures_list):
        map_closeness = compute_specific_nav(gnx, outputDirectory, algo_name='closenessCentrality')
        map_fetures[3] = map_closeness

    if('bfsmoments' in fetures_list):
        map_bfs = compute_specific_nav(gnx, outputDirectory, algo_name='bfsMoments')
        map_fetures[4] = map_bfs

    if('flow' in fetures_list):
        map_flow = compute_specific_nav(gnx, outputDirectory, algo_name='flowMeasure')
        map_fetures[5] = map_flow

    if('ab' in fetures_list):
        map_attracttor = compute_specific_nav(gnx, outputDirectory, algo_name='attractionBasin')
        map_fetures[6] = map_attracttor

    if('motif3' in fetures_list):
        map_motif3 = compute_specific_nav(gnx, outputDirectory, algo_name='motifs3',motif_variations_path = motif_path)
        map_fetures[7] = map_motif3

    if('motif4' in fetures_list):
        map_motif4 = compute_specific_nav(gnx, outputDirectory, algo_name='motifs4', motif_variations_path = motif_path)
        map_fetures[8] = map_motif4

    if('kcore' in fetures_list):
        map_kcore = compute_specific_nav(gnx, outputDirectory, algo_name='k-core')
        map_fetures[9] = map_kcore

    if ('louvain' in fetures_list):
        map_louvain = compute_specific_nav(gnx, outputDirectory, algo_name='louvain')
        map_fetures[10] = map_louvain

    if ('page_rank' in fetures_list):
        map_pageRank = compute_specific_nav(gnx, outputDirectory, algo_name='pageRank')
        map_fetures[11] = map_pageRank

    if('fiedler_vector' in fetures_list):
        map_fiedlerVector = compute_specific_nav(gnx, outputDirectory, algo_name='fiedlerVector')
        map_fetures[12] = map_fiedlerVector

    if('hierarchy_energ' in fetures_list):
        map_hierarchyEnerg = compute_specific_nav(gnx, outputDirectory, algo_name='hierarchyEnerg')
        map_fetures[13] = map_hierarchyEnerg

    return gnx, map_fetures


def compute_specific_nav(gnx, outputDirectory,algo_name, motif_variations_path = None):
    file_name = str(outputDirectory) + '/output/' + algo_name + '.txt'
    if (not os.path.isfile(file_name) or os.stat(file_name).st_size == 0):
        f = open(file_name, 'w')
        ft = open(outputDirectory + r'/times/' + algo_name + '_times.txt', 'w')
        map_nav = run_specific_algo(f, ft, gnx,algo_name,motif_variations_path);
        f.close()
        ft.close()
    else:
        map_nav = ReadFeatureFile.fileToMap(file_name)
    print (str(datetime.now()) + ' finish ' + algo_name + ' information')
    return map_nav


def run_specific_algo(f, ft, gnx, algo_name, motif_variations_path = None):

    if('general' == algo_name):
        return general.general_information(gnx, f, ft)
    elif('betweeneseCentrality' == algo_name):
        return betweennessCentrality.betweenness_centrality(gnx, f, ft, normalized=False)
    elif ('closenessCentrality' == algo_name):
        return closenessCentrality.closeness_centrality(f, ft, gnx)
    elif('bfsMoments' == algo_name):
        return bfs.bfs_distance_distribution(f, ft, gnx)
    elif('flowMeasure' == algo_name):
        threshold = 0;
        return flow.flow_mesure(f, ft, gnx, threshold)
    elif('attractionBasin' == algo_name):
        return attractorBasin.attractor_basin(gnx, f, ft)
    elif('motifs3' == algo_name):
        return myMotifs.find_all_motifs(f, ft, gnx,
                                        motif_path=motif_variations_path,
                                        motifs_number=3)
    elif('motifs4' == algo_name):
            return myMotifs.find_all_motifs(f, ft, gnx,
                                        motif_path=motif_variations_path,
                                        motifs_number=4)
    elif('k-core' == algo_name):
        return k_core.k_core(f, ft, gnx)
    elif ('louvain' == algo_name):
        return louvain.louvainCommunityDetection(f, ft, gnx)
    elif ('pageRank' == algo_name):
        return pageRank.page_rank(gnx, f, ft)
    elif ('fiedlerVector' == algo_name):
        return fiedlerVector.fiedlerVector(gnx, f, ft)
    elif ('hierarchyEnerg' == algo_name):
        return hierarchyEnergy.hierarchy_energy(gnx, f, ft)


