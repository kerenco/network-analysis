from datetime import datetime
from services import db_service

def parameterInitializer():
    start_dates = {"11_03_2017", "16_04_2017"} #{"25_01_2017",  "12_12_2016"} #
    end_dates = {"16_04_2017", "23_05_2017"}#{"25_01_2017", "11_03_2017", "16_04_2017", "23_05_2017"} #
    thresholds = {0.05, 0.0833, 0.1, 0.15, 0.1666, 0.2, 0.25, 0.5, 0.75, 1}
    intercept = {True, False}
    regression_types = {"ridge", "lasso", "regular"}
    rank_method = {"regression", "davids", "aph_1"}
#    dates_keys = setDateKey(start_dates, end_dates)
    return start_dates, end_dates, thresholds, intercept, regression_types, rank_method

def main():
    start_dates, end_dates, thresholds, intercept, regression_types, rank_method = parameterInitializer()
    for start_date in start_dates:
        for end_date in end_dates:
            if start_date is not end_date:
                for threshold in thresholds:
                    for r_method in rank_method:
                        if r_method is not "regression":
                            profitCalculator(start_date, end_date, threshold, None, None, r_method)
                        else:
                            for regression_type in regression_types:
                                for inter in intercept:
                                    profitCalculator(start_date, end_date, threshold, inter, regression_type, r_method)

def profitCalculator(start_date, end_date, threshold, inter, regression_type, r_method):
    companies_details = companiesAndDebenturesSetter(start_date, end_date, threshold, inter, regression_type, r_method)
    if r_method is not "regression":
        profit, num_of_comparisons = CalculateProfit(companies_details, start_date, end_date, threshold, inter,
                                                     r_method)
        print(" | start_date=", start_date, " | end_date=", end_date, " | r_method= ", r_method,
              " | threshold=", threshold, " | profit=", profit,
              " | total_num_of_comparisons=", num_of_comparisons, " | interest leverage: ", profit / num_of_comparisons)
        setProfitInDB(start_date, end_date, threshold, inter, profit, num_of_comparisons, r_method)

    else:
        profit, num_of_comparisons = CalculateProfit(companies_details, start_date, end_date, threshold, inter,
                                                     regression_type)
        print(" | start_date=", start_date, " | end_date=", end_date, " | regression type= ", regression_type,
              " | threshold=", threshold, " | intercept=", inter, " | profit=", profit,
              " | total_num_of_comparisons=", num_of_comparisons, " | interest leverage: ", profit / num_of_comparisons)
        setProfitInDB(start_date, end_date, threshold, inter, profit, num_of_comparisons, regression_type)

####################################################################
#######               Set Data Stage                     ###########
####################################################################

def companiesAndDebenturesSetter(start_date, end_date, threshold, intercept, regression_type, r_method):
    company_array = {}
    companys_numbers = getCompanysNumbersList(start_date, threshold)
    for i in companys_numbers:
        company_name = companyName(i)
        num_company_debentures = numCompanyDebentures(start_date, company_name)
        debentures_array = getDebentures_array(i, start_date, end_date)
        i_rank = getCompanyRank(start_date, threshold, intercept, regression_type, i, r_method)
        i_midrog_rate = getCompanyMidrogRank(i, start_date)

        company_array[i] = Company(company_name,
                                   i,
                                   num_company_debentures,
                                   debentures_array,
                                   i_rank,
                                   i_midrog_rate)
    return company_array

def companyName(company_num):
    query_company_name = "SELECT `company_Name` FROM `company_key` WHERE `num`=" + str(company_num) + ";"
    result = db_service.fetchoneQueryResult(query_company_name)
    return result[0]

def numCompanyDebentures(date, company_name):
    query_count = 'SELECT `company_name`,COUNT(8) FROM `'+date+'` WHERE `company_name`="'+str(company_name) +\
                  '" GROUP BY `company_name`;'
    result = db_service.fetchoneQueryResult(query_count)
    return result[1]

def getDebentures_array(i, start_date, end_date):
    array = []
    query_debentures_of_company = "SELECT `debenture_name`,`debenture_number`,`end_day_value`,`MACHAM`,`interest` " \
                                  "FROM `"+str(start_date)+"` WHERE (SELECT `company_Name` FROM `company_key` " \
                                                                        "WHERE `num`=" + str(i) + ")=`company_name`;"
    debentures_of_company = db_service.fetchallQueryResult(query_debentures_of_company)
    for details_start_day_result in debentures_of_company:
        end_value_result = getEndDayValue(details_start_day_result, end_date)
        array.append(Debenture(details_start_day_result[0],
                               details_start_day_result[1],
                               details_start_day_result[2],
                               end_value_result,
                               details_start_day_result[3],
                               details_start_day_result[4]))
    return array

def getEndDayValue(details_start_day_result, end_date):
    end_value_query = "SELECT `end_day_value` FROM `" + str(end_date) + "` WHERE `debenture_number`=" + str(
                         details_start_day_result[1]) + ";"
    try:
        end_value_result = db_service.fetchoneQueryResult(end_value_query)[0]
    except:
        end_value_result = details_start_day_result[2] * (1 + (details_start_day_result[4] / 100)) ** \
                        details_start_day_result[3]#######we should also need to add the no risk interest!!! copons?
    return end_value_result

def getCompanyRank(start_date, threshold, intercept, regression_type, i, r_method):
    if r_method is "regression":
        i_query = "SELECT `" + r_method + "_score_results` FROM `debenture_cretria_metrix_all_graph` WHERE `threshold`=" + str(threshold) +\
                  " AND `data_date`='" + start_date + "' AND `intercept`='" + str(intercept) + "' AND `vetrex`=" + str(i) +\
                  " AND `regression_type`='" + str(regression_type) + "';"
    else:
        i_query = "SELECT `" + r_method + "_score_results` FROM `debenture_cretria_metrix_all_graph` WHERE `threshold`=" + str(threshold) +\
                  " AND `data_date`='" + start_date + "' AND `vetrex`=" + str(i) + " GROUP BY `vetrex`;"
    i_rank = db_service.fetchoneQueryResult(i_query)[0]
    return i_rank

def getCompanyMidrogRank(company, start_date):
    midrog_value_query = "SELECT `rank_number` FROM `ranking_midrog`" \
                            "WHERE (SELECT `MALOT_rank` FROM `" + str(start_date) + "`" \
                                        "WHERE (SELECT `company_Name` FROM `company_key` " \
                                                   "WHERE `num`=" + str(company) + ")=`company_name` " \
                                                   "GROUP BY company_Name)=`rank`;"
    result = db_service.fetchoneQueryResult(midrog_value_query)
    return result[0]

####################################################################
#######            Profit Calculation Stage              ###########
####################################################################

def CalculateProfit(companies_details, start_date, end_date, threshold, intercept, rank_method):
    profit = 0
    num_of_comparisons = 0
    for i in companies_details:
        profit_of_company_i = 0 #for investigation how much each company add to the total profit
        i_rank = companies_details.get(i).rank_value
        for j in companies_details:
            j_rank = companies_details.get(j).rank_value
            is_companies_have_the_same_midrog_rank = companies_details.get(i).rank is companies_details.get(j).rank
            if i_rank > j_rank:
                profit_i_j = companies_details.get(i).companyProfit() - companies_details.get(j).companyProfit()
            else:
                profit_i_j = companies_details.get(j).companyProfit() - companies_details.get(i).companyProfit()

            if all([j > i, is_companies_have_the_same_midrog_rank]):
                profit_of_company_i += profit_i_j
                profit += profit_i_j
                num_of_comparisons += 1

        insert_company_profit_to_db(i, profit_of_company_i, start_date, end_date, threshold, intercept, rank_method)

    return profit, num_of_comparisons

####################################################################
####### calculating the number of debenture per company  ###########
####################################################################

def getCompanysNumbersList(start_date, threshold):
    companys_list = []
    companys_numbers_query = "SELECT DISTINCT `vetrex` FROM `debenture_cretria_metrix_all_graph` " \
                             "WHERE `threshold`=" + str(threshold) + " AND `data_date`='" + start_date + "';"
    companys_numbers = db_service.fetchallQueryResult(companys_numbers_query)
    for i in companys_numbers:
        companys_list.append(i[0])
    return companys_list

####################################################################
  #######       insert result in to DB Stage           ###########
####################################################################

def setProfitInDB(start_date, end_date, threshold, intercept, profit, num_of_comparisons, rank_method):
    date_time = datetime.now()
    insert_query = "INSERT INTO `profit_results` VALUES" \
                   "('" + str(date_time)+"','" + str(start_date)+"','" + str(end_date) + "','" + str(threshold)\
                   + "','" + str(intercept)+"','" + str(profit)+"','" + str(num_of_comparisons)\
                   + "','" + str(rank_method) + "','profit when comparing companies with the same Midrog rate');"
    db_service.executeInsertQuery(insert_query)

def insert_company_profit_to_db(i, profit_of_company_i, start_date, end_date, threshold, intercept, rank_method):
    date_time = datetime.now()
    insert_query = "INSERT INTO `profit_company_results` VALUES" \
                   "('" + str(date_time) + "','" + str(start_date) + "','" + str(end_date) + "','" + str(threshold) \
                   + "','" + str(intercept) + "','" + str(i) + "','" + str(profit_of_company_i) \
                   + "','" + str(rank_method) + "','profit when comparing companies with the same Midrog rate');"
    db_service.executeInsertQuery(insert_query)

def setDateKey(start_dates, end_dates):
    date_key = {}
    for i in start_dates:
        if len(date_key.keys()) == 0:
            date_key[i] = 1
        else:
            date_key[i] = (len(date_key.keys()) + 1)
    for j in end_dates:
        if j not in date_key:
            date_key[j] = (len(date_key.keys()) + 1)
    return date_key

class Company(object):

    def __init__(self, company_name, company_number, num_company_debentures,
                 company_debentures, company_rank_value, medrogRank):
        self.name = company_name
        self.num = company_number
        self.number_of_debentures = num_company_debentures
        self.debentures_array = company_debentures
        self.rank_value = company_rank_value
        self.rank = medrogRank

    def companyProfit(self):
        company_profit = 0
        for debenture in self.debentures_array:
            company_profit += (100 / (self.number_of_debentures * debenture.startValue)) * debenture.debentureProfit()
        return company_profit

    def name(self):
        return self.name

    def num(self):
        return self.num

    def number_of_debentures(self):
        return self.number_of_debentures

    def debentures_array(self):
        return self.debentures_array

    def rank_value(self):
        return self.rank_value

    def rank(self):
        return self.rank

class Debenture(object):

    def __init__(self, debenture_name, debenture_number, debenture_start_value, debentuer_end_vlue, macham, interest):
        self.name = debenture_name
        self.id = debenture_number
        self.startValue = debenture_start_value
        self.endValue = debentuer_end_vlue
        self.macham = macham
        self.interest = interest


    def debentureProfit(self):
        return self.endValue-self.startValue

    def name(self):
        return self.name

    def id(self):
        return self.id

    def startValue(self):
        return self.startValue

    def endValue(self):
        return self.endValue

    def macham(self):
        return self.macham

    def interest(self):
        return self.interest

if __name__ == '__main__':
    main()