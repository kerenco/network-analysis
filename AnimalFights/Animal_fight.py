from services import db_service
from services import MCDA_algos_service
from services import create_tables_service

import os
import csv
import numpy
import networkx as nx
from scipy import stats
from datetime import datetime
from sklearn import linear_model
from subprocess import check_output
import graph_features.features as features
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def featuresEntitiesInializer():
    features_entities = ['betweenness', 'closeness', 'flow', 'ab', 'kcore',
                         'page_rank', 'hierarchy_energy', 'load_centrality']
    return features_entities

def parameterInitalizer():
    features_entities = featuresEntitiesInializer()
    regression_types = {"ridge", "lasso", "regular"}
    number_of_itretions_for_each_table = 1
    train_set_size = 80
    is_removing_algos = False
    return features_entities, regression_types, number_of_itretions_for_each_table, train_set_size, is_removing_algos

def main():
    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\AnimalFights\A1\ShizukaMcDonald_Data")
    date_time = datetime.now()
    problematic_tabels, unconnected_train_graph = initializerResultsArrays()
    features_entities, regression_types, number_of_itretions_for_each_table, train_set_size, is_removing_algos \
                                                                                                = parameterInitalizer()
    for fn in os.listdir('.'):
        if os.path.isfile(fn):
            for i in range(0, number_of_itretions_for_each_table):
                try:
                    print("< - - file name: ", fn, " | i=", i, " - - > ")
                    move_file_details_to_db(os.path.abspath(fn))
                    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis")

                    #create tables section
                    create_tables_for_calcs("animal_fight", train_set_size)

                    #algo's sections: Davids Adagio and Elo
                    num_of_rows_in_table, number_of_comparisons, table_max_prediction_score = table_details()
                    algos_prediction_results = run_algo(fn)
                    algos_prediction_results.update({"num_of_rows_in_table": num_of_rows_in_table, "number_of_comparisons":
                                          number_of_comparisons, "table_max_prediction_score": table_max_prediction_score})

                    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\AnimalFights")
                    for regression_type in regression_types:
                        gnx_train, m_train, gnx, m_gnx, spearmans_rank_correlation, gnx_test, m_gnx_test =\
                                        create_cretria_matrix("animal_fight", train_set_size, features_entities)

                        #APH section
                        aph_1_2_3_scores = MCDA_algos_service.run_aph_algos(gnx_test, m_gnx)
                        algos_prediction_results.update(aph_1_2_3_scores)

                        #regression algo section
                        if nx.is_connected(gnx_train.to_undirected()):
                            f, spearmans_rank_correlation, features_entities_result =\
                                calc_logistic(gnx_train, m_train, m_gnx, features_entities, spearmans_rank_correlation,
                                                                                    regression_type, is_removing_algos)
                            f.update(algos_prediction_results)
                            features_entities = featuresEntitiesInializer()
                            updateF(f, features_entities)
                            insertResultToDB(fn, i, f, spearmans_rank_correlation, regression_type, date_time,
                                                                            features_entities_result, features_entities)
                        else:
                            if fn not in unconnected_train_graph:
                                unconnected_train_graph.append(fn)
                except:
                    print("there is a problem with the table: ", fn)
                    problematic_tabels.append(fn)
                os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\AnimalFights\A1\ShizukaMcDonald_Data")
    print("problematic_tables", problematic_tabels)

def initializerResultsArrays():
    problematic_tables = []
    unconnected_train_graph = []
    return problematic_tables, unconnected_train_graph

def run_algo(fn):
    #Davids
    algos_prediction_results = MCDA_algos_service.davids("animal_fight_80", "animal_fight_100", "animal_fight_20")
    #Elo, Adagio
    algos_prediction_results.update(calculate_adagio_and_elo_predection_score(fn))
    return algos_prediction_results

def updateF(f, features_entities):
    for algo in features_entities:
        if features.vertices_algo_dict.get(algo) not in f:
            f[features.vertices_algo_dict.get(algo)] = 'NULL'

####################################################################
##############       move the file to the db         ###############
####################################################################

def move_file_details_to_db(file):
    ###Trunate tabkes in db
    truncate_tables_in_db()
    ###insert the data to the db
    insert_the_data_in_to_the_db(file)

def truncate_tables_in_db():
    for table in ["`animal_fight`", "`animal_fight_0`", "`animal_fight_100`", "`animal_fight_80`",
                  "`animal_fight_20`"]:
        db_service.executeTruncateQuery(table)

def insert_the_data_in_to_the_db(file):
    f = open(file, 'r')
    reader1 = csv.reader(f, delimiter=',')
    first_row = next(reader1)
    key = {first_row[i]: i for i in range(1, len(first_row))}
    querys_arr = []
    for row in reader1:
        for j in range(1, len(first_row)):
            value = row[j]
            if int(value) > 0:  # and reader1[0] is not first_row [j]):
                for i in range(0, int(value)):
                   querys_arr.append("INSERT INTO animal_fight"
                                                    " VALUES ('" + str(key[row[0]]) + "','" + str(j) + "');")
    db_service.executeInsertQuerysArray(querys_arr)

####################################################################
      ##############        calc_logistic       ###############
####################################################################

def create_cretria_matrix(table, train_set_size, features_list):
    #### Calculate the algo on the 80% data (train)
    print(table)
    [gnx_train, m_train] = features.calc_fetures_vertices(file_input= 'C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\\'
                                                                      + table + "_" + str(train_set_size) + "%.txt",
                                                          outputDirectory='C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\\A1',
                                                          motif_path=r"output",
                                                          directed=True,
                                                          takeConnected=False,
                                                          fetures_list=features_list)

    #calculationg sperman corelations
    spearmans_rank_correlation = calc_spearmans_correlations(m_train, features_list)

    #### Calculate the algorithem on the all graph
    [gnx, m_gnx] = features.calc_fetures_vertices(file_input = 'C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\\'
                                                               + str(table) + "_100%.txt",
                                                  outputDirectory='C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\A1',
                                                  motif_path=r"output",
                                                  directed=True,
                                                  takeConnected=False,
                                                  fetures_list=features_list)

    [gnx_test, m_gnx_test] = features.calc_fetures_vertices(file_input = 'C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\\'
                                                                         + str(table) + "_20%.txt",
                                                            outputDirectory='C:\\Users\\Doron\\workspace\\MasterThasisProject\\network-analysis\\AnimalFights\\A1',
                                                            motif_path=r"output",
                                                            directed=True,
                                                            takeConnected=False,
                                                            fetures_list=[])
    return gnx_train, m_train, gnx, m_gnx, spearmans_rank_correlation, gnx_test, m_gnx_test

def calc_spearmans_correlations(m_train, features_list):
    spearmans_rank_correlation = {}
    for i in features_list:
        for j in features_list:
            if features.vertices_algo_dict[i] < features.vertices_algo_dict[j]:
                try:
                    spearmans_rank_correlation[str(features.vertices_algo_dict[i]) + "_" + str(features.vertices_algo_dict[j])] =\
                        (stats.pearsonr(convert_to_array(m_train[features.vertices_algo_dict[i]]), convert_to_array(m_train[features.vertices_algo_dict[j]])))
                except:
                    spearmans_rank_correlation[str(features.vertices_algo_dict[i]) + "_" + str(features.vertices_algo_dict[j])] = None
    return spearmans_rank_correlation

def calc_logistic(gnx_train, m_train, m_gnx, features_entities, spearmans_rank_correlation, regression_type, is_removing_algos):

    print("<<<<<<<<Regression tpe: ", regression_type, " | fetures_entities: ", features_entities, ">>>>>>>>>")
    x, y, weight_of_edges_train, x_algo_order = MCDA_algos_service.matrix_builder(m_train, gnx_train)
    model, regression_result = MCDA_algos_service.get_logistic_model_coefficients(x, x_algo_order, y, True, regression_type)
    isarray = remove_algo_disicion(regression_result, regression_type, is_removing_algos)

    if isarray is not False:
        del model
        del regression_result

        if isarray[0] == 1:
            features_entities.remove('flow')
            m_gnx.pop(5)
            m_train.pop(5)
            spearmans_rank_correlation = update_spearmans_rank_correlation(spearmans_rank_correlation,
                                                                                            ["5_6", "5_11", "5_12"])

        if isarray[1] == 1:
            features_entities.remove('ab')
            m_gnx.pop(6)
            m_train.pop(6)
            spearmans_rank_correlation = update_spearmans_rank_correlation(spearmans_rank_correlation,
                                                                                            ["5_6", "6_11", "6_12"])

        if isarray[2] == 1:
            features_entities.remove('page_rank')
            m_gnx.pop(11)
            m_train.pop(11)
            spearmans_rank_correlation = update_spearmans_rank_correlation(spearmans_rank_correlation,
                                                                                            ["5_11", "6_11", "11_12"])

        if isarray[3] == 1:
            features_entities.remove('hierarchy_energy')
            m_gnx.pop(13)
            m_train.pop(13)
            spearmans_rank_correlation = update_spearmans_rank_correlation(spearmans_rank_correlation,
                                                                                            ["5_12", "6_12", "11_12"])

        print("features_entities:  ", features_entities)
        x, y, weight_of_edges_train, x_algo_order = MCDA_algos_service.matrix_builder(m_train, gnx_train)
        if isarray[4] == 1:
            model, regression_result = MCDA_algos_service.get_logistic_model_coefficients(x, x_algo_order, y, False,
                                                                                          regression_type)
        else:
            model, regression_result = MCDA_algos_service.get_logistic_model_coefficients(x, x_algo_order, y, True,
                                                                                          regression_type)

    regression_result['test_regression_prediction_scroe'] \
                                   = MCDA_algos_service.animalRegressionPredictionScroe(model, m_gnx, "animal_fight_20")
    regression_result['train_regression_prediction_scroe'] \
                                   = MCDA_algos_service.animalRegressionPredictionScroe(model, m_gnx, "animal_fight_80")
    return regression_result, spearmans_rank_correlation, features_entities


def update_spearmans_rank_correlation(spearmans_rank_correlation, index_array):
    for i in index_array:
        spearmans_rank_correlation[i] = (0, 0)
    return spearmans_rank_correlation


def remove_algo_disicion(regression_result, regression_type, is_removing_algos):
    #treshold=[(flow,ab,pagerank,hieracy energy,intercept]
    # sign_side=[sign_side flow ,sign_side ab, sign_side pagerank, sign_side hieracy energy,sign_side intercept]
    # were 1: {}< tresholds[0] and 0: {}> tresholds[0]
    if is_removing_algos:
        if regression_type is "regular":
            thresholds_ranges = [[-0.5, 0], [0, 1000], [0, 1000], [-0.5, 0.5], [-0.4, 0.4]]
            is_array = remove_algo_disicion_maker(regression_result, thresholds_ranges)
        if regression_type is "ridge":
            thresholds_ranges = [[-0.4, 0.4], [0.1, 1000], [-0.3, 0.5], [-0.1, 0.15], [0.4, 0.6]]
            is_array = remove_algo_disicion_maker(regression_result, thresholds_ranges)
        if regression_type is "lasso":
            thresholds_ranges = [[-1000.0, 1000], [0.2, 1000], [-1000.0, 1000], [-0.05, 0.05], [0.4, 0.6]]
            is_array = remove_algo_disicion_maker(regression_result, thresholds_ranges)
        return is_array
    else:
        return False

def remove_algo_disicion_maker(regression_result, thresholds):
    isarray = []
    # flow coef
    if all([regression_result.get(5) > thresholds[0][0], regression_result.get(5) < thresholds[0][1]]):
        isarray.append(0)
    else:
        isarray.append(1)
    # ab coef
    if all([regression_result.get(6) > thresholds[1][0], regression_result.get(6) < thresholds[1][1]]):
        isarray.append(0)
    else:
        isarray.append(1)
    # page rank coef
    if all([regression_result.get(11) > thresholds[2][0], regression_result.get(11) < thresholds[2][1]]):
        isarray.append(0)
    else:
        isarray.append(1)
    #hieracy energy coef
    if all([regression_result.get(13) > thresholds[3][0], regression_result.get(13) < thresholds[3][1]]):
        isarray.append(0)
    else:
        isarray.append(1)
    # intercept
    if all([regression_result.get('intercept') > thresholds[4][0], regression_result.get('intercept') < thresholds[4][1]]):
        isarray.append(0)
    else:
        isarray.append(1)
    return isarray


def create_logistic_model(regression_type, gnx_train, m_train, features_entities, isIntercept):
    #### Set the algo results to be ready for logistic regression
    x, y, weight_of_edges_train, x_algo_order = MCDA_algos_service.matrix_builder(m_train, gnx_train)

    #### Calculate the logistic regresion on the train set
    if regression_type is "ridge":
        model = linear_model.Ridge(alpha=.5, fit_intercept=isIntercept)
        model.fit(x, y)
        f = (model.intercept_, model.coef_)
        result = arrange_model_coef_results(features_entities, f)
        result.append(f[0])
    else:
        if regression_type is "lasso":
            model = linear_model.Lasso(alpha=0.1, fit_intercept=isIntercept)
            model.fit(x, y)
            f = (model.intercept_, model.coef_)
            result = arrange_model_coef_results(features_entities, f)
            result.append(f[0])
        else:
            model = LogisticRegression(fit_intercept=isIntercept)
            model.fit(x, y)
            f = (model.intercept_, model.coef_)
            result = regular_arrange_model_coef_results(features_entities, f)
            if isIntercept is True:
                result.append(f[0][0])  # for regressions with intercept
            else:
                result.append(f[0])     # for regressions without intercept
    return model, result


def arrange_model_coef_results(features_entities, f):
    result = []
    temp = dict(zip(features_entities, f[1]))
    if 'flow' in features_entities:
        result.append(temp['flow'])
    else:
        result.append(0.0)
    if 'ab' in features_entities:
        result.append(temp['ab'])
    else:
        result.append(0.0)
    if 'page_rank' in features_entities:
        result.append(temp['page_rank'])
    else:
        result.append(0.0)
    if 'hierarchy_energy' in features_entities:
        result.append(temp['hierarchy_energy'])
    else:
        result.append(0.0)
    return result

def regular_arrange_model_coef_results(features_entities, f):
    result = []
    temp = dict(zip(features_entities, f[1][0]))
    if 'flow' in features_entities:
        result.append(temp['flow'])
    else:
        result.append(0.0)
    if 'ab' in features_entities:
        result.append(temp['ab'])
    else:
        result.append(0.0)
    if 'page_rank' in features_entities:
        result.append(temp['page_rank'])
    else:
        result.append(0.0)
    if 'hierarchy_energy' in features_entities:
        result.append(temp['hierarchy_energy'])
    else:
        result.append(0.0)
    return result

####################################################################
   ##############     Adagio and Elo scoring      ###############
####################################################################

def calculate_adagio_and_elo_predection_score(fn):
    convert_train_data_from_DB_to_csv(fn)
    run_adagio_script()
    adagio_rank, elo_rank = read_ranks_results_from_adagio_script()
    return calculate_prediction_score(adagio_rank, elo_rank)

def convert_train_data_from_DB_to_csv(fn):
    animal_number = get_animal_number_in_train()
    train_matrix = create_train_matrix_as_2d_array(animal_number)
    convert_train_matrix_to_csv(train_matrix)

def get_animal_number_in_train():
    res = db_service.fetchoneQueryResult("SELECT MAX(`From_E`),MAX(`To_E`) FROM `animal_fight_100`;")
    return max(res[0], res[1])

def create_train_matrix_as_2d_array (animal_number):
    train_matrix_as_2d_array = [[x for x in range(0, int(animal_number) + 1)]]
    for i in range(1, int(animal_number)+1):
        animal_i_result_array = [i]
        for j in range(1, int(animal_number) + 1):
            res = db_service.fetchoneQueryResult("SELECT COUNT(8) FROM `animal_fight_80` "
                                                 "WHERE `From_E`="+str(i)+" AND`To_E`="+str(j)+";")
            animal_i_result_array.append(res[0])
        train_matrix_as_2d_array.append(animal_i_result_array)
    return train_matrix_as_2d_array

def convert_train_matrix_to_csv(train_matrix):
    a=numpy.asarray(train_matrix).astype(int)
    indir = "network-analysis\AnimalFights\A1\ShizukaMcDonald_Data\adagio_elo_calculation_folder"
    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\AnimalFights\A1\ShizukaMcDonald_Data\adagio_elo_calculation_folder")
    numpy.savetxt("train_animal_matrix.csv", a, delimiter=",")
    indir = "network-analysis"

def run_adagio_script():
    check_output(r"cd c:\Python34\Scripts && java -jar adagio.jar -folder C:\Users\Doron\workspace\MasterThasisProject\network-analysis\A1\ShizukaMcDonald_Data\adagio_elo_calculation_folder -preprocessing true -ranking top -ending csv", shell=True)

def read_ranks_results_from_adagio_script():
    indir = "network-analysis\AnimalFights\A1\ShizukaMcDonald_Data\adagio_elo_calculation_folder"
    adagio_rank = get_rank_result_from_file("train_animal_matrix.csv.adagio.ranks")
    elo_rank = get_rank_result_from_file("train_animal_matrix.csv.elo.ranks")
    indir = "network-analysis"
    return adagio_rank, elo_rank

def get_rank_result_from_file(file_name):
    indir = "network-analysis//AnimalFights//A1//ShizukaMcDonald_Data//adagio_elo_calculation_folder"
    rank = {}
    f = open(file_name, 'r')
    lines = f.read();
    lst = lines.split('\n')
    for x in [row.split('	') for row in lst]:
        if x[0] is not '':
            rank[int(round(float((x[0]))))] = int(x[1])
    return rank

def calculate_prediction_score(adagio_rank, elo_rank):
    adagio_prediction = 0
    elo_prediction = 0
    query_result = db_service.fetchallQueryResult("SELECT * FROM `animal_fight_20`;")
    for test_edge in query_result:
        is_vet_edge_in_adagio_rank = int(test_edge[0]) in adagio_rank.keys() and int(test_edge[1]) in adagio_rank.keys()
        is_vet_edge_in_elo_rank = int(test_edge[0]) in elo_rank.keys() and int(test_edge[1]) in elo_rank.keys()
        if is_vet_edge_in_adagio_rank:
            if int(adagio_rank[int(test_edge[0])]) < int(adagio_rank[int(test_edge[1])]):
                adagio_prediction += 1/len(query_result)
        if is_vet_edge_in_elo_rank:
            if elo_rank[int(test_edge[0])] < elo_rank[int(test_edge[1])]:
                elo_prediction += 1/len(query_result)
    return {"test_adagio_prediction": adagio_prediction, "test_elo_prediction": elo_prediction}

####################################################################
##############     partial table creationin db       ###############
####################################################################

def create_tables_for_calcs(table, train_set_size):
    #### Creating the 80% and 20% data files of the graph (the weight of the 20% is the count of the edge and the weight of the 80% is Xi-Xj)
    create_tables_service.create_animals_partial_tables(table, train_set_size)
    #### Creating the file of the all graph
    create_tables_service.create_animals_partial_tables(table, 100)

####################################################################
###     getting data from DB and insert to it the results       ####
####################################################################
def max_prediction_score():
    from_array = db_service.fetchallQueryResult("SELECT DISTINCT `From_E` FROM `animal_fight_20`;")
    to_array = db_service.fetchallQueryResult("SELECT DISTINCT `To_E` FROM `animal_fight_20`;")
    total = 0
    sum_max_ij = 0
    for i in from_array:
        for j in to_array:
            if j[0] > i[0]:
                k_i_j = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `animal_fight_20` WHERE "
                                                       "`From_E`='" + str(i[0]) + "' AND `To_E`='" + str(j[0])+"';")[0]
                k_j_i = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `animal_fight_20` WHERE "
                                                       "`From_E`='" + str(j[0]) + "' AND `To_E`='" + str(i[0])+"';")[0]
                sum_max_ij += max(k_i_j, k_j_i)
                sum_ks = k_i_j+k_j_i
                total += sum_ks

    return sum_max_ij/total

def table_details():
    num_of_rows_in_table = db_service.fetchoneQueryResult("SELECT COUNT(5) FROM `animal_fight`;")[0]
    number_of_comparisons = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM (SELECT DISTINCT * "
                                                                                        "FROM `animal_fight`)dt;")[0]
    table_max_prediction_score = max_prediction_score()
    return num_of_rows_in_table, number_of_comparisons, table_max_prediction_score

def insertResultToDB(fn, i, f, Spearmans_correlations, regression_type, date_time, features_entities_results, features_entities):

    insert_query = "INSERT INTO `animal_fight_results` VALUES ('" + str(date_time) + "','" + fn + "',"+str(i) + ","
    for algo in features_entities:
        insert_query += str(f.get(features.vertices_algo_dict.get(algo))) + ","

    insert_query += str(f.get("intercept"))+","+str(f.get("test_regression_prediction_scroe"))+","\
                    + str(f.get("train_regression_prediction_scroe")) + ",'" + str(regression_type) + "'," \
                    + str(f.get("david_prediction_train")) + "," + str(f.get("david_prediction_test")) + "," \
                    + str(f.get("test_adagio_prediction")) + "," + str(f.get("test_elo_prediction")) + ","\
                    + str(f.get("num_of_rows_in_table")) + "," + str(f.get("number_of_comparisons")) + "," \

    for i in features_entities:
        for j in features_entities:
            if features.vertices_algo_dict[i] < features.vertices_algo_dict[j]:
                insert_query += str(Spearmans_correlations.get(str(features.vertices_algo_dict[i]) + "_"
                                                               + str(features.vertices_algo_dict[j]))[0]) + ","

    insert_query += str(f.get("table_max_prediction_score")) + ',"'+str(features_entities_results)+'");'

    print(insert_query)
    db_service.executeInsertQuery(insert_query)

def insert_matrix_mgnx_into_db(m_gnx, date_time, fn, model, regression_type):
    for vet in m_gnx[11]:
        insert_query = "INSERT INTO `animal_fight_cretria_metrix` VALUES ('"+str(date_time)+"','"+str(fn)+"','"+str(vet)+"'"
        x = []
        for algo in m_gnx:
            insert_query += ","+"'"+str(m_gnx[algo][vet])+"'"
            x.append(m_gnx[algo][vet])
        insert_query += ",'"+str(model.decision_function([x])[0])+"','"+str(regression_type)+"');"
        print(insert_query)
        db_service.executeInsertQuery(insert_query)

def convert_to_array(lista):
    arr = []
    for a in lista:
        arr.append(lista[a])
    return arr

if __name__ == '__main__':
    main()