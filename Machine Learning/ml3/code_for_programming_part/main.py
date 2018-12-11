import numpy as np

# 2.(d)
matrix = np.array([[0,14],[6,9]])
print(np.linalg.eig(matrix))

# 3.(c)
matrixB = np.array([[-0.75,-1.5,0.5],[3.25,2.5,0.5],[1.25,-2.5,-3.5],[-3.75,1.5,2.5]])
print(np.cov(matrixB,rowvar=False))
# print(np.linalg.eig(np.cov(matrixB,rowvar=False))[0])
print(max(np.linalg.eig(np.cov(matrixB,rowvar=False))[0]))


# 3.(d)
import sklearn.decomposition as skd
pca = skd.PCA(n_components = 3)
skd.PCA.fit(pca,matrixB)
W1 = pca.components_
W = W1.transpose()
Z = pca.transform(matrixB)
# print(Z)
print(np.array(list(map(lambda x:x[:2], Z))))

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import fetch_lfw_people
lfw_people = fetch_lfw_people(min_faces_per_person=70)
n_samples, h, w = lfw_people.images.shape
npix = h*w
fea = lfw_people.data
def plt_face(x):
    global h,w
    plt.imshow(x.reshape((h, w)), cmap=plt.cm.gray)
    plt.xticks([])
plt.figure(figsize=(10,20))

# 5.(a)
plt_face(fea[3])
plt.show()

# 5.(b)
size = len(fea[0])
N = len(fea)
means = np.zeros(size)
for f in fea:
    for index in range(len(f)):
        means[index] = means[index] + f[index]
means = means/N
plt_face(means)
plt.show()

# 5.(c)
import sklearn.decomposition as skd
pca = skd.PCA(n_components = 5)
skd.PCA.fit(pca,fea)
W1 = pca.components_
print(W1)

# 5.(d)
fea2 = pca.transform(fea)
meanMatrix = list()
for index in range(len(fea)):
    meanMatrix.append(means)
meanMatrix = np.array(meanMatrix)
print(meanMatrix)
approximate = np.matmul(fea2, W1) + meanMatrix
plt_face(approximate[3])
plt.show()

pca = skd.PCA(n_components = 50)
skd.PCA.fit(pca,fea)
W1 = pca.components_
fea2 = pca.transform(fea)
meanMatrix = list()
for index in range(len(fea)):
    meanMatrix.append(means)
meanMatrix = np.array(meanMatrix)
print(meanMatrix)
approximate = np.matmul(fea2, W1) + meanMatrix
plt_face(approximate[3])
plt.show()
