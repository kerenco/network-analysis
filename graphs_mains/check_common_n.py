import pickle
import os
from graph_features import initGraph
import networkx as nx
from sklearn.metrics import accuracy_score

wdir = os.getcwd()
test_sizes = [0.2]
graph_name = 'wiki'
file_in = str(wdir) + r'/../data/directed/social_sign/'+graph_name+'/input/'+graph_name+'.txt'


print (' start reload graph')
gnx = initGraph.init_graph(draw=False, file_name=file_in, directed=False, Connected=True);
print (' finish reload graph')

for test in test_sizes:
    directory = wdir +r'/../data/result_social_sign/'+graph_name+'/'+str(test)+'/'
    with open(directory +'deep_True_True_'+graph_name+'.dump','rb') as f:
        clf =pickle.load(f)

    with open(directory + 'new_test_features_'+graph_name+'.dump','rb') as f:
        features = pickle.load(f)
    # with open(directory + 'train_features_second_'+graph_name+'.dump','rb') as f:
    #     features = pickle.load(f)
    count = 0
    total =0
    predictions = []
    tags = []
    f_0_common = open(directory+'0_common.txt','w')
    f_1_common = open(directory+'1_common.txt','w')
    f_10_common = open(directory+'10_common.txt','w')
    f_25_common = open(directory+'25_common.txt','w')
    for f in features:
        total += 1
        edge = f[0]
        src = edge[0]
        trg = edge[1]
        common_neg = len(list(nx.common_neighbors(gnx, src, trg)))
        predict = clf.predict_proba(f[1:-1])
        tag = f[-1]
        print predict
        print edge
        if  common_neg > 25:
            f_0_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_1_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_10_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_25_common.writelines(str(predict) + ',' + str(tag)+'\n')
            # predictions.append(predict)
            # tags.append(f[-1])
        elif common_neg > 10:
            f_0_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_1_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_10_common.writelines(str(predict) + ',' + str(tag)+'\n')
        elif common_neg > 1:
            f_0_common.writelines(str(predict) + ',' + str(tag)+'\n')
            f_1_common.writelines(str(predict) + ',' + str(tag)+'\n')
        else:
            f_0_common.writelines(str(predict) + ',' + str(tag)+'\n')

        f_0_common.flush()
        f_1_common.flush()
        f_10_common.flush()
        f_25_common.flush()
    print count,total
    # print clf.predict(features[0][1:-1])
    print tags[0:20]
    print predictions[0:20]
    print accuracy_score(tags,predictions)


