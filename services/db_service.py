import mysql.connector

def executeInsertQuery(query):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute(query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error
    cnx.close()

def executeInsertQuerysArray(arr):
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor(buffered=True)
    for query in arr:
        try:
            cursor.execute(query)  # Execute the SQL command
            cnx.commit()  # Commit your changes in the database
        except:
            cnx.rollback()  # Rollback in case there is any error
    cnx.close()

def fetchoneQueryResult(query):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)  # Execute the SQL command
    cnx.close()
    return cursor.fetchone()

def fetchallQueryResult(query):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)  # Execute the SQL command
    cnx.close()
    return cursor.fetchall()

def executeCreateQuery(query):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    try:
        print(query)
        cursor.execute(query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error
        print("there was an exception while running the query")
    cnx.close()

def executeDeleteQuery(query):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute(query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error
        print("there was an exception while running the query")
    cnx.close()

def executeTruncateQuery(table):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute("TRUNCATE TABLE `master_thesis`." + table + ";")  # Execute the SQL command
    except:
        cnx.rollback()  # Rollback in case there is any error
        print("there was an exception while running the query")
    cnx.close()

def executeCreateTableQuery(query):
    cnx = createCNX()
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute(query)  # Execute the SQL command
        cnx.commit()  # Commit your changes in the database
    except:
        cnx.rollback()  # Rollback in case there is any error
    cnx.close()

def createCNX():
    return mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')

def createCursor(is_buffered):
    cnx = createCNX()
    return cnx.cursor(buffered=is_buffered)