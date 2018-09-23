# Name: Haonan Wu
# Number: N18859539
import numpy as np
import pandas as pd
from scipy import stats


def csv2np(filename):
    return pd.read_csv(filename, header=None).values

def log_guassian(mean, variance2, x):
    a = np.log(1/np.sqrt(2 * np.pi * variance2))
    b = (-(x - mean)**2 / 2 / variance2) * np.log(np.exp(1))
    return a + b

def write_file(data):
    f = open("result.txt", "a") 
    f.write(str(data) + "\n")

def train(filename):
    train_data = csv2np(filename)
    total_examples, cols = train_data.shape
    class_type, class_cnt = np.unique(train_data[:,-1], return_counts=True)
    
    PC = dict(zip(class_type, class_cnt/total_examples)) 
    PXiC = {}
    
    for class_name in class_type:
        class_data = train_data[train_data[:,-1]==class_name]
        num_example, _ = class_data.shape
        tmp_result = []
        for i in range(0, cols-1): 
            average = np.mean(class_data[:,i])
            length = np.linalg.norm(class_data[:,i] - average)
            variance2 = length**2 / (num_example-1)
            tmp_result.append((average, variance2))
        PXiC[class_name] = tmp_result
    
    return (PC, PXiC)

def predict(filename, model):
    test_data = csv2np(filename)
    PC, PXiC = model
    num_test, cols = test_data.shape
    result = np.zeros((num_test, len(PC.keys())))
    class_type = list(PC.keys())
    
    for t in range(len(class_type)):
        i = class_type[t]
        tmp = np.zeros(test_data.shape)
        for k in range(num_test):
            for j in range(0, cols-1):
                data = test_data[k, j]
                tmp[k, j] = log_guassian(PXiC[i][j][0], PXiC[i][j][1], data)

        tmp = np.sum(tmp, axis=1) + np.log(PC[i])
        result[:,t] = tmp

    mapidx = np.argmax(result, axis=1)

    pred_res = np.zeros(mapidx.shape)
    for t in range(len(class_type)):
        pred_res[mapidx[:]==t] = class_type[t]

    for i in pred_res:
        write_file(int(i))
    total = pred_res.shape
    correct_number = np.sum(pred_res==test_data[:,-1])
    error_number = total - correct_number
    write_file(correct_number)
    write_file(error_number)
    write_file(error_number / total)
    # print("correct number: %f" % correct_number)   
    # print("error number: %f" % error_number)   
    # print("error rate: %f" % (error_number / total))

    # number = np.sum(test_data[:,-1]==0.0)
    # print(number, test_data.shape[0])

if __name__=="__main__":
    model = train('spambasetrain.csv')
    write_file(model[0][0.0])
    write_file(model[0][1.0])
    for i in model[1][0.0]:
        write_file(i)
    for i in model[1][1.0]:
        write_file(i)

    # predict('spambasetrain.csv', model)
    predict('spambasetest.csv', model)

    # tt = csv2np('spambasetrain.csv')
    # for i in range(0,9):
    #     for j in range(i+1,9):
    #         a =  np.corrcoef(tt[:,i],tt[:,j])[0, 1]
    #         print("%d %d: %f" %(i, j, a))
