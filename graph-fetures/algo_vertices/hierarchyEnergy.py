import numpy as np
from utils import timer


def hierarchy_energy(gnx,f,ft):
    start = timer.start(ft, 'hierarchyEnergy')
    hierarchyEnergy_list, vet_index = calculate_hierarchyEnergy_index(gnx)
    timer.stop(ft, start)
    hierarchyEnergy_map={}
    #writing the results in to file
    num=0
    for n in vet_index:
        f.writelines(str(n)+','+str(hierarchyEnergy_list[num][0]) + '\n')
        hierarchyEnergy_map[n]=hierarchyEnergy_list[num][0]
        num+=1
    return hierarchyEnergy_map


def calculate_hierarchyEnergy_index(gnx):
    vet_index,g=build_graph_matrix(gnx)
    l, y, tol, r, d=initialize_vars_from_laplacian_matrix(g)
#####calculation of hierarchy Energy
    while (np.linalg.norm(r) > tol):
        gamma = np.dot(r.T,r)
        alpha =np.divide(gamma,np.dot(d.T,np.dot(l,d)))
        y = np.add(y, alpha*d)
        r = np.subtract(r,alpha*np.dot(l,d))
        beta = np.divide((np.dot(r.T,r)),gamma)
        d = np.add(r,beta*d)
    else:
        return y,vet_index

def build_graph_matrix (gnx):
    a=[]
    vet_index=gnx.nodes()
    for i in vet_index:
        temp=[]
        for j in gnx.nodes():
            if (gnx.has_edge(i,j)):
                temp.append(1)
            else:
                temp.append(0)
        a.append(temp)
    graph_matrix=np.squeeze(a)
    return vet_index, graph_matrix


def initialize_vars_from_laplacian_matrix(g):
    #creating laplacian matrix
    w=g+g.T
    d= np.diag(sum(w))
    l = d - w
    id = (np.sum(g, 0))
    od = (np.sum(g, 1))
    #initialize_vars
    b = np.subtract((np.array([od])).T,(np.array([id])).T)
    tol = 0.001;
    n = np.size(g, 1)
    y = np.random.rand(n, 1)
    y = np.subtract(y,(1 / n) * sum(y))
    k=np.dot(l, y)
    r =np.subtract(b,k)
    d = r
    return l,y,tol,r,d