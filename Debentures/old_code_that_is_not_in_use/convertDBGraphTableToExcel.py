import mysql.connector
import xlsxwriter


def main():
    graph_db_table = "graph12_12_2016t=0.25"
    start_number_of_companies=94
    end_number_of_companies =97
    #createing the excel file
    workbook = xlsxwriter.Workbook(graph_db_table)
    worksheet = workbook.add_worksheet(graph_db_table)
    StartEndCompanies=addCompaniesNames(graph_db_table,worksheet,start_number_of_companies,end_number_of_companies)
    setValuesInMatrix(graph_db_table, worksheet,StartEndCompanies)


def addCompaniesNames(graph_db_table,worksheet,start_number_of_companies,end_number_of_companies):
    StartCompanigs=setStartCompanigs(graph_db_table,worksheet,start_number_of_companies)
    EndCompanigs=setEndCompanigs (graph_db_table,worksheet,end_number_of_companies)
    #print ([StartCompanigs,EndCompanigs])
    return [StartCompanigs,EndCompanigs]


def setStartCompanigs(graph_db_table,worksheet,start_number_of_companies):
    start_companies_list=list()
    row = 1
    col = 0
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    query = "SELECT `From_E`, COUNT(*) FROM `" + graph_db_table + "` GROUP BY `From_E`;"
    cursor.execute(query)
    for i in range(1,start_number_of_companies+1):
        res=cursor.fetchone()
        print(res[0])
        worksheet.write(row, col,res[0])
        start_companies_list.append(res[0])
        print (start_companies_list)
        row += 1
    return start_companies_list


def setEndCompanigs (graph_db_table,worksheet,end_number_of_companies):
    end_companies_list=list()
    row = 0
    col = 1
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    query = "SELECT `To_E`, COUNT(*) FROM `" + graph_db_table + "` GROUP BY `To_E`;"
    cursor.execute(query)
    for i in range(1,end_number_of_companies+1):
        res=cursor.fetchone()
        worksheet.write(row, col,res[0])
        end_companies_list.append(res[0])
        col += 1
    return end_companies_list


def setValuesInMatrix(graph_db_table, worksheet, StartEndCompanies):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    row=1
    for i in range (0,len(StartEndCompanies[0])):
        start_company=StartEndCompanies[0][i]
        col=1
        for j in range (0,len(StartEndCompanies[1])):
            end_company=StartEndCompanies[1][j]
            query="SELECT COUNT(*) FROM `" + graph_db_table + "` WHERE `From_E`= '"+start_company+"' AND `To_E`= '"+end_company+"';"
            cursor.execute(query)
            num=cursor.fetchone()
            print(num[0])
            if (num[0]!=0):
                res=1
            else:
                res=0
            worksheet.write(row, col, res)
            col+=1
        row+= 1


if __name__ == '__main__':
    main()