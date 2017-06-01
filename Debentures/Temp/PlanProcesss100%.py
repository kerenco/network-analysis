import mysql.connector


"""in this script i am taking the graph data from the db and convert it to two text files (80% & 20%) that include
the graph edges and there wieghts... it is possiable that an edge will appear more then once in any file..."""


def main():

    db_table_name= "graph12_12_2016t=0.2"
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    size_query="SELECT COUNT(*) FROM `"+ db_table_name +"`;"
    cursor.execute(size_query)
    size= cursor.fetchone()
    table_length=size[0]
    print(table_length)
    vetrx_list_100= createVetrexList(cursor,db_table_name,table_length)

    text_file_100= open('graph12_12_2016t=x_100%.txt' ,"w")
    for vet in vetrx_list_100:
        to=vetrx_list_100.count([vet[0],vet[1]])
        to_revrse=vetrx_list_100.count([vet[1],vet[0]])
        if(to-to_revrse>0):
          text_file_100.writelines(str(vet[0]) + ',' + str(vet[1])+ ',' + str((to-to_revrse)/(to+to_revrse))+ '\n')
    text_file_100.writelines('-1,-1')
    text_file_100.close()




def createVetrexList(cursor,db_table_name,table_length):

    query = "SELECT * FROM `" + db_table_name + "` ORDER BY RAND();"
    cursor.execute(query)
    vetrx_list_100 = list()
    w_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    x_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')


    for i in range (0, table_length):
        res = cursor.fetchone()

        w_cursor = w_cnx.cursor()
        from_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[0]+"';"
        w_cursor.execute(from_num_query)
        from_num_100=w_cursor.fetchone()[1]

        x_cursor = x_cnx.cursor()
        to_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[1]+"';"
        x_cursor.execute(to_num_query)
        to_num_100=x_cursor.fetchone()[1]

        vetrx_list_100.append([from_num_100,to_num_100])
    return vetrx_list_100


if __name__ == '__main__':
    main()