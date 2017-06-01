import mysql.connector

def main():
    treshhold= {0.05,0.0833,0.1,0.15,0.1666,0.2,0.25}
    for i in treshhold:
        creatingGraph(i)
        print("The graph with treshhold"+str(i) +" had been finished")


def creatingGraph(treshhold):
    graph_table="`graph12_12_2016t=" + str(treshhold)+"`"
    calculateForTable ("`12_12_2016(-aaa+)`",graph_table,treshhold)
    calculateForTable("`12_12_2016(-aa+)`", graph_table, treshhold)
    calculateForTable("`12_12_2016(-a+)`", graph_table, treshhold)
    calculateForTable("`12_12_2016(-bbb+)`", graph_table, treshhold)
    #calculateForTable("`12_12_2016(-bb+)`", graph_table, treshhold)
    calculateForTable("`12_12_2016(-b+)`", graph_table, treshhold)
    calculateForTable("`12_12_2016(-ccc+)`", graph_table, treshhold)
    #calculateForTable("`12_12_2016(-cc+)`", graph_table, treshhold)
    #calculateForTable("`12_12_2016(-c+)`", graph_table, treshhold)

def calculateForTable(detail_table_name,graph_table,treshhold):
    """for each two debenture the edgeDirection value is calculated and then insert in to the correct db table- (Graph) in the DB"""
    num_of_rows= CountRowDataOfTableInDB(detail_table_name)
    #print(num_of_rows)
    for i in range (0,num_of_rows):
        a_debenture = ConectDataToDebenture(i,detail_table_name)
        #print(a_debenture)
        #print("now we are working on deburture number ",i)
        for j in range (i+1,num_of_rows+1):
            #print("and we are compare it to deburture ",j)
            b_debenture=ConectDataToDebenture(j,detail_table_name)
            #print(b_debenture)
            query= calculateDebentureMatrix(a_debenture,b_debenture,treshhold,graph_table)
            cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
            cursor = cnx.cursor()
            if (query is not ""):
                try:
                    print(query)
                    cursor.execute(query)  # Execute the SQL command
                    cnx.commit()  # Commit your changes in the database

                except:
                    cnx.rollback()  # Rollback in case there is any error
                    print("there was an wxception while running the query")
            #print ("The query: ["+query+"] was executed")

            c_debenture =b_debenture
            cnx.close()


def calculateDebentureMatrix(a_debenture, b_debenture, treshhold, graph_tabel):
    """In this function we are building the company graph whille using (aDebenture[2],bDebenture[2])=nominalInterest OR (aDebenture[3],bDebenture[3]) efectiveInterest"""
    query = ""
    a_normal_interest=normalizeInterest(a_debenture[2],a_debenture[3])
    #print(a_normal_interest)
    b_normal_interest = normalizeInterest(b_debenture[2], b_debenture[3])
    #print(b_normal_interest)
    if (abs(a_normal_interest - b_normal_interest) < treshhold) & (a_debenture[4] is not b_debenture[4]):
        if (a_normal_interest- b_normal_interest >= 0):
            query ="INSERT INTO "+graph_tabel+" VALUES ('"+b_debenture[4]+"','"+a_debenture[4]+"');"
            #print("the query for "+a_debenture[4]+" and "+b_debenture[4]+" is: "+query)
            return query
        else:
            query ="INSERT INTO "+graph_tabel+" VALUES ('"+a_debenture[4]+"','"+b_debenture[4]+"');"
            #print("the query for "+b_debenture[4]+" and "+a_debenture[4]+" is: "+query)
            return query
    else:
        return query


def ConectDataToDebenture (given_row_number, table_name):
    query= "SELECT * FROM "+table_name+";"
    #print(query)
    ##Open database connection
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    cursor.execute(query)
    cursor.fetchmany(size=given_row_number-1)
    row=cursor.fetchone()
    ## The order of the deburture is: debentureName = row[1],nominalInterest = row[2],efectiveInterest = row[3],averageTimePeriod = row[4],companyNumber= row[5]
    ##cursor.close()
    return row


def normalizeInterest (interest,average_time_period ):
    """In this function we are normalize the interst of a given deburture"""
    norma_interest= interest/average_time_period
    return norma_interest


def CountRowDataOfTableInDB (table):
    ## Open database connection
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    query = "SELECT COUNT(*) FROM "+table+";"
    ## execute query separately
    #print (query)
    cursor.execute(query)
    res = cursor.fetchone()
    cursor.close()
    return  res[0]      #total rows


if __name__ == '__main__':
    main()