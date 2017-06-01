from services import db_service
import csv
import os

def main():
    indir="network-analysis/Debentures/Temp/data"
    os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\Debentures\Temp\data")
    for fn in os.listdir('.'):
        if os.path.isfile(fn):
            try:
                print("file name: ", fn)
                move_file_details_to_db(fn)
                os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis")
            except:
                print("!@#$%^&*()(*&^%$#@!  there was a problem with the data in the table: ", fn)
        os.chdir(r"C:\Users\Doron\workspace\MasterThasisProject\network-analysis\A1\ShizukaMcDonald_Data")


####################################################################
##############       move the file to the db         ###############
####################################################################

def move_file_details_to_db(file):
    create_table(file)
    ###insert the data to the db
    insert_the_data_in_to_the_db(file)


def create_table(file):
    query = "CREATE TABLE `" + file[:-4] + "` " \
            "(`date` TEXT COLLATE utf8_unicode_ci,`debenture_name` TEXT COLLATE utf8_unicode_ci,`debenture_number` " \
            "INT(11) DEFAULT NULL,`kind_of_debenture` TEXT COLLATE utf8_unicode_ci,`interest` DOUBLE DEFAULT NULL," \
            "`MACHAM` DOUBLE DEFAULT NULL,`company_name` TEXT COLLATE utf8_unicode_ci,`MALOT_rank` TEXT COLLATE " \
            "utf8_unicode_ci,`end_day_value` DOUBLE DEFAULT NULL) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
    db_service.executeCreateTableQuery(query)

def insert_the_data_in_to_the_db(file):
    f = open(file, 'r')
    reader1 = csv.reader(f, delimiter=',')
    first_row = next(reader1)
    for row in reader1:
        query = insertQueryBuilder(row, file, first_row)
        db_service.executeInsertQuery(query)

def insertQueryBuilder(row, file, first_row):
    query = "INSERT INTO `" + file[:-4] + "` VALUES ("
    for j in range(0, len(first_row)):
        value = row[j]
        if j in [2, 4, 5, 8]:
            if j == 4:
                query = query + str(value)[:-1] + ","
            else:
                query = query + str(value) + ","
        else:
            query = query + "'" + str(value) + "',"
    return query[:-2]+");"

if __name__ == '__main__':
    main()