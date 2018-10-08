import numpy as np
import itertools

def readfile(filename):
    label = []
    features = []

    with open(filename) as f:
        line = f.readline()
        while line:
            label.append(line[0])
            features.append(set(line[1:].split()))
            line = f.readline()
    return features, label

class KNearestNeighbor(object):
    def distance(self, set1, set2):
        if self.distfuction == 0:
            return len(set1 & set2)
        else:
            a = len(set1 & set2)
            b = len(set1 | set2)
            return b / (b - a) if b > a else float("inf")

    def train(self, X, y, distance = 0):
        self.distfuction = distance
        self.X_train = X
        self.y_train = np.array(y).astype('int')
    
    def predict(self, X, y, k=1):
        error = 0
        y_pred = [1 for _ in range(len(X))]
        for i in range(len(X)):
            dist = np.array(list(map(lambda a : self.distance(X[i], a), self.X_train)))
            dist_sort = sorted(dist)
            dist_top = set(dist_sort[-k:])
            labels = []
            for d in dist_top:
                labels.append(list(self.y_train[dist == d]))
            closest_y = list(itertools.chain.from_iterable(labels)) + [0, 1]
            counts = np.bincount(closest_y)
            y_pred[i] = np.argmax(list(reversed(counts))) ^ 1
            if y_pred[i] != int(y[i]):
                error += 1
        print(error)
        return y_pred, 1 - error / len(X)

    def cross_validation(self, X, y, k=1, cross=5):
        n = len(X)
        l = n // cross
        
        ave_acc = 0.0
        
        for i in range(cross):
            X_train, y_train = X[0:i*l] + X[i*l+l:], y[0:i*l] + y[i*l+l:]
            X_test, y_test = X[i*l:i*l+l], y[i*l:i*l+l]
            self.train(X_train, y_train)
            _, acc = self.predict(X_test, y_test, k)
            ave_acc += acc
        print("\n{}\n".format(ave_acc / 5.0))

if __name__ == '__main__':
    X_train, y_train = readfile("reviewstrain.txt")
    # print(len(X_train))
    # X_test, y_test = readfile("reviewstest.txt")
    # X_test, y_test = readfile("negative.txt")
    X_test, y_test = readfile("positive.txt")
    # X_test, y_test = readfile("test.txt")
    # print(len(X_test))
    knn = KNearestNeighbor()
    # knn.train(X_train[0:10], y_train[0:10])
    # knn.predict(X_test[0:1], y_test[0:1], 1)
    # knn.train(X_train, y_train)
    # knn.predict(X_test, y_test, 1)

    # for k in [3, 7, 99]:
    #     knn.cross_validation(X_train, y_train, k, 5)

    knn.train(X_train, y_train, 1)
    knn.predict(X_test, y_test, 5)