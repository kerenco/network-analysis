

def main():
    """for each two debenture the edgeDirection value is calculated and then insert in to the correct db table- (Graph) in the DB"""
    treshhold=1
    numOfRows= 7
    for i in range (1,numOfRows):
        a_debenture = ConectDataToDebenture(i)
        print("now we are working on Deburture number ",i)
        for j in range (i+1,numOfRows+1):
            print("and we are compare it to Deburture ",j)
            b_debenture=ConectDataToDebenture(j)
            query= calculateDebentureMatrix(a_debenture,b_debenture,treshhold)
            print ("The query: [",query,"] was executed")
    print("The graph building had been finished")


def calculateDebentureMatrix(a_debenture, b_debenture, treshhold):
    """In this function we are building the company graph whille using (aDebenture[2],bDebenture[2])=nominalInterest OR (aDebenture[3],bDebenture[3]) efectiveInterest"""
    query = ""
    a_normal_interest=normalizeInterest(a_debenture[2],a_debenture[3])
    print(a_normal_interest)
    b_normal_interest = normalizeInterest(b_debenture[2], b_debenture[3])
    print(b_normal_interest)
    if (abs(a_normal_interest - b_normal_interest) < treshhold)&(a_debenture[4] is not b_debenture[4]):
        if (a_normal_interest- b_normal_interest >= 0):
            #query = "INSERT INTO Graph (From_E,To_E) VALUES ('"+b_debenture[4]+"','"+a_debenture[4]+"');"
            print("the query for "+a_debenture[4]+" and "+b_debenture[4]+" is: ",query)
            return query
        else:
           # query = "INSERT INTO Graph (From_E,To_E) VALUES ('" + a_debenture[4] + "','" + b_debenture[4] + "');"
            print("the query for " + b_debenture[4] + " and " + a_debenture[4] + " is: ", query)
            return query
    else:
        return query


def normalizeInterest (interest,average_time_period ):
    """In this function we are normalize the interst of a given deburture"""
    norma_interest= interest/average_time_period
    return norma_interest


def ConectDataToDebenture (given_row_number):
    # The order of the deburture is: debentureName = row[1],nominalInterest = row[2],efectiveInterest = row[3],averageTimePeriod = row[4],companyNumber= row[5]
    debenture = [["A",2.00, 0.78, 0.95, "אאורה"]
                ,["B",2.92, 1.98, 1.62, "אאורה"]
                ,["C",4.04, 3.09, 2.86, "אאורה"]
                ,["D", 4.74, 4.11, 3.91, "אאורה"]
                ,["E",1.41, 0.23, 1.11,"אבגול"]
                ,["F",3.24, 2.50, 4.95, "אבגול"]
                ,["G",3.06, 1.46, 2.79, "אביב"]]
    asd=debenture[given_row_number-1]
    return asd


if __name__ == '__main__':
    main()