from datetime import datetime
import time

def start(f,algo_name):
    f.writelines('Start ' + algo_name + ' at: \n'  + str(datetime.now()) + '\n');
    return time.time()

def stop(f,start):
    f.writelines(str(datetime.now()) + '\nfinish! \n')
    f.writelines('It Took: ' + str(time.time() - start) +'\n')
