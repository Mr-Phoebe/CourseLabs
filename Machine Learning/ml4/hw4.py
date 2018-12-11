# teammate:
# Xinglun Xu (xx688) Haonan Wu (hw1651)


# coding: utf-8

# In[304]:


with open('reviewstrain.txt', 'r') as reviewstrainFile:
    reviewstrainBuffer = reviewstrainFile.read()

with open('reviewstest.txt', 'r') as reviewstestFile:
    reviewstestBuffer = reviewstestFile.read()

reviewstrainBuffer = reviewstrainBuffer.splitlines()
reviewstestBuffer = reviewstestBuffer.splitlines()

def parseCommentIntoTrainData(s):
    raw = s
    raw = raw.split()
    label = True if raw[0]=="1" else False
    raw.pop(0)
    newSet = set()
    for s in raw:
        newSet.add(s)
    newSet = list(newSet)
    return label, newSet

reviewsTrain = list(map(parseCommentIntoTrainData, reviewstrainBuffer))
reviewsTest = list(map(parseCommentIntoTrainData, reviewstestBuffer))


# In[283]:


dic = dict()
for _, doc in reviewsTrain:
    for word in doc:
        if word not in dic:
            dic[word]=0
        dic[word]+=1



# In[284]:


import operator
#(a)
print("a")
sortedList = sorted(dic.items(), key=operator.itemgetter(1))
sortedList.reverse()
print(sortedList[:5])


# In[317]:


import pandas as pd

df = pd.DataFrame(reviewsTrain,columns=['label', 'wordsAttribute'])


# In[318]:


import numpy as np

s = set()
def addWordToSet(x):
    for word in x:
        s.add(word)
df['wordsAttribute'].apply(addWordToSet)
s = list(s)

def transformWordsToFeatures(df):
    wordCols = []
    for word in s:
        wordCol = []
        for row in df.itertuples():
            b = True if word in row[2] else False
            wordCol.append(b)
        wordCols.append(wordCol)

    tempDf = pd.DataFrame(np.array(wordCols).transpose(), columns=s)

    return pd.concat([df, tempDf], axis=1)


# In[319]:


df3 = transformWordsToFeatures(df)


# In[315]:


import math


def getEntropy(S, labelName):
    counts = S[labelName].value_counts().to_dict()
    N_pos = 0 if True not in counts else counts[True]
    N_neg = 0 if False not in counts else counts[False]
    N = len(S)
    ret = 0
    if N_pos > 0:
        ret = ret - (N_pos/N)*math.log(N_pos/N,2)
    if N_neg > 0:
        ret = ret - (N_neg/N)*math.log(N_neg/N,2)
    return ret

def getDataByCategory(df, typeName, typeVal):
    return df.loc[df[typeName]==typeVal]

def getExpectedEntropyWithSplit(S, a):
    S_a_T = getDataByCategory(S, a, True)
    S_a_F = getDataByCategory(S, a, False)
    # print(len(S_a_pos))
    # print(len(S_a_neg))
    # print()

    S_a_T_entropy = 0 if len(S_a_T)==0 else (len(S_a_T)/len(S))*getEntropy(S_a_T, 'label')
    S_a_F_entropy = 0 if len(S_a_F)==0 else (len(S_a_F)/len(S))*getEntropy(S_a_F, 'label')

    return S_a_T_entropy+S_a_F_entropy




# In[321]:


# getExpectedEntropyWithSplit(df3, ".")
# df3.loc[df3['poor']==True]['label'].value_counts()
# getExpectedEntropyWithSplit(df3, "bad")
# getEntropy(df3.loc[df3['poor']==True], "label")

originalEntropy = getEntropy(df3, 'label')
infoGainDic = dict()
for word in s:
    infoGain = originalEntropy - getExpectedEntropyWithSplit(df3, word)
    infoGainDic[word] = infoGain



# In[322]:


sorted_by_value = sorted(infoGainDic.items(), key=lambda kv: kv[1])
sorted_by_value.reverse()
trainAttributes = [key for key,_ in sorted_by_value[:50]]


# In[380]:


#(b)
print("b")
print([key for key,_ in sorted_by_value[:5]])


# In[346]:


from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(hidden_layer_sizes=(10))
clf.fit(df3[trainAttributes], df3['label'])


# In[324]:


testdf = pd.DataFrame(reviewsTest,columns=['label', 'wordsAttribute'])


# In[325]:


transformedTestDf = transformWordsToFeatures(testdf)


# In[347]:


clf.score(transformedTestDf[trainAttributes],transformedTestDf['label'] )


# In[349]:


predict_result = clf.predict(transformedTestDf[trainAttributes] )
true_result = transformedTestDf['label']


# In[356]:


from sklearn.metrics import confusion_matrix
#(c)
print("c")
tn, fp, fn, tp = confusion_matrix(true_result, predict_result).ravel()
print("true negative: ",tn, "\nfalse positive: ",fp, "\nfalse negative: ",fn, "\ntrue positive: ",tp)
print("accuracy: ", (tp+tn)/(tp+tn+fp+fn))


# In[358]:


df3['label'].value_counts()


# In[360]:


predict_result = np.full(len(transformedTestDf),True)


# In[362]:


#(d)
print("d")
tn, fp, fn, tp = confusion_matrix(true_result, predict_result).ravel()
print("accuracy: ", (tp+tn)/(tp+tn+fp+fn))


# In[363]:


#(e)
print("e")
#We decrease the number of attributes to prevent overfitting.
#
#We increase the number of attributes to make our model learn intention of more words.
#In this way, our model can interpret meaning of more words


# In[364]:


def trainWithK(k):
    trainAttributes = [key for key,_ in sorted_by_value[:k]]
    clf = MLPClassifier(hidden_layer_sizes=(10))
    clf.fit(df3[trainAttributes], df3['label'])
    return clf.score(transformedTestDf[trainAttributes],transformedTestDf['label'])


# In[368]:


trainWithK(100)


# In[378]:


import matplotlib.pyplot as plt

#(f)
print("f")
listK = [1, 5, 25, 125, 625]
listAccuracy = [trainWithK(k) for k in listK]


# In[381]:

print("we choose k with values: ",listK)
print("the corresponding accuracy: ", listAccuracy)


# In[379]:


plt.plot(listK, listAccuracy)


# In[ ]:


#(f)
# The result from the graph is what I expected.
# We sort attributes based on their significance and then add them to our train data in the order of significance.
# Firstly, the accuracy grow rapidly as we add attributes since those attributes are very related to the target variable.
# However, after around 150 attributes, the marginal benefit of adding attributes is becoming trivial since those attributes
# are not significant anymore.
