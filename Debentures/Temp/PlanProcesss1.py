import mysql.connector


"""in this script i am taking the graph data from the db and convert it to two text files (80% & 20%) that include
the graph edges and there wieghts... it is possiable that an edge will appear more then once in any file..."""


def main():

    db_table_name= "graph12_12_2016t=0.25"
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    size_query="SELECT COUNT(*) FROM `"+ db_table_name +"`;"
    cursor.execute(size_query)
    size= cursor.fetchone()
    table_length=size[0]
    vetrx_list_80, vetrx_list_20= createVetrexList(cursor,db_table_name,table_length)

    text_file_80= open(db_table_name+'_80%.txt' ,"w")
    for vet in vetrx_list_80:
        to=vetrx_list_80.count([vet[0],vet[1]])
        to_revrse=vetrx_list_80.count([vet[1],vet[0]])
        if(to-to_revrse>0):
          text_file_80.writelines(str(vet[0]) + ',' + str(vet[1])+ ',' + str((to-to_revrse)/(to+to_revrse))+ '\n')
    text_file_80.writelines('-1,-1')
    text_file_80.close()

    text_file_20 = open(db_table_name + '_20%.txt', "w")
    for vet in vetrx_list_20:
        to=vetrx_list_20.count([vet[0],vet[1]])
        to_revrse=vetrx_list_20.count([vet[1],vet[0]])
        if(to-to_revrse>0):
          text_file_20.writelines(str(vet[0]) + ',' + str(vet[1])+ ',' + str((to-to_revrse)/(to+to_revrse))+ '\n')
    text_file_20.writelines('-1,-1')
    text_file_20.close()



def createVetrexList(cursor,db_table_name,table_length):

    query = "SELECT * FROM `" + db_table_name + "` ORDER BY RAND();"
    cursor.execute(query)
    vetrx_list_80 = list()
    vetrx_list_20 = list()
    w_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    x_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    e_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    r_cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')

    for i in range (1, int(0.8*table_length)+1):
        res = cursor.fetchone()

        w_cursor = w_cnx.cursor()
        from_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[0]+"';"
        w_cursor.execute(from_num_query)
        from_num_80=w_cursor.fetchone()[1]

        x_cursor = x_cnx.cursor()
        to_num_query= "SELECT * FROM `company_key` WHERE `company_Name`='"+res[1]+"';"
        x_cursor.execute(to_num_query)
        to_num_80=x_cursor.fetchone()[1]

        vetrx_list_80.append([from_num_80,to_num_80])

    for i in range(int(0.8 * table_length) + 1,table_length+1):
        res = cursor.fetchone()

        e_cursor = e_cnx.cursor()
        from_num_query = "SELECT * FROM `company_key` WHERE `company_Name`='" + res[0] + "';"
        e_cursor.execute(from_num_query)
        from_num_20 = e_cursor.fetchone()[1]

        r_cursor = r_cnx.cursor()
        to_num_query = "SELECT * FROM `company_key` WHERE `company_Name`='" + res[1] + "';"
        r_cursor.execute(to_num_query)
        to_num_20 = r_cursor.fetchone()[1]

        vetrx_list_20.append([from_num_20, to_num_20])

    return vetrx_list_80,vetrx_list_20


if __name__ == '__main__':
    main()