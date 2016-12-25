import graph_tool
from utils import timer

def find_all_circuits(f, ft, ggt):
    start = timer.start(ft, 'Find Cycles')
    circuits = graph_tool.topology.all_circuits(ggt)
    timer.stop(ft,start)
    for c in circuits:
        first = True
        for v in c:
            if(first):
                f.writelines('[' +str(ggt.vp.id[v]))
                first = False
            else:
                f.writelines(',' + str(ggt.vp.id[v]))
        f.writelines(']\n')