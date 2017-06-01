import matplotlib.pyplot as plt
import mysql.connector
import numpy as np


def main ():
    date = '12_12_2016' #'11_03_2016'#
    matrix = get_details_from_db(date)
    plot_histograms(matrix, date)


def plot_histograms(matrix,date):
    fig = plt.figure(figsize=(10, 8))

    sub1 = fig.add_subplot(521)  # instead of plt.subplot(3, 2, 1)
    sub1.set_title('page_rank ,variance: '+str(np.var(matrix[2])))  # non OOP: plt.title('The function f')
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub1.hist(matrix[2], bins=50, normed=True, stacked=True, cumulative=True)

    sub2 = fig.add_subplot(522)
    sub2.set_title('hierarchyEnergy, variance: '+str(np.var(matrix[3])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub2.hist(matrix[3], bins=50, normed=True, stacked=True, cumulative=True)

    sub3 = fig.add_subplot(523)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub3.set_title('flow,variance: '+str(np.var(matrix[0])))
    sub3.hist(matrix[0], bins=50, normed=True, stacked=True, cumulative=True)

    sub4 = fig.add_subplot(524)
    sub4.set_title('A.Bvariance: '+str(np.var(matrix[1])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub4.hist(matrix[1], bins=50, normed=True, stacked=True, cumulative=True)

    sub5 = fig.add_subplot(525)
    sub5.set_title('intercept, variance: '+str(np.var(matrix[4])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub5.hist(matrix[4], bins=50, normed=True, stacked=True, cumulative=True)

    sub6 = fig.add_subplot(526)
    sub6.set_title('prediction score,variance: '+str(np.var(matrix[5])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub6.hist(matrix[5], bins=50, normed=True, stacked=True, cumulative=True)

    sub7 = fig.add_subplot(527)
    sub7.set_title('APH1 prediction score,variance: '+str(np.var(matrix[6])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub7.hist(matrix[6], bins=50, normed=True, stacked=True, cumulative=True)

    sub8 = fig.add_subplot(528)
    sub8.set_title('APH2 prediction score,variance: '+str(np.var(matrix[7])))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    sub8.hist(matrix[7], bins=50, normed=True, stacked=True, cumulative=True)

    sub9 = fig.add_subplot(529)
#    sub9.set_title('APH3 prediction score,variance: '+str(np.var(matrix[8])))#
    sub9.set_title('Davids prediction score,variance: '+str(np.var(matrix[9])))

    plt.xlabel("Value")
    plt.ylabel("Frequency")
    #sub9.hist(matrix[8],bins=50,normed=True,stacked=True,cumulative=True)
    sub9.hist(matrix[9], bins=50, normed=True, stacked=True, cumulative=True)

    plt.tight_layout()
    plt.savefig('debenture.png')
    plt.show()

def get_details_from_db(date):
    matrix = [[], [], [], [], [], [], [], [], [], []]
    cnx = mysql.connector.connect(user='root', password='YOFISHELI', host='127.0.0.1', database='master_thesis')
    cursor = cnx.cursor()
    size_query = "SELECT COUNT(8) FROM `debenture_results`;"
    cursor.execute(size_query)
    size = cursor.fetchone()
    table_length = size[0]
    query = "SELECT * FROM `debenture_results`;"
    print(query)
    cursor.execute(query)
    for i in range(0, table_length):
        res = cursor.fetchone()
        matrix[0].append(res[4])
        matrix[1].append(res[5])
        matrix[2].append(res[6])
        matrix[3].append(res[7])
        matrix[4].append(res[8])
        matrix[5].append(res[9])
        matrix[6].append(res[13])
        matrix[7].append(res[14])
        matrix[8].append(res[15])
        matrix[9].append(res[16])
    return matrix


if __name__ == '__main__':
    main()