import mysql.connector

def main():
    db_table_name= "graph12_12_2016t=0.05"
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    size_query="SELECT COUNT(*) FROM `"+ db_table_name +"`;"
    cursor.execute(size_query)
    #size=5
    size= cursor.fetchone()
    table_length=size[0]
    text_file= open(db_table_name+'.txt' ,"w")
    vetres= createVetrexList(cursor,db_table_name,table_length)
    [text_file.writelines(str(vet[0]) + ',' + str(vet[1]) + '\n') for vet in vetres]
    text_file.writelines('-1,-1' + '\n')
    text_file.close()


def createVetrexList(cursor,db_table_name,table_length):
    query = "SELECT * FROM `" + db_table_name + "`;"
    cursor.execute(query)
    vetrx_list=list()
    for i in range (1, table_length+1):
        #cursor.fetchmany(size= i-1)
        res = cursor.fetchone()
        w_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
        w_cursor = w_cnx.cursor()
        from_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[0]+"';"
        #print(from_num_query)
        w_cursor.execute(from_num_query)
        from_num=w_cursor.fetchone()[1]
        print(from_num)

        x_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
        x_cursor = x_cnx.cursor()
        to_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[1]+"';"
        #print(to_num_query)
        x_cursor.execute(to_num_query)
        to_num=x_cursor.fetchone()[1]
        print(to_num)

        vetrx_list.append([from_num,to_num])
    return vetrx_list



if __name__ == '__main__':
    main()