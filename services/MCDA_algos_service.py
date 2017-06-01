from services import db_service
import graph_features.features as fetures
from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
import numpy as np
import random
import networkx as nx
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def calc_cretria_metrexes(threshold, train_set_size, date, fetures_list):
    print(r""+date+"t="+str(threshold)+"_"+str(train_set_size)+"%.txt")

    [gnx_train, m_train] = fetures.calc_fetures_vertices(
                                                        file_input=r"graph" + date + "t=" + str(threshold) + "_" + str(train_set_size) + "%.txt",
                                                        outputDirectory=r"A1",
                                                        motif_path=r"output",
                                                        directed=True,
                                                        takeConnected=False,
                                                        fetures_list=fetures_list)

    #### Set the algo results to be ready for logistic regression
    x, y, weight_of_edges_train, x_algo_order = matrix_builder(m_train, gnx_train)

    #### Calculate the logistic regresion on the train set
    [gnx, m_gnx] = fetures.calc_fetures_vertices(
        file_input=r"graph"+date+"t="+str(threshold)+"_100%.txt",
        outputDirectory=r"A1",
        motif_path=r"output",
        directed=True,
        takeConnected=False,
        fetures_list=fetures_list)

    #creating the graph with the edges that we are going to test thier direction
    [gnx_test, m_test] =fetures.calc_fetures_vertices (file_input = r"graph"+date+"t="+str(threshold)+"_"+str(100-train_set_size)+"%.txt",
                                    outputDirectory=r"A1",
                                    motif_path=r"output",
                                    directed=True,
                                    fetures_list=[],
                                    takeConnected=False,)

    return gnx_train, m_train, x, x_algo_order, y, weight_of_edges_train,gnx, m_gnx,gnx_test, m_test

###########################################################
####################logistic regression####################
###########################################################

def calc_logistic_score (x, x_algo_order, y, inter_boolean, m_gnx, gnx_test, gnx_train, regression_type):
    model, result = get_logistic_model_coefficients(x, x_algo_order, y, inter_boolean, regression_type)
    prediction_result = calc_regression_score(model, m_gnx, gnx_test)
    score_the_train_data_prediction = calc_regression_score(model, m_gnx, gnx_train)
    max_score_train_data_prediction = max_prediction_score(gnx_train)
    max_score_test_data_prediction = max_prediction_score(gnx_test)

    result.update({'prediction_result': prediction_result,
                   'score_the_train_data_prediction': score_the_train_data_prediction,
                   'max_score_train_data_prediction': max_score_train_data_prediction,
                   'max_score_test_data_prediction': max_score_test_data_prediction})
    return result, model


def calc_regression_score(model, map_features, test_graph):
    result = 0
    ##calculate the value that need to be add when the prediction is correct
    val = 1 / test_graph.number_of_edges()
    #val2= 1/ nx.Graph(test_graph).number_of_edges()
    ##running on all the test set and adding the value to the result
    for edge in test_graph.edges(data=True):
        try:
            map_features_start = []
            map_features_end = []
            for fn in map_features:
                map_features_start.append(map_features[fn][edge[0]])
                map_features_end.append(map_features[fn][edge[1]])
            start_score = model.decision_function(map_features_start)
            end_score = model.decision_function(map_features_end)
            #       score=edge_score(res[0],res[1],model_coef,map_features)
            if (end_score[0] > start_score[0]):
                result += val
        except:
            result += 0
            print("don't have ranks on one of the vertices edge: ", edge)
    return result


def get_logistic_model_coefficients(x, x_algo_order, y, inter_boolean, regression_type):
    #### Calculate the logistic regresion on the train set
    if regression_type is "ridge":
        model = linear_model.Ridge(alpha=.5, fit_intercept=inter_boolean)
        model.fit(x, y)
        f = (model.intercept_, model.coef_)
        print("f ", f)
        model_coefficients = dict(zip(x_algo_order, f[1]))
        model_coefficients['intercept'] = f[0]

    else:
        if regression_type is "lasso":
            model = linear_model.Lasso(alpha=0.1, fit_intercept=inter_boolean)
            model.fit(x, y)
            f = (model.intercept_, model.coef_)
            print("f ", f)
            model_coefficients = dict(zip(x_algo_order, f[1]))
            model_coefficients['intercept'] = f[0]

        else:
            model = LogisticRegression(fit_intercept=inter_boolean)
            model.fit(x, y)
            f = (model.intercept_, model.coef_)
            print("f ", f)
            model_coefficients = dict(zip(x_algo_order, f[1][0]))
            if inter_boolean is True:
                model_coefficients['intercept'] = f[0][0]  # for regressions with intercept
            else:
                model_coefficients['intercept'] = f[0]    # for regressions without intercept

    return model, model_coefficients

def animalRegressionPredictionScroe(model, map_features, db_table_name):
    result = 0
    ##calculating the numbers of rows in the test set
    table_length = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `" + db_table_name + "`;")[0]
    ##calculate the value that need to be add when the prediction is correct
    val = 1/table_length
    ##running on all the test set and adding the value to the result
    query_result = db_service.fetchallQueryResult("SELECT * FROM `" + db_table_name + "`;")
    for res in query_result:
        map_features_start = []
        map_features_end = []
        for fn in map_features:
            map_features_start.append(map_features[fn][res[0]])
            map_features_end.append(map_features[fn][res[1]])
        start_score = model.decision_function(map_features_start)
        end_score = model.decision_function(map_features_end)
#       score=edge_score(res[0],res[1],model_coef,map_fetures)
        if end_score[0] < start_score[0]:
            result += val
    return result

def matrix_builder(map_features, gnx):
    x = []
    y = []
    weight_of_edges = []
    x_algo_order = []
    for n in gnx.nodes():
        for m in gnx.nodes():
            if n < m:
                if gnx.has_successor(n, m):
                    if y.count(1) < y.count(0):
                        features_list_of_n_m = []
                        for fm in map_features:
                            features_list_of_n_m.append(map_features[fm][n] - map_features[fm][m])
                        y.append(1)
                        x.append(features_list_of_n_m)
                        weight_of_edges.append(gnx[n][m]['weight'])
                    else:
                        features_list_of_n_m = []
                        for fm in map_features:
                            features_list_of_n_m.append(map_features[fm][m] - map_features[fm][n])
                        y.append(0)
                        x.append(features_list_of_n_m)
                        weight_of_edges.append(gnx[n][m]['weight'])

                if gnx.has_predecessor(n, m):
                    if y.count(0) < y.count(1):
                        features_list_of_n_m = []
                        for fm in map_features:
                            features_list_of_n_m.append(map_features[fm][m] - map_features[fm][n])
                        y.append(0)
                        x.append(features_list_of_n_m)
                        weight_of_edges.append(gnx[m][n]['weight'])
                    else:
                        features_list_of_n_m = []
                        for fm in map_features:
                            features_list_of_n_m.append(map_features[fm][n] - map_features[fm][m])
                        y.append(1)
                        x.append(features_list_of_n_m)
                        weight_of_edges.append(gnx[m][n]['weight'])
    for fm in map_features:
        x_algo_order.append(fm)
    return x, y, weight_of_edges, x_algo_order

###########################################################
####################        APH        ####################
###########################################################
def run_aph_algos(gnx_test, m_gnx):
    rank_aph1 = aph_1(m_gnx)
    rank_aph2 = aph_2(m_gnx)
    aph_1_2_3_scores = ranking_aph_algos(rank_aph1, rank_aph2, gnx_test, m_gnx)
    return aph_1_2_3_scores

def aph_1(m_gnx):
    score_results = {}
    m_gnx_normed_array = convert_to_normed_arrays_aph1(m_gnx)
    for i in m_gnx_normed_array:# WITH WEIGHT OF 1 FOR ALL THE ALGORITHEMS
        score_results[i] = sum(m_gnx_normed_array[i])
    return score_results

def aph_2(m_gnx):
    m_gnx_list_for_aph2 = convert_to_aph2(m_gnx)
    row_sums = {}
    for i in m_gnx_list_for_aph2: # WITH WEIGHT OF 1 FOR ALL THE ALGORITHEMS
        row_sums[i] = np.asarray(m_gnx_list_for_aph2[i]).sum(axis=0)
    return row_sums

def aph_3(m_gnx, top, buttom):
    res = 1
    for fn in m_gnx:
        res *= m_gnx[fn][top]/m_gnx[fn][buttom]# WITH WEIGHT OF 1 FOR ALL THE ALGORITHEMS
    return res

def convert_to_normed_arrays_aph1(m_gnx):
    res = {}
    secure_random = random.SystemRandom()
    keys = secure_random.choice(list(m_gnx))
    for i in m_gnx[keys]:
        arr = []
        for j in m_gnx:
            try:
                arr.append((m_gnx[j][i] - m_gnx[j][min(m_gnx[j], key=lambda k: m_gnx[j][k])]) /
                            ( m_gnx[j][max(m_gnx[j], key=lambda k: m_gnx[j][k])]
                                                                - m_gnx[j][min(m_gnx[j], key=lambda k: m_gnx[j][k])]))
            except:
                arr.append(0)
        res[i] = arr
    return res

def convert_to_aph2(m_gnx):
    res = {}
    secure_random = random.SystemRandom()
    keys = secure_random.choice(list(m_gnx))
    for i in m_gnx[keys]:
        arr = []
        for j in m_gnx:
            try:
                arr.append(m_gnx[j][i] / m_gnx[j][max(m_gnx[j], key=lambda k: m_gnx[j][k])])
            except:
                arr.append(0)
        res[i] = arr
    return res

def convert_list_to_array(m_list):
    res = []
    for j in m_list:
        res.append(m_list[j])
    return res

def convert_the_results_to_list(row_sums, m_gnx):
    res = {}
    secure_random = random.SystemRandom()
    keys = secure_random.choice(m_gnx)
    counter = 0
    for i in keys:
        res[i] = row_sums[counter]
        counter += 1
    return res

def ranking_aph_algos(rank_aph1, rank_aph2, gnx_test, m_gnx):
    aph_1_score = aph_score(rank_aph1, gnx_test)
    aph_2_score = aph_score(rank_aph2, gnx_test)
    aph_3_score = aph3_score(m_gnx, gnx_test)
    return {'aph_1': aph_1_score, 'aph_2': aph_2_score, 'aph_3': aph_3_score}

def aph_score(aph_rank, test_graph):
    result = 0
    ##calculate the value that need to be add when the prediction is correct
    val = 1 / test_graph.number_of_edges()
    ##running on all the test set and adding the value to the result
    for edge in test_graph.edges(data=True):
        try:
            if aph_rank[edge[1]] > aph_rank[edge[0]]:
                result += val
        except:
            result += 0
            print("don't have ranks on ome of the vertexes edge: ", edge)
    return result

def aph3_score(m_gnx, test_graph):

    result = 0
    #calculate the value that need to be add when the prediction is correct
    val = 1 /test_graph.number_of_edges()
    #running on all the test set and adding the value to the result
    for edge in test_graph.edges(data=True):
        try:
            if aph_3(m_gnx, edge[1], edge[0]) > 1:
                result += val
        except:
            print("don't have ranks on ome of the vertexes edge: ", edge)
    return result


###########################################################
####################      Davids       ####################
###########################################################
def davids(train_table, all_graph_table, test_table):
    score_80 = calc_davids_score(train_table)
    result_train = prediction_scroe(score_80, train_table)
    score_100 = calc_davids_score(all_graph_table)
    result_test = prediction_scroe(score_100, test_table)
    return {'david_prediction_test': result_test, 'david_prediction_train': result_train}

def prediction_scroe(score, db_table_name):
    result = 0
    ##calculating the numbers of rows in the test set
    table_length = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `" + db_table_name + "`;")[0]
    ##calculate the value that need to be add when the prediction is correct
    val = 1/table_length
    ##running on all the test set and adding the value to the result
    query_result = db_service.fetchallQueryResult("SELECT * FROM `" + db_table_name + "`;")
    for res in query_result:
        if score[res[0]] > score[res[1]]:
            result += val
    return result

def calc_davids_score(table):
    result = {}
    animal_list = animal_creator_list(table)
    w, w2, l, l2 = calc_w(animal_list, table)
    for animal in animal_list:
        result[animal] = (w[animal]+w2[animal]-l[animal]-l2[animal])
    return result

def animal_creator_list(db_table_name):
    animal = list()
    query_result = db_service.fetchallQueryResult("SELECT * FROM `" + db_table_name + "`;")
    for res in query_result:
        if res[0] not in animal:
            animal.append(res[0])
        if res[1] not in animal:
            animal.append(res[1])
    return animal

def calc_w (animal_list, table):
    w = {}
    l = {}
    pij = p_ij_getter(table, animal_list)
    for i in animal_list:
        w_i = 0
        l_i = 0
        for j in animal_list:
             if i is not j:
                w_i += pij.get(str(i)+"_"+str(j))
                l_i += pij.get(str(j)+"_"+str(i))
        w[i] = w_i
        l[i] = l_i
    w2, l2 = calc_w2_and_l2(w, l, animal_list, pij)
    return w, w2, l, l2

def calc_w2_and_l2 (w, l, animal_list, pij):
    w2 = {}
    l2 = {}
    for i in animal_list:
        w2_i = 0
        l2_i = 0
        for j in animal_list:
            w2_i += w[j] * pij.get(str(i)+"_"+str(j))
            l2_i += l[j] * pij.get(str(j)+"_"+str(i))
        w2[i] = w2_i
        l2[i] = l2_i
    return w2, l2

def p_ij_getter(table, animal_list):
    pij = {}
    ij = ij_getter_from_db(table, animal_list)
    for i in animal_list:
        for j in animal_list:
            if all([i != j, (ij.get(str(i)+"_"+str(j))+ij.get(str(j)+"_"+str(i))) > 0]):
                    pij[str(i) + "_" + str(j)] = ij.get(str(i) + "_" + str(j)) / (ij.get(str(i) + "_" + str(j)) + ij.get(str(j) + "_" + str(i)))
            else:
                pij[str(i) + "_" + str(j)] = 0

    return pij

def ij_getter_from_db(table, animal_list):
    ij_s = {}
    query_result = db_service.fetchallQueryResult("SELECT `From_E`, `To_E`, COUNT(*) FROM "
                                                  + table + "  GROUP BY `From_E`, `To_E`;")
    for res in query_result:
        ij_s[str(res[0])+"_"+str(res[1])] = res[2]
    for a in animal_list:
        for b in animal_list:
            if str(a)+"_"+str(b) not in ij_s.keys():
                ij_s[str(a) + "_" + str(b)] = 0
    return ij_s

###########################################################
##########         Max Prediction Score          ##########
###########################################################
#in this function there is a bug #
def max_prediction_score(gnx_t):
    result = 0
    a = nx.get_edge_attributes(gnx_t, 'weight')
    for i in gnx_t.nodes():
        for j in gnx_t.nodes():
            if j > i:
                max_ij = 0
                sum_ij = 0
                ij_keys = nx.edges(gnx_t, [i, j])
                for key in ij_keys:
                    if any([all([key[0] == i, key[1] == j]), all([key[0] == j, key[1] == i])]):
                        max_ij = max(max_ij, a.get(key))
                        sum_ij += a.get(key)
                        try:
                            result += max_ij/sum_ij
                        except:
                            print("there are no edges between: ", i, "and: ", j)
    return result
