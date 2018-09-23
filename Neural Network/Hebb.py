import numpy as np

def train(train_data):
    features = train_data[:, : -1]
    labels = train_data[:, -1]
    rows, col = features.shape
    weight = np.zeros(col)
    bias = 0

    #trainning
    for i in range(rows):
        weight += features[i,:] * labels[i]
        bias += labels[i]

    return weight, bias


def test(weight, bias, test_data):
    features = test_data[:, : -1]
    labels = test_data[:, -1]
    rows, _ = features.shape
    # test
    error = 0
    for i in range(rows):
        res = 0

        if np.dot(weight, features[i,:]) + bias >= 0:
            res=1
        else:
            res=-1

        if res != labels[i]:
            error += 1

    return error


def process1(weight, bias):

    c = [0,1,1,1,0,0,1,0,0,1,0,0,0,1,1]
    total = 1<<15
    k_error = [0 for _ in range(16)]
    for i in range(1, total):
        tmp = i
        bits = 0
        index = 0
        cur = np.array([c + [1]])
        while tmp != 0:
            if tmp & 1:
                cur[0, index] ^= 1
                bits += 1
            index += 1
            tmp >>= 1
        k_error[bits] += test(weight, bias, cur)
    return k_error

def process2(weight, bias):

    c = [0,1,1,1,0,0,1,0,0,1,0,0,0,1,1]
    total = 1<<15
    k_error = [0 for _ in range(16)]
    for i in range(1, total):
        tmp = i
        bits = 0
        index = 0
        cur = np.array([c + [1]])
        while tmp != 0:
            if tmp & 1:
                cur[0, index] = 0
                bits += 1
            index += 1
            tmp >>= 1
        k_error[bits] += test(weight, bias, cur)
    return k_error


if __name__ =="__main__":

    c = [0,1,1,
         1,0,0,
         1,0,0,
         1,0,0,
         0,1,1]

    nc = [1,0,1,
          1,0,1,
          0,1,0,
          1,0,1,
          1,0,1]

    train_data = np.array([c + [1], nc + [-1]])

    weight, bias = train(train_data)

    k_error = process1(weight, bias)

    print(k_error)

    k_error = process2(weight, bias)

    print(k_error)

