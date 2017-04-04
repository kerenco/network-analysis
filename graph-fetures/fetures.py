import initGraph
import ReadFeatureFile
import os,sys
from datetime import datetime
import traceback

from algo_vertices import general
import ReadFeatureFile
from algo_vertices import betweennessCentrality
# from algo_vertices import motifs
from algo_vertices import closenessCentrality
from algo_vertices import flow
from algo_vertices import bfs
from algo_vertices import attractorBasin
from algo_vertices import myMotifs
from algo_vertices import k_core
from algo_vertices import louvain
from algo_vertices import pageRank
from algo_vertices import fiedlerVector
from algo_vertices import hierarchyEnergy
from algo_vertices import eccentricity
from algo_vertices import loadCentrality
from algo_vertices import communicabilityCentrality
from algo_vertices import averageNeighborDegree

from algo_edges import edgeFeatureBasedVertices
from algo_edges import minimum_edge_cut
from algo_edges import edge_current_flow_betweenness_centrality
from algo_edges import edge_betweenness_centrality


vertices_algo_dict = {'general' :1,
                      'betweenness':2,
                      'closeness':3,
                      'bfsmoments':4,
                      'flow':5,
                      'ab':6,
                      'motif3':7,
                      'motif4':8,
                      'kcore':9,
                      'louvain':10,
                      'page_rank':11,
                      'fiedler_vector':12,
                      'hierarchy_energy':13,
                      'eccentricity':14,
                      'load_centrality':15,
                      'communicability_centrality':16,
                      'average_neighbor_degree':17}

vertices_algo_feature_directed_length_dict = {'general':2,
                                              'bfsmoments':2,
                                              'motif3':14}

vertices_algo_feature_undirected_length_dict = {'bfsmoments':2,
                                              'motif3':2,
                                                'motif4':11}

def calc_fetures_vertices(file_input, motif_path, outputDirectory, directed, takeConnected, fetures_list,return_map=True):
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
    gnx = initGraph.init_graph(draw=False,file_name = file_input,directed=directed,Connected =takeConnected);
    print (str(datetime.now()) +' finish reload graph')

    map_fetures = {}

    if ('general' in fetures_list):
        try:
            map_general = compute_specific_nav(gnx, outputDirectory,algo_name = 'general')
            map_fetures[1] = map_general
        except:
            print 'error in general:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('betweenness' in fetures_list):
        try:
            map_betweenness = compute_specific_nav(gnx,outputDirectory,algo_name='betweenness')
            map_fetures[2] = map_betweenness
        except:
            print 'error in betweeenness:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('closeness' in fetures_list):
        try:
            map_closeness = compute_specific_nav(gnx, outputDirectory, algo_name='closeness')
            map_fetures[3] = map_closeness
        except:
            print 'error in closeness:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('bfsmoments' in fetures_list):
        try:
            map_bfs = compute_specific_nav(gnx, outputDirectory, algo_name='bfsmoments')
            map_fetures[4] = map_bfs
        except:
            print 'error in bfsmoments:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('flow' in fetures_list):
        try:
            map_flow = compute_specific_nav(gnx, outputDirectory, algo_name='flow')
            map_fetures[5] = map_flow
        except:
            print 'error in flow:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('ab' in fetures_list):
        try:
            map_attracttor = compute_specific_nav(gnx, outputDirectory, algo_name='ab')
            map_fetures[6] = map_attracttor
        except:
            print 'error in attractor basin:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('motif3' in fetures_list):
        try:
            map_motif3 = compute_specific_nav(gnx, outputDirectory, algo_name='motifs3',motif_variations_path = motif_path)
            map_fetures[7] = map_motif3
        except:
            print 'error in motif3:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('motif4' in fetures_list):
        try:
            map_motif4 = compute_specific_nav(gnx, outputDirectory, algo_name='motifs4', motif_variations_path = motif_path)
            map_fetures[8] = map_motif4
        except:
            print 'error in motif4:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('kcore' in fetures_list):
        try:
            map_kcore = compute_specific_nav(gnx, outputDirectory, algo_name='kcore')
            map_fetures[9] = map_kcore
        except:
            print 'error in kcore:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('louvain' in fetures_list):
        try:
            map_louvain = compute_specific_nav(gnx, outputDirectory, algo_name='louvain')
            map_fetures[10] = map_louvain
        except:
            print 'error in louvain:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('page_rank' in fetures_list):
        try:
            map_pageRank = compute_specific_nav(gnx, outputDirectory, algo_name='page_rank')
            map_fetures[11] = map_pageRank
        except:
            print 'error in page_rank:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('fiedler_vector' in fetures_list):
        try:
            map_fiedlerVector = compute_specific_nav(gnx, outputDirectory, algo_name='fiedler_vector')
            map_fetures[12] = map_fiedlerVector
        except:
            print 'error in fiedler_vector:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('hierarchy_energy' in fetures_list):
        try:
            map_hierarchyEnerg = compute_specific_nav(gnx, outputDirectory, algo_name='hierarchy_energy')
            map_fetures[13] = map_hierarchyEnerg
        except:
            print 'error in hierarchy energy:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if('eccentricity' in fetures_list):
        try:
            map_eccentricity = compute_specific_nav(gnx, outputDirectory, algo_name='eccentricity')
            map_fetures[14] = map_eccentricity
        except:
            print 'error in eccentricity:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('load_centrality' in fetures_list):
        try:
            map_load_centrality = compute_specific_nav(gnx, outputDirectory, algo_name='load_centrality')
            map_fetures[15] = map_load_centrality
        except:
            print 'error in load_centrality:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('communicability_centrality' in fetures_list):
        try:
            map_communicability_centrality = compute_specific_nav(gnx, outputDirectory, algo_name='communicability_centrality')
            map_fetures[16] = map_communicability_centrality
        except:
            print 'error in communicability centrality:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if ('average_neighbor_degree' in fetures_list):
        try:
            map_average_neighbor_degree = compute_specific_nav(gnx, outputDirectory, algo_name='average_neighbor_degree')
            map_fetures[17] = map_average_neighbor_degree
        except:
            print 'error in average neighbor:',sys.exc_info()[0]
            print sys.exc_info()[2]
            traceback.print_exc()

    if(return_map):
        return [gnx,map_fetures]

def compute_specific_nav(gnx, outputDirectory,algo_name, motif_variations_path = None):
    file_name = str(outputDirectory) + '/output/' + algo_name + '.txt'
    if (not os.path.isfile(file_name) or os.stat(file_name).st_size == 0):
        f = open(file_name, 'w')
        ft = open(outputDirectory + r'/times/' + algo_name + '_times.txt', 'w')
        map_nav = run_specific_algo_vertices(f, ft, gnx, algo_name, motif_variations_path);
        f.close()
        ft.close()
    else:
        map_nav = ReadFeatureFile.fileToMap_vertices(file_name)
    print (str(datetime.now()) + ' finish ' + algo_name + ' information')
    return map_nav

def run_specific_algo_vertices(f, ft, gnx, algo_name, motif_variations_path = None):

    if('general' == algo_name):
        return general.general_information(gnx, f, ft)
    elif('betweenness' == algo_name):
        return betweennessCentrality.betweenness_centrality(gnx, f, ft, normalized=False)
    elif ('closeness' == algo_name):
        return closenessCentrality.closeness_centrality(f, ft, gnx)
    elif('bfsmoments' == algo_name):
        return bfs.bfs_distance_distribution(f, ft, gnx)
    elif('flow' == algo_name):
        threshold = 0;
        return flow.flow_mesure(f, ft, gnx, threshold)
    elif('ab' == algo_name):
        return attractorBasin.attractor_basin(gnx, f, ft)
    elif('motifs3' == algo_name):
        return myMotifs.find_all_motifs(f, ft, gnx,
                                        motif_path=motif_variations_path,
                                        motifs_number=3)
    elif('motifs4' == algo_name):
            return myMotifs.find_all_motifs(f, ft, gnx,
                                        motif_path=motif_variations_path,
                                        motifs_number=4)
    elif('kcore' == algo_name):
        return k_core.k_core(f, ft, gnx)
    elif ('louvain' == algo_name):
        return louvain.louvainCommunityDetection(f, ft, gnx)
    elif ('page_rank' == algo_name):
        return pageRank.page_rank(gnx, f, ft)
    elif ('fiedler_vector' == algo_name):
        return fiedlerVector.fiedlerVector(gnx, f, ft)
    elif ('hierarchy_energy' == algo_name):
        return hierarchyEnergy.hierarchy_energy(gnx, f, ft)
    elif ('eccentricity' == algo_name):
        return eccentricity.eccentricity(gnx, f, ft)
    elif ('load_centrality' == algo_name):
        return loadCentrality.load_centrality(gnx, f, ft)
    elif ('communicability_centrality' == algo_name):
        return communicabilityCentrality.communicability_centrality(gnx, f, ft)
    elif ('average_neighbor_degree' == algo_name):
        return averageNeighborDegree.average_neighbor_degree(gnx, f, ft)

def compute_specific_eav(gnx, outputDirectory,algo_name, motif_variations_path = None):
    file_name_edges = str(outputDirectory) + r'/output_edges/' + algo_name + '_edges.txt'
    file_name_vertex = str(outputDirectory) + '/output/' + algo_name + '.txt'
    if (not os.path.isfile(file_name_edges) or os.stat(file_name_edges).st_size == 0):
        file_edges = open(file_name_edges, 'w')
        file_vertex = open(file_name_vertex, 'w')

        file_edges_t = open(outputDirectory + r'/times_edges/' + algo_name + '_times.txt', 'w')
        file_vertex_t = open(outputDirectory + r'/times/' + algo_name + '_times.txt', 'w')
        if (not os.path.isfile(file_name_vertex) or os.stat(file_name_vertex).st_size == 0):
            map_algo = run_specific_algo_vertices(file_vertex, file_vertex_t, gnx,algo_name,motif_variations_path)
        else:
            map_algo = ReadFeatureFile.fileToMap_vertices(file_name_vertex)

        file_vertex.close()
        file_vertex_t.close()
        map_eav = run_specific_algo_edges(file_edges,file_edges_t,gnx,algo_name,map_algo)
        file_edges.close()
        file_edges_t.close()

    else:
        map_eav = ReadFeatureFile.fileToMap_edges(file_name_edges)
    print (str(datetime.now()) + ' finish ' + algo_name + ' information')
    return map_eav

def run_specific_algo_edges(f, ft, gnx, algo_name,map_algo):

    new_edge_algo=['min_cut', 'edge_flow', 'edge_betweenness']
    if(algo_name not in new_edge_algo):
        return edgeFeatureBasedVertices.edge_based_node_feature(f, gnx, map_algo)

    #only for undirected
    elif ('min_cut' == algo_name):
        return minimum_edge_cut.minimum_edge_cut(f, ft,gnx)


    elif ('edge_flow' == algo_name):
        return edge_current_flow_betweenness_centrality.edge_current_flow_betweenness_centrality(f, ft, gnx)

    elif ('edge_betweenness' == algo_name):
        return edge_betweenness_centrality.edge_betweenness_centrality(f, ft, gnx)


def calc_fetures_edges(file_input, motif_path, outputDirectory, directed, takeConnected = False, fetures_list=[], return_map=True):
    print (str(datetime.now()) + ' start reload graph')
    # [ggt,   gnx] = initGraph.init_graph(draw = False);
    gnx = initGraph.init_graph(draw=False, file_name=file_input, directed=directed, Connected=takeConnected);
    print (str(datetime.now()) + ' finish reload graph')

    map_fetures = {}
    new_edge_algo = ['min_cut', 'edge_flow', 'edge_betweenness']

    if ('general' in fetures_list):
        map_general = compute_specific_eav(gnx, outputDirectory, algo_name='general')
        map_fetures[1] = map_general
    if ('closeness' in fetures_list):
        map_closeness = compute_specific_eav(gnx, outputDirectory, algo_name='closeness')
        map_fetures[2] = map_closeness
    if ('bfsmoments' in fetures_list):
        map_bfsmoments = compute_specific_eav(gnx, outputDirectory, algo_name='bfsmoments')
        map_fetures[3] = map_bfsmoments
    if ('flow' in fetures_list):
        map_flow = compute_specific_eav(gnx, outputDirectory, algo_name='flow')
        map_fetures[4] = map_flow
    if ('ab' in fetures_list):
        map_ab = compute_specific_eav(gnx, outputDirectory, algo_name='ab')
        map_fetures[5] = map_ab
    if ('kcore' in fetures_list):
        map_kcore = compute_specific_eav(gnx, outputDirectory, algo_name='kcore')
        map_fetures[6] = map_kcore
    if ('louvain' in fetures_list):
        map_louvain = compute_specific_eav(gnx, outputDirectory, algo_name='louvain')
        map_fetures[7] = map_louvain
    if ('page_rank' in fetures_list):
        map_page_rank = compute_specific_eav(gnx, outputDirectory, algo_name='page_rank')
        map_fetures[8] = map_page_rank
    if ('fiedler_vector' in fetures_list):
        map_fiedler_vector = compute_specific_eav(gnx, outputDirectory, algo_name='fiedler_vector')
        map_fetures[9] = map_fiedler_vector
    if ('hierarchy_energy' in fetures_list):
        map_hierarchy_energy = compute_specific_eav(gnx, outputDirectory, algo_name='hierarchy_energy')
        map_fetures[10] = map_hierarchy_energy
    if ('eccentricity' in fetures_list):
        map_eccentricity = compute_specific_eav(gnx, outputDirectory, algo_name='eccentricity')
        map_fetures[11] = map_eccentricity
    if ('load_centrality' in fetures_list):
        map_load_centrality = compute_specific_eav(gnx, outputDirectory, algo_name='load_centrality')
        map_fetures[12] = map_load_centrality
    if ('communicability_centrality' in fetures_list):
        map_communicability_centrality = compute_specific_eav(gnx, outputDirectory, algo_name='communicability_centrality')
        map_fetures[13] = map_communicability_centrality
    if ('average_neighbor_degree' in fetures_list):
        map_average_neighbor_degree = compute_specific_eav(gnx, outputDirectory, algo_name='average_neighbor_degree')
        map_fetures[14] = map_average_neighbor_degree

    if(return_map):
        return [gnx,map_fetures]