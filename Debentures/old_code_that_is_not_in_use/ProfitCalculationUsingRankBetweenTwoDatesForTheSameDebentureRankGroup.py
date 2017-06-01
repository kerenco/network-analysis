import mysql.connector
import time
from datetime import datetime


def main():
    start_dates = {"12_12_2016","25_01_2017"}
    end_dates = {"25_01_2017","11_03_2017"}
    tresholds = {0.05,0.0833,0.1,0.15,0.1666,0.2,0.25}
    intercept = {True,False}
    regression_types = {"ridge","lasso","regular"}
    for start_date in start_dates:
        for end_date in end_dates:
            if(start_date is not end_date):
                for treshold in tresholds:
                    for inter in intercept:
                        for regression_type in regression_types:
                            ##########setRegressionDataInDB(start_date,treshold,inter) ### now we set the result fot this test==>
                             #<==  while running part3_Debentures_Scoring.py one each treshold in each date and removing the remark at line 36
                            CalculateNumberOfDebenturePerCompany(start_date)
                            profit , num_of_comparisons = CalculateProfit(start_date,end_date, treshold, inter, regression_type)
                            print ("profit is :       ", profit)
                            setProfitInDB(start_date,end_date, treshold, inter, profit, num_of_comparisons, regression_type)


####################################################################
####################################################################
  #######               Set Data Stage                 ###########
####################################################################
####################################################################
#def setRegressionDataInDB(start_date,treshold,inter):
#    results = getRegressionScores(start_date,treshold,inter)
#    setScoresInDB(results)

"todo..."



####################################################################
####################################################################
#######            Profit Calculation Stage              ###########
####################################################################
####################################################################


def CalculateProfit(start_date,end_date, treshold, intercept, regression_type):
    profit=0
    num_of_comparisons = 0
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    companys_numbers = getCompanysNumbersList(start_date, treshold)

    for i in companys_numbers:
        profit_of_company_i=0 #for investigation how much each company add to the total profit
        i_query = "SELECT `vet_model_score` FROM `debenture_cretria_metrix_all_graph` WHERE `treshold`="+str(treshold)+\
                  " AND `data_date`='"+start_date+"' AND `intercept`='"+str(intercept)+"' AND `vetrex`="+str(i)+\
                  " AND `regression_type`='"+ str(regression_type) + "';"
        cursor.execute(i_query)
        i_rank= cursor.fetchone()[0]
        cnx.close
        for j in companys_numbers:
            time.sleep(0.03)

            j_query = "SELECT `vet_model_score` FROM `debenture_cretria_metrix_all_graph` WHERE `treshold`=" \
                      + str(treshold) + " AND `data_date`='" + start_date + "' AND `intercept`='" + str(intercept)\
                      + "' AND `vetrex`=" + str(j) + " AND `regression_type`='"+ str(regression_type) + "';"
            cursor.execute(j_query)
            j_rank = cursor.fetchone()[0]
            is_companies_have_the_same_midrog_rank = getCompanyMidrogRank(i ,start_date) is getCompanyMidrogRank(j ,start_date)

            if (i_rank > j_rank):
                profit_i_j = getProfitOfInvestInHighRankAginstLowRank(i, j, start_date, end_date, is_companies_have_the_same_midrog_rank)
            else:
                profit_i_j = getProfitOfInvestInHighRankAginstLowRank(j, i, start_date, end_date, is_companies_have_the_same_midrog_rank)
            profit_of_company_i += profit_i_j

            time.sleep(0.03)
            if all([j > i,is_companies_have_the_same_midrog_rank]):
                profit += profit_i_j
                num_of_comparisons += 1

            if (num_of_comparisons != 0):
                print("profit so for: ",profit," | i=",i," |j=",j," | start_date=",start_date," |end_date=",end_date,
                        " |treshold=",treshold," |intercept=",intercept," | profit_of_company_i=",profit_of_company_i,
                        " | total_num_of_comparisons=",num_of_comparisons," | annual interest leverage: ",(profit*4)/num_of_comparisons)

        insert_company_profit_to_db(i, profit_of_company_i, start_date, end_date, treshold, intercept, regression_type)

    return profit , num_of_comparisons


def getProfitOfInvestInHighRankAginstLowRank (high_rank_company,low_rank_company,start_date,end_date,is_companies_have_the_same_midrog_rank):
    if (is_companies_have_the_same_midrog_rank):
        #print("high: ",high_rank_company)
        profit_from_high_rank= CalculateProfitOfCompany(high_rank_company,start_date,end_date)
        #print("low: ",low_rank_company)
        profit_from_low_rank= CalculateProfitOfCompany(low_rank_company,start_date,end_date)
        #print (high_rank_company,"<=high_rank_company  low_rank_company=>", low_rank_company," | ",profit_from_high_rank-profit_from_low_rank)
        return profit_from_high_rank-profit_from_low_rank
    else:
        return 0

def getCompanyMidrogRank(company,start_date):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    midrog_value_query="SELECT `rank_number` FROM `ranking_midrog`" \
                            "WHERE (SELECT `MALOT_rank` FROM `" + str(start_date) +"`" \
                                "WHERE (SELECT `company_Name` FROM `company_key` " \
                                    "WHERE `num`=" + str(company) + ")" \
                                    "=`company_name` GROUP BY company_Name)" \
                                "=`rank`;"
    cursor.execute(midrog_value_query)
    midrog_rank = cursor.fetchone()[0]
    return midrog_rank

def CalculateProfitOfCompany(company,start_date,end_date):
    debenture_numbers_list=[]
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    count_query = "SELECT COUNT(8) FROM `"+start_date+"`" \
                                                      " WHERE (SELECT `company_Name` FROM `company_key` WHERE `num`="+str(company)+")=`company_name`;"
    cursor.execute(count_query)
    num=cursor.fetchone()[0]
    debentures_numbers_query = "SELECT `debenture_number` FROM `"+start_date+"`" \
                                                                             " WHERE (SELECT `company_Name` FROM `company_key` WHERE `num`="+str(company)+")=`company_name`;"
    #print("debentures_numbers_query: ",debentures_numbers_query)
    cursor.execute(debentures_numbers_query)
    for i in range (0,num):
        debenture_num = cursor.fetchone()[0]
        debenture_numbers_list.append(debenture_num)
    #print("debenture_numbers_list: ",debenture_numbers_list)
    company_profit = 0
    for debenture_number in debenture_numbers_list:
        company_profit += debentureProfitCalculator(debenture_number,start_date,end_date)
        #print("debentur: ",debenture_number," | ",num,"| company profit is: ",company_profit,  )
    cnx.close

    return company_profit


####################################################################
    #######    calculating specific debenture profit   #######
####################################################################

def debentureProfitCalculator(debenture_number,start_date,end_date):
    part_of_investment_in_debenture = getNumberOfDebenturesPerCompany(debenture_number,start_date)
    end_value, start_value = getDebentureProfitInTimePeriod(debenture_number,start_date,end_date)
    result = ((100*part_of_investment_in_debenture) / start_value) * (end_value-start_value)
    #print(result)
    return result


def getNumberOfDebenturesPerCompany(debenture_number,start_date):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    query1 = "SELECT `company_name` FROM `"+start_date+"` WHERE `debenture_number`="+str(debenture_number)+";"
    cursor.execute(query1)
    company_name=cursor.fetchone()
    query2 = "SELECT `number_of_debentuers` FROM `company_key` WHERE `company_Name`='"+company_name[0]+"';"
    cursor.execute(query2)
    part_of_investment_in_debenture = (1/cursor.fetchone()[0])

    return part_of_investment_in_debenture


def getDebentureProfitInTimePeriod(debenture_number,start_date,end_date):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    start_value_query = "SELECT `end_day_value`,`MACHAM`,`interest` FROM `"+start_date+"` WHERE `debenture_number`="+str(debenture_number)+";"
    cursor.execute(start_value_query)
    start_detailes=cursor.fetchone()
    start_value=start_detailes[0]
    end_value_query = "SELECT `end_day_value` FROM `"+end_date+"` WHERE `debenture_number`="+str(debenture_number)+";"
    cursor.execute(end_value_query)
    #handling the case where the debenture life allready end befor the end date
    try:
        end_value = cursor.fetchone()[0]
    except:
        end_value = start_detailes[0] * (1 + start_detailes[1] * start_detailes[2]/100) #######we should also need to add the no risk interest!!!
    cnx.close

    return end_value,start_value

####################################################################
####### calculating the number of debenture per company  ###########
####################################################################

def CalculateNumberOfDebenturePerCompany(date):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    x_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    num_of_companies_query = 'SELECT COUNT(8) FROM (SELECT DISTINCT `company_name` FROM `'+str(date)+'`)df; '
    print(num_of_companies_query)
    cursor.execute(num_of_companies_query)
    num_of_companies = cursor.fetchone()
    query_count = 'SELECT `company_name`,COUNT(8) FROM `'+date+'` GROUP BY `company_name`;'
    cursor.execute(query_count)
    for i in range (0,num_of_companies[0]):
        result = cursor.fetchone()
        #print(result)
        update_query = "UPDATE `company_key` SET `number_of_debentuers`="+str(result[1])+\
                       " WHERE `company_Name`='"+result[0]+"';"
        #print (update_query)
        try:
            x_cnx.cursor(buffered=True).execute(update_query)  # Execute the SQL command
            x_cnx.commit()  # Commit your changes in the database
        except:
            x_cnx.rollback()  # Rollback in case there is any error
    cnx.close


def getCompanysNumbersList(start_date, treshold):
    companys_list=[]
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    num_of_companys_query = "SELECT COUNT(8) FROM (SELECT * FROM `debenture_cretria_metrix_all_graph` " \
                            "WHERE `treshold` = "+str(treshold)+" AND `data_date` = '"+start_date+"' GROUP BY `vetrex`)df;"
    cursor.execute(num_of_companys_query)
    num_of_companys = cursor.fetchone()[0]
    companys_numbers_query = "SELECT `vetrex` FROM `debenture_cretria_metrix_all_graph` " \
                             "WHERE `treshold`="+str(treshold)+" AND `data_date`='"+start_date+"';"
    cursor.execute(companys_numbers_query)
    for i in range (0,num_of_companys):
        companys_list.append(cursor.fetchone()[0])
    cnx.close

    return companys_list


####################################################################
####################################################################
  #######       insert result in to DB Stage           ###########
####################################################################
####################################################################

def setProfitInDB(start_date, end_date, treshold, intercept, profit, num_of_comparisons, regression_type):
    date_time = datetime.now()
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    insert_query = "INSERT INTO `profit_results` VALUES" \
                   "('"+str(date_time)+"','"+str(start_date)+"','"+str(end_date)+"','"+str(treshold)\
                   +"','"+str(intercept)+"','"+str(profit)+"','"+str(num_of_comparisons)\
                   + "','" + str(regression_type) +"','profit when comparing companies with the same Midrog rate');"
    print ("insert_query: ",insert_query)
    try:
        cursor.execute(insert_query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error

def insert_company_profit_to_db(i, profit_of_company_i, start_date, end_date, treshold, intercept, regression_type):
    date_time = datetime.now()
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    insert_query = "INSERT INTO `profit_company_results` VALUES" \
                   "('" + str(date_time) + "','" + str(start_date) + "','" + str(end_date) + "','" + str(treshold) \
                   + "','" + str(intercept) + "','" + str(i) + "','" + str(profit_of_company_i) \
                   + "','" + str(regression_type) + "','profit when comparing companies with the same Midrog rate');"
    print("insert_query: ", insert_query)
    try:
        cursor.execute(insert_query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error


if __name__ == '__main__':
    main()