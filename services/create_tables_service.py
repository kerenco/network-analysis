import os
from services import db_service


def tables_creator(threshold, train_set_size, date):
    truncate_tables_in_db()
    #### Creating the 80% and 20% data files of the graph (the weight of the 20% is the count of the edge and the weight of the 80% is Xi-Xj)
    create_partial_tables(threshold, train_set_size,date)
    #### Creating the file of the all graph
    create_partial_tables(threshold, 100, date)

def truncate_tables_in_db():
    for table in ["`debentures_0`", "`debentures_20`", "`debentures_80`", "`debentures_100`"]:
        db_service.executeTruncateQuery(table)

def create_partial_tables(threshold, part_for_train, date):
    db_table_name = "graph"+date+"t="+str(threshold)
    vetrx_list_train, vetrx_list_test = createVetrexList(db_table_name, part_for_train)

    text_file_train = open(db_table_name+'_'+str(part_for_train)+'%.txt', "w")
    query_arr1 = []
    for vet in vetrx_list_train:
        #inserting the data to db for davids rank
        query = 'INSERT INTO `debentures_' + str(part_for_train) + '` VALUES (' + str(vet[0]) + ',' + str(vet[1]) \
                + ');'
        query_arr1.append(query)
        #creating the file to the logistic regression
        to = vetrx_list_train.count([vet[0], vet[1]])
        to_revrse = vetrx_list_train.count([vet[1], vet[0]])
        if(to-to_revrse>0):
            text_file_train.writelines(str(vet[0]) + ',' + str(vet[1]) + ',' + str((to-to_revrse)/(to+to_revrse))
                                       + '\n')
    text_file_train.writelines('-1,-1')
    text_file_train.close()
    db_service.executeInsertQuerysArray(query_arr1)
    text_file_test = open(db_table_name + "_" + str((100-part_for_train)) + '%.txt', "w")
    query_arr2 = []
    for vet in vetrx_list_test:
        #inserting the data to db for davids rank
        query = 'INSERT INTO `debentures_'+str(100-part_for_train)+'` VALUES ('+str(vet[0])+','+str(vet[1])\
                    + ');'
        query_arr2.append(query)
        #without WEIGHT  text_file_test.writelines(str(vet[0]) + ',' + str(vet[1])+ ',' + str(1)+ '\n')
        text_file_test.writelines(str(vet[0]) + ',' + str(vet[1]) + ',' + str(vet[2]) + '\n')
    text_file_test.writelines('-1,-1')
    text_file_test.close()
    db_service.executeInsertQuerysArray(query_arr2)


def createVetrexList(db_table_name, value):
    vetrx_list_train = list()
    vetrx_list_test = list()
    cnx = db_service.createCNX()
    cursor = cnx.cursor(buffered=True)
    companies_keys = setCompanyKeysList()
    query = "SELECT * FROM `" + db_table_name + "` ORDER BY RAND();"
    cursor.execute(query)
    for i in range(0, int(value * cursor.rowcount / 100)):
        res = cursor.fetchone()
        vetrx_list_train.append([companies_keys[res[0]], companies_keys[res[1]]])
    for i in range(int(value * cursor.rowcount / 100) + 1, cursor.rowcount):
        res = cursor.fetchone()
        counter = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `" + db_table_name +
                                                 "` WHERE `From_E`= '" + res[0] + "' AND `To_E`= '" + res[1] + "';")[0]
        vetrx_list_test.append([companies_keys[res[0]], companies_keys[res[1]], counter])
        # without WEIGHT  vetrx_list_test.append([from_num_test, to_num_test])
    cnx.close()
    return vetrx_list_train, vetrx_list_test

def setCompanyKeysList():
    companies_keys = {}
    query_result = db_service.fetchallQueryResult("SELECT * FROM `company_key`;")
    for res in query_result:
        companies_keys[res[0]] = res[1]
    return companies_keys

def create_animals_partial_tables(table, part_for_train):

    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\AnimalFights")
    table_length = db_service.fetchoneQueryResult("SELECT COUNT(*) FROM `" + table + "`;")[0]
    vetrx_list_train, vetrx_list_test = createAnimalVetrexList(table, table_length, part_for_train)
    text_file_train = open(table+'_'+str(part_for_train)+'%.txt', "w")
    query_arr1 = []
    for vet in vetrx_list_train:
        #inserting the data to db for davids rank
        query_arr1.append('INSERT INTO `'+table+'_'+str(part_for_train) +
                                          '` VALUES ('+str(vet[0])+','+str(vet[1]) + ');')
        #creating the file to the logistic regression
        to = vetrx_list_train.count([vet[0], vet[1]])
        to_revrse = vetrx_list_train.count([vet[1], vet[0]])
        if to-to_revrse > 0:
            text_file_train.writelines(str(vet[0]) + ',' + str(vet[1]) + ',' + str((to-to_revrse)/(to+to_revrse)) + '\n')
    text_file_train.writelines('-1,-1')
    text_file_train.close()
    db_service.executeInsertQuerysArray(query_arr1)

    text_file_test = open(table + "_" + str((100 - part_for_train)) + '%.txt', "w")
    query_arr2 = []
    for vet in vetrx_list_test:
        #inserting the data to db for davids rank
        query_arr2.append('INSERT INTO `'+table+'_' + str(100 - part_for_train) +
                                          '` VALUES (' + str(vet[0]) + ',' + str(vet[1]) + ');')
        #creating the file to the logistic regression
        #without WEIGHT  text_file_test.writelines(str(vet[0]) + ',' + str(vet[1])+ ',' + str(1)+ '\n')
        text_file_test.writelines(str(vet[0]) + ',' + str(vet[1]) + ',' + str(vetrx_list_test.count([vet[0], vet[1]]))
                                  + '\n')

    text_file_test.writelines('-1,-1')
    text_file_test.close()
    db_service.executeInsertQuerysArray(query_arr2)


def createAnimalVetrexList(db_table_name, table_length, value):
    cnx = db_service.createCNX()
    cursor = cnx.cursor(buffered=True)
    vetrx_list_train = list()
    vetrx_list_test = list()
    query = "SELECT * FROM `" + db_table_name + "` ORDER BY RAND();"
    cursor.execute(query)
    for i in range(0, int(value*table_length/100)):
        res = cursor.fetchone()
        vetrx_list_train.append([res[0], res[1]])

    for i in range(int(value*table_length/100) + 1, table_length):
        res = cursor.fetchone()
        counter = db_service.executeInsertQuery("SELECT COUNT(*) FROM `" + db_table_name
                                                + "` WHERE `From_E`= '" + str(res[0]) +
                                                "'AND `To_E`= '" + str(res[1]) + "';")
        vetrx_list_test.append([res[0], res[1], counter])
    cnx.close()
    return vetrx_list_train, vetrx_list_test