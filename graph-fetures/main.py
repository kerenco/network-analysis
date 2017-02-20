import initGraph
from datetime import datetime

from algo import general
# from algo import betweennessCentrality
# from algo import motifs
from algo import closenessCentrality
from algo import flow
from algo import bfs
from algo import attractorBasin
from algo import pageRank
from algo import myMotifs
from algo import hierarchyEnergy

########### load graph from file ##########
print (str(datetime.now()) +' start reload graph')
# [ggt,   gnx] = initGraph.init_graph(draw = False);
gnx = initGraph.init_graph_networkx(draw = True,directed=True);
print (str(datetime.now()) +' finish reload graph')


f = open(r'./output/general.txt', 'w')
ft = open(r'./times/general_times.txt', 'w')
general.general_information(gnx, f, ft);
f.close()
ft.close()
print (str(datetime.now()) +' finish general information')

# f = open(r'./output/betweeneseCentrality.txt', 'w')
# ft = open(r'./times/betweeneseCentrality_times.txt', 'w')
# betweennessCentrality.betweenness_centrality(ggt,f,ft, normalized=False);
# f.close()
# ft.close()
# print str(datetime.now()) +' finish betweeneseCentrality'

f = open(r'./output/closenessCentrality.txt', 'w')
ft = open(r'./times/closenessCentrality_times.txt', 'w')
closenessCentrality.closeness_centrality(f,ft,gnx)
f.close()
ft.close()
print (str(datetime.now()) +' finish Closeness Centrality')

f = open(r'./output/bfsDistribution.txt', 'w')
ft = open(r'./times/bfsDistribution_times.txt', 'w')
bfs.bfs_distance_distribution(f, ft, gnx)
f.close()
ft.close()
print (str(datetime.now()) +' finish BFS distance distribution')

f = open(r'./output/flowMesure.txt', 'w')
ft = open(r'./times/flowMesure_times.txt', 'w')
flow.flow_mesure(f,ft,gnx)
f.close()
ft.close()
print (str(datetime.now()) +' finish flow mesure')

f = open(r'./output/attractionBasin.txt', 'w')
ft = open(r'./times/attractionBasin_times.txt', 'w')
attractorBasin.attractor_basin(gnx,f,ft)
f.close()
ft.close()
print (str(datetime.now()) +' finish attraction basin')

f = open(r'./output/pageRank.txt', 'w')
ft = open(r'./times/pageRank_times.txt', 'w')
pageRank.page_rank(gnx,f,ft)
f.close()
ft.close()
print (str(datetime.now()) +' finish pageRank')

f = open(r'./output/hierarchyEnergy.txt', 'w')
ft = open(r'./times/hierarchyEnergy_times.txt', 'w')
hierarchyEnergy.hierarchy_energy(gnx,f,ft)
f.close()
ft.close()
print (str(datetime.now()) +' finish hierarchyEnergy')

print (str(datetime.now()) +' start motifs 3')
f = open(r'./output/motifs3.txt', 'w')
ft = open(r'./times/motifs3_times.txt', 'w')
myMotifs.find_all_motifs(f, ft, gnx, motifs_number= 3)
f.close()
ft.close()
print (str(datetime.now()) +' finish motifs 3')

print (str(datetime.now()) +' start motifs 4')
f = open(r'./output/motifs4.txt', 'w')
ft = open(r'./times/motifs4_times.txt', 'w')
myMotifs.find_all_motifs(f, ft, gnx, motifs_number= 4)
f.close()
ft.close()
print (str(datetime.now()) +' finish motifs 4')


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
