from services import db_service

def parameterInitializer():
    thresholds = {0.05, 0.0833, 0.1, 0.15, 0.1666, 0.2, 0.25, 0.5, 0.75, 1}
    date = {"23_05_2017", "11_03_2017", "12_12_2016", "25_01_2017", "16_04_2017"}
    return thresholds, date

def main():
    thresholds, date = parameterInitializer()
    for d_date in date:
        for threshold in thresholds :
            creatingGraph(threshold, d_date)
            print("The graph with threshold : "+str(threshold) + ", on the date: " + str(d_date) + " had been finished")

def creatingGraph(threshold, date):
    graph_table = "graph"+date+"t=" + str(threshold)
    createTable(graph_table)
    calculateForTable(date, graph_table, threshold)
    deleteEdgesFromAtoA(graph_table)

def createTable(graph_table):
    query = "CREATE TABLE `" + graph_table + "` (`From_E` text CHARACTER SET utf8, `To_E` text CHARACTER SET utf8) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
    db_service.executeCreateQuery(query)


def calculateForTable(detail_table_name, graph_table, threshold):
    debenture_detailes = setDebentureDetailes(detail_table_name)
    for i in range(0, len(debenture_detailes)):
        for j in range(0, len(debenture_detailes)):
            if j > i:
                query = calculateDebentureMatrix(i, j, threshold, graph_table, debenture_detailes)
                if query is not "":
                    db_service.executeInsertQuery(query)

def setDebentureDetailes(detail_table_name):
    debenture_details = []
    query_result = db_service.fetchallQueryResult("SELECT `debenture_name`,`debenture_number`,`interest`,`MACHAM`,`company_name`,`MALOT_rank`,`rank_number` " \
                               "FROM `" + str(detail_table_name) + "` INNER JOIN `ranking_midrog` ON `MALOT_rank` = `rank`;")
    for details_debenture_result in query_result:
        debenture_details.append(Debenture(details_debenture_result[0],
                                           details_debenture_result[1],
                                           details_debenture_result[2],
                                           details_debenture_result[3],
                                           details_debenture_result[4],
                                           details_debenture_result[5],
                                           details_debenture_result[6]))

    return debenture_details

def getDebenturesNumberList(detail_table_name):
    debentures_array = []
    query_result = db_service.fetchallQueryResult("SELECT `debenture_number` FROM " + str(detail_table_name) + ";")
    for res in query_result:
        debentures_array.append(res[0])
    return debentures_array


def calculateDebentureMatrix(i, j, threshold, graph_table, debenture_details):
    query = ""
    if all([debenture_details[i].rank_number == debenture_details[j].rank_number, debenture_details[j].rank_number is not 0]):
        if all([abs(debenture_details[i].macham - debenture_details[j].macham) < threshold,
                debenture_details[i].company_name is not debenture_details[j].company_name]):
            if debenture_details[i].interest - debenture_details[j].interest >= 0:
                query = "INSERT INTO `" + graph_table + "` VALUES ('" + debenture_details[j].company_name + "','"\
                        + debenture_details[i].company_name + "');"
                return query
            else:
                query = "INSERT INTO `" + graph_table + "` VALUES ('" + debenture_details[i].company_name + "','"\
                        + debenture_details[j].company_name + "');"
                return query
        else:
            return query
    else:
        return query

def deleteEdgesFromAtoA(graph_table):
    query = "DELETE FROM `" + graph_table + "` WHERE `From_E`=`To_E`;"
    db_service.executeDeleteQuery(query)


class Debenture(object):

    def __init__(self, debenture_name, debenture_number, interest, macham, company_name, malot_rank, rank_number):
        self.name = debenture_name
        self.id = debenture_number
        self.interest = interest
        self.macham = macham
        self.company_name = company_name
        self.malot_rank = malot_rank
        self.rank_number = rank_number

    def debentureProfit(self):
        return self.endValue-self.startValue

    def name(self):
        return self.name

    def id(self):
        return self.id

    def company_name(self):
        return self.company_name

    def malot_rank(self):
        return self.malot_rank

    def macham(self):
        return self.macham

    def interest(self):
        return self.interest

    def rank_number(self):
        return self.rank_number

if __name__ == '__main__':
    main()