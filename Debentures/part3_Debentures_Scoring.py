from services import create_tables_service
from services import MCDA_algos_service
from services import db_service
from datetime import datetime

def parameter_initializer():
    date = {"12_12_2016", "25_01_2017", "16_04_2017", "11_03_2017", "23_05_2017"}
    thresholds = {0.05, 0.0833, 0.1, 0.15, 0.1666, 0.2, 0.25, 0.5, 0.75, 1}
    intercept = {True, False}
    features_list_for_matrix_cretrias = ['flow', 'ab', 'page_rank', 'hierarchy_energy']
    number_of_iterations = 5
    is_into_debenture_cretria_metrix_all_graph = True ##True for ProfitCalculationUsingRankBetweenTwoDates.py
    regression_types = {"ridge", "lasso", "regular"}
    return date, thresholds, intercept, features_list_for_matrix_cretrias, number_of_iterations,\
           is_into_debenture_cretria_metrix_all_graph, regression_types

def main():
    dates, thresholds, intercept, features_list_for_matrix_cretrias, number_of_iterations,\
                                is_into_debenture_cretria_metrix_all_graph, regression_types = parameter_initializer()

    for date in dates:
        for threshold in thresholds:
            for i in range(0, number_of_iterations):
                print(">>>>>>> date:", date, " |threshold:", threshold, " | fetures_list_for_matrix_cretrias:",
                                    features_list_for_matrix_cretrias, " | iteration:", i, " <<<<<<<<<<<<")

                #creating the cretrias matrix for all the vetreces
                create_tables_service.tables_creator(threshold, 80, date)
                gnx_train, m_train, x, x_algo_order, y, weight_of_edges_train, gnx, m_gnx, gnx_test, m_test =\
                      MCDA_algos_service.calc_cretria_metrexes(threshold, 80, date, features_list_for_matrix_cretrias)

                #APH algorithems
                aph_1_2_3_scores = MCDA_algos_service.run_aph_algos(gnx_test, m_gnx)

                #Davids algorithems
                algos_prediction_results = MCDA_algos_service.davids("debentures_80", "debentures_100", "debentures_20")
                algos_prediction_results.update(aph_1_2_3_scores)
                algos_prediction_results.update({"threshold": threshold})

                #Regression algorithem
                for regression_type in regression_types:
                    for inter in intercept:
                        f, model = MCDA_algos_service.calc_logistic_score(x, x_algo_order, y, inter, m_gnx,
                                                                                gnx_test, gnx_train, regression_type)
                        f.update(algos_prediction_results)
                        print("F: ", f)
                        date_time = datetime.now()
                        insertResultToDB(f, date, i, date_time, regression_type)

                        #For the part4 (Profit Calculations)- insert the all ranks of the full graph to DB
                        if all([is_into_debenture_cretria_metrix_all_graph is True, i == 0]):
                            aph_1_score_results = MCDA_algos_service.aph_1(m_gnx)
                            davids_score_results = MCDA_algos_service.calc_davids_score("debentures_100")
                            insertMatrix_mgnx_IntoDB(date, threshold, inter, m_gnx, gnx, date_time, regression_type,
                                                     aph_1_score_results, davids_score_results)


def insertResultToDB(f, date, i, date_time, regression_type):
    insert_query = "INSERT INTO `debenture_results` VALUES ('"+str(f.get('threshold'))+"','"+str(date)+"','"\
                   + str(date_time)+"','"+str(i)+"',"+str(f.get(5))+","+str(f.get(6))+","+str(f.get(11))+"," \
                   + str(f.get(13))+","+str(f.get('intercept'))+","+str(f.get('prediction_result'))+"," \
                   + str(f.get('score_the_train_data_prediction')) + "," + str(f.get('max_score_train_data_prediction'))\
                   + "," + str(f.get('max_score_test_data_prediction')) + "," + str(f.get('aph_1'))+","\
                   + str(f.get('aph_2')) + "," + str(f.get('aph_3')) + "," + str(f.get('david_prediction_test')) + ","\
                   + str(f.get('david_prediction_train'))+",'"+str(regression_type) + "');"
    print(insert_query)
    db_service.executeInsertQuery(insert_query)


def insertMatrix_mgnx_IntoDB(date, threshold, intercept, m_gnx, gnx, date_time, regression_type, aph_1_score_results ,davids_score_results):
    x, y, wights, x_algo_order = MCDA_algos_service.matrix_builder(m_gnx, gnx)
    model, model_coefficients = MCDA_algos_service.get_logistic_model_coefficients(x, x_algo_order, y, intercept, regression_type)
    for vet in m_gnx[11]:
        insert_query = "INSERT INTO `debenture_cretria_metrix_all_graph` VALUES ('"+str(date)+"','"+str(date_time)+"',"\
                      + str(threshold)+",'"+str(intercept)+"',"+str(vet)
        matrix = []
        for algo in m_gnx:
            insert_query += ","+str(m_gnx[algo][vet])
            matrix.append(m_gnx[algo][vet])
        insert_query += ","+str(model.decision_function([matrix])[0])+",'"+str(regression_type) +\
                        "',"+str(aph_1_score_results[vet])+","+str(davids_score_results[vet])+");"
        print(insert_query)
        db_service.executeInsertQuery(insert_query)


if __name__ == '__main__':
    main()

