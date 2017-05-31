import os
import sys
sys.path.append( os.getcwd() +"//..")
from graph_features import initGraph
import numpy as np
from learning.TagsLoader import TagsLoader
from features_calculator import featuresCalculator
import featuresList
from sklearn import metrics
import pickle
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt
import numpy
from sklearn import metrics
from sklearn.model_selection import train_test_split
import itertools
import os

currentDirectory = str(os.getcwd())

def neighbor(G,start):
    if (G.is_directed()):
        return itertools.chain(G.successors(start), G.predecessors(start))
    else:
        return G.neighbors(start)

def init_vertex_dict_by_edges(gnx,trains,tags):
    vertex_dict ={}
    count = 0
    for test_size in trains:
        vertex_dict[test_size] = {}
        for v in gnx.nodes():
            vertex_dict[test_size][v] = {'out_pos':0,
                                         'out_neg':0,
                                         'in_pos':0,
                                         'in_neg':0}
    edges = gnx.edges()
    for e in edges:
        count +=1
        print count,len(edges)
        for test_size in trains:
            if e in trains[test_size]:
                color = tags[e]
                if color == 1:
                    vertex_dict[test_size][e[0]]['out_pos'] +=1
                    vertex_dict[test_size][e[1]]['in_pos'] +=1
                elif color == -1:
                    vertex_dict[test_size][e[0]]['out_neg'] +=1
                    vertex_dict[test_size][e[1]]['in_neg'] +=1

    return vertex_dict


def calc_local_sign_features(gnx,trains,tags,global_features):
    train_feature ={}
    test_features ={}
    for test_size in trains.keys():
        print type(test_size)
        train_feature[test_size] = []
        test_features[test_size] = []
    count =0
    # vertex_dict = init_vertex_dict(gnx,train,test,tags)
    vertex_dict = init_vertex_dict_by_edges(gnx,trains,tags)
    # print vertex_dict
    edges = gnx.edges()
    for e in gnx.edges():
        count+=1
        print count,len(edges)
        src_vertex = e[0]
        trg_vertex = e[1]

        e_color = tags[e]
        for test_size in trains:
            if e in trains[test_size]:
                if e_color == 1:
                    train_feature[test_size].append([e,vertex_dict[test_size][src_vertex]['out_pos']-1,
                                          vertex_dict[test_size][src_vertex]['out_neg'],
                                          vertex_dict[test_size][trg_vertex]['in_pos']-1,
                                          vertex_dict[test_size][trg_vertex]['in_neg']])
                elif e_color == -1:
                    train_feature[test_size].append([e, vertex_dict[test_size][src_vertex]['out_pos'],
                                          vertex_dict[test_size][src_vertex]['out_neg']-1,
                                          vertex_dict[test_size][trg_vertex]['in_pos'],
                                          vertex_dict[test_size][trg_vertex]['in_neg']-1])

                for k in global_features:
                    train_feature[test_size][-1].extend(global_features[k][e])
                train_feature[test_size][-1].append(e_color)
            else:
                test_features[test_size].append([e, vertex_dict[test_size][src_vertex]['out_pos'],
                                      vertex_dict[test_size][src_vertex]['out_neg'],
                                      vertex_dict[test_size][trg_vertex]['in_pos'],
                                      vertex_dict[test_size][trg_vertex]['in_neg']])
                for k in global_features:
                    test_features[test_size][-1].extend(global_features[k][e])
                test_features[test_size][-1].append(e_color)


    return train_feature,test_features

def remove_sign_zero(gnx,tags):
    edges_to_remove =[]
    for t in tags:
        if tags[t] == 0:
            gnx.remove_edge(t[0],t[1])
            edges_to_remove.append(t)
    for e in edges_to_remove:
        del tags[e]

def z_scoring(matrix):
    new_matrix = np.matrix(matrix)

    minimum = np.asarray(new_matrix.min(0))
    for i in range(minimum.shape[1]):
        if minimum[0,i] > 0:
            new_matrix[:,i] = np.log10(new_matrix[:,i])
        elif minimum[0,i] == 0:
            new_matrix[:, i] = np.log10(new_matrix[:, i]+0.1)
        if new_matrix[:,i].std() > 0:
            new_matrix[:,i] = (new_matrix[:,i]-new_matrix[:,i].min())/new_matrix[:,i].std()
    return new_matrix

def perform_learning(train_features, test_features, f_output, local, gglobal, deep = False):
    if (local and gglobal):
        train = [x[1:-1] for x in train_features]
        test = [x[1:-1] for x in test_features]
    elif (local and not gglobal):
        train = [x[1:5] for x in train_features]
        test = [x[1:5] for x in test_features]
    elif (not local and gglobal):
        train = [x[5:-1] for x in train_features]
        test = [x[5:-1] for x in test_features]


    # print train[0]
    train_tags = [x[-1] for x in train_features]
    test_tags = [x[-1] for x in test_features]

    train = z_scoring(train)
    test = z_scoring(test)
    print len(train[0])
    if not deep:
        algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM', 'SGD']
        for algo in algos:
            print algo
            f_output.writelines(algo +'\n')

            if algo == 'adaBoost':
                clf = AdaBoostClassifier(n_estimators=100)
            if algo == 'RF':
                clf = RandomForestClassifier(n_estimators=1000, criterion="gini", min_samples_split=15, oob_score=True,
                                             class_weight='balanced', max_depth=3)
            if algo == 'L-SVM':
                clf = SVC(kernel='linear', class_weight="balanced", C=0.01, probability=True)
            if algo == 'RBF-SVM':
                clf = SVC(class_weight="balanced", C=0.01, probability=True)
            if algo == 'SGD':
                clf = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1, eta0=0.0,
                                    fit_intercept=True, l1_ratio=0.15, learning_rate='optimal', loss='hinge',
                                    n_iter=5, n_jobs=1, penalty='l2', power_t=0.5, random_state=None, shuffle=True,
                                    verbose=0, warm_start=False)
        # print train
            clf.fit(train, train_tags)
            if (algo == 'RF'):
                print len(clf.feature_importances_)
                print clf.feature_importances_
                f_output.writelines(str(clf.feature_importances_)+'\n')
            evaluate_auc(clf, test, test_tags, train, train_tags,f_output)

    else:
        print train[0]

        from keras.models import Sequential
        from keras.layers import Dense, Dropout
        from keras.regularizers import l2, l1_l2

        clf = Sequential()
        clf.add(
            Dense(100, activation="relu", kernel_initializer="he_normal", input_dim=train.shape[1]))
        # self.classifier.add(Dropout(0.5))
        # self.classifier.add(Dense(100, init='he_normal', activation='relu', W_regularizer=l2(0.5)))
        clf.add(Dropout(0.1))
        clf.add(Dense(1, init='uniform', activation='relu', W_regularizer=l1_l2(0.4)))
        clf.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        clf.fit(train, train_tags, validation_data=[test, test_tags], epochs=100,
                            batch_size=10, verbose=2)

        evaluate_auc(clf, test, test_tags, train, train_tags)


def evaluate_auc(clf, test, test_tags, train, train_tags,f_output):
    predictions = clf.predict(test)
    test_fpr, test_tpr, thresholds = metrics.roc_curve(test_tags, predictions)
    aucTest = np.trapz(test_tpr, test_fpr)
    print 'Auc Test:', aucTest
    f_output.writelines('Auc Test:'+str(aucTest)+'\n')
    predictions = clf.predict(train)
    train_fpr, train_tpr, thresholds = metrics.roc_curve(train_tags, predictions)
    aucTrain = np.trapz(train_tpr, train_fpr)
    print 'Auc Train', aucTrain
    f_output.writelines('Auc Train:'+str(aucTrain)+'\n')


def calc_by_train_size(graph_name,test_sizes,f_output,random_state,load,deep):
    for test_size in test_sizes:
        output_result_dir = './../data/result_social_sign/'+graph_name+'/'+str(test_size)+'/'
        if (not os.path.exists(output_result_dir)):
            os.mkdir(output_result_dir)
    if not load:
        wdir = os.getcwd()
        file_in = str(wdir) + r'/../data/directed/social_sign/'+graph_name+'/input/'+graph_name+'.txt'
        classification_result = [graph_name+'-tags']
        directory_tags_path = str(wdir) + r'/../data/directed/social_sign/'+graph_name+'/tags/'


        # file_in = str(wdir) + r'/../data/directed/social_sign/epinions/input/epinions.txt'
        # classification_wiki_result = ['epinions-tags']
        # directory_tags_path = str(wdir) + r'/../data/directed/social_sign/epinions/tags/'


        # file_in = str(wdir) + r'/../data/roi-graph.txt'
        # classification_wiki_result = ['roi-tags']
        # directory_tags_path = str(wdir) + r'/../data/'

        print (' start reload graph')
        # [ggt,   gnx] = initGraph.init_graph(draw = False);
        gnx = initGraph.init_graph(draw=False, file_name=file_in, directed=True, Connected=True);
        print (' finish reload graph')

        calculator = featuresCalculator()
        features_list = featuresList.featuresList(True, 'edges').getFeatures()
        features_list.remove('flow')
        features_list.remove('ab')
        features_list.remove('edge_flow')
        features_list.remove('edge_betweenness')
        features_list.remove('motif4')
        if(graph_name in ['epinions']):
            features_list.remove('kcore')

        print features_list
        # output_dir = str(wdir) + r'/../data/directed/social_sign/epinions/features'
        output_dir = str(wdir) + r'/../data/directed/social_sign/'+graph_name+'/features'
        # output_dir = str(wdir) + r'/../data/'
        result = calculator.calculateFeatures(features_list, file_in, output_dir, True, 'edges', parallel=False)

        tagsLoader = TagsLoader(directory_tags_path, classification_result)
        tagsLoader.load_edges()
        # tags = tagsLoader.calssification_to_edge_to_tag['epinions-tags']
        tags = tagsLoader.calssification_to_edge_to_tag[classification_result[0]]
        # tags = tagsLoader.calssification_to_edge_to_tag['roi-tags']
        print tagsLoader.calssification_to_edge_to_tag.keys()

        remove_sign_zero(gnx,tags)
        edges = gnx.edges()
        print len(edges)
        print len(gnx.nodes())
        print len(tags)
        s_e = set(edges)
        s_t = set(tags.keys())
        print s_e.difference(s_t)
        print s_t.difference(s_e)
        new_tags =[]
        for e in edges:
            new_tags.append(tags[e])

        # random_state = random.randint(0,len(edges))
        # random_state = 2
        X_train = {}
        X_test ={}
        Y_train = {}
        Y_test ={}
        for test_size in test_sizes:
            x_train , x_test, y_train, y_test = train_test_split(edges,new_tags,
                                                                test_size=test_size,
                                                                random_state=random_state)

            X_train[test_size] = x_train
            X_test[test_size] = x_test
            Y_train[test_size] = y_train
            Y_test[test_size] = y_test

        # print X_train
        # print X_test
        # print result[1]
        train_features, test_features = calc_local_sign_features(gnx, X_train, tags, result[1])
        # print train_features
        # print test_features
        #
        for test_size in train_features.keys():
            output_result_dir = './../data/result_social_sign/' + graph_name + '/' + str(test_size) + '/'
            with open(output_result_dir +'train_features_'+graph_name+'.dump', 'wb') as f:
                pickle.dump(train_features[test_size], f)
            with open(output_result_dir+'test_features_'+graph_name+'.dump', 'wb') as f:
                pickle.dump(test_features[test_size], f)
        #
    else:
        with open(output_result_dir+'/train_features_'+graph_name+'.dump', 'rb') as f:
            train_features = pickle.load( f)
        with open(output_result_dir+'/test_features_'+graph_name+'.dump', 'rb') as f:
            test_features = pickle.load( f)


    for test_size in train_features.keys():
        print test_size
        f_output.writelines(str(test_size)+'\n')
        train_features_specific = train_features[test_size]
        test_features_specific = test_features[test_size]
        print 'local'
        f_output.writelines('local\n')
        perform_learning(train_features_specific, test_features_specific,f_output, local=True, gglobal=False, deep=deep)
        print 'global'
        f_output.writelines('global\n')
        perform_learning(train_features_specific, test_features_specific,f_output, local=False, gglobal=True, deep=deep)
        print 'Both'
        f_output.writelines('Both\n')
        perform_learning(train_features_specific, test_features_specific,f_output, local=True, gglobal=True, deep=deep)





test_sizes = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]
# test_sizes = [0.2,0.4]
# graph_name = sys.argv[0]
graph_name = 'slashdot'
f_output = open('./../data/result_social_sign/'+graph_name+'/result.txt','w')
calc_by_train_size(graph_name=graph_name,test_sizes=test_sizes,f_output=f_output,random_state=2,load=False,deep=False)
f_output.close()

# for test_size in test_sizes:
#     output_result_dir = './../data/result_social_sign/roi/'+str(test_size)
#     with open(output_result_dir + '/train_features_roi.dump', 'rb') as f:
#         train_features = pickle.load(f)
#     with open(output_result_dir + '/test_features_roi.dump', 'rb') as f:
#         test_features = pickle.load(f)
#
#     print test_size
#     print 'train:'
#     print len(train_features),train_features
#     print 'test:'
#     print len(test_features),test_features