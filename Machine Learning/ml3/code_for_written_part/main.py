import math

def createData(a1,a2,a3,r):
    return {"a1":a1, "a2":a2,"a3":a3,"r":r}

data = list()

F = False
T = True

data.append(createData(F,F,F,"+"))
data.append(createData(T,F,T,"+"))
data.append(createData(F,F,T,"-"))
data.append(createData(F,T,F,"+"))
data.append(createData(T,T,F,"-"))
data.append(createData(T,T,T,"-"))
data.append(createData(F,F,F,"-"))

index = 0
tree = dict()

def getID():
    global index
    index = index + 1
    return index

def createLeaf(S, label):
    leaf = {"S":S, "label":label, "isLeaf":True}
    nodeId = getID()
    tree[nodeId] = leaf
    return nodeId

def createNode(S, S_a_T, S_a_F, a_select):
    node = {"S":S, "S_a_T":S_a_T, "S_a_F":S_a_F, "a_select":a_select,"isLeaf":False}
    nodeId = getID()
    tree[nodeId] = node
    return nodeId

def hasSameAttribute(x1,x2):
    return x1["a1"]==x1["a1"] and x1["a2"]==x1["a2"] and x1["a3"]==x1["a3"]

def recur(S):
    if len(S)==2 and hasSameAttribute(S[0], S[1]):
        return createLeaf(S, "+")

    if len(S)==0:
        return None
    if isPure(S):
        return createLeaf(S, S[0]["r"])
    e_a1 = getExpectedEntropyWithSplit(S, "a1")
    e_a2 = getExpectedEntropyWithSplit(S, "a2")
    e_a3 = getExpectedEntropyWithSplit(S, "a3")
    e = min(e_a1,e_a2,e_a3)
    a_select = "a1"
    if e==e_a1:
        a_select = "a1"
    elif e==e_a2:
        a_select = "a2"
    else:
        a_select = "a3"
    S_a_T = getDataByCategory(S, a_select, T)
    S_a_F = getDataByCategory(S, a_select, F)
    return createNode(S, recur(S_a_T), recur(S_a_F), a_select)

def isPure(S):
    label = S[0]["r"]
    for element in S:
        if element["r"]!=label:
            return False
    return True

# math.log(x[, base])
def getEntropy(S, attribute="r",  attributeVal="+"):
    N_pos = 0
    for element in S:
        if element[attribute]==attributeVal:
            N_pos = N_pos+1
    N = len(S)
    N_neg = len(S) - N_pos
    ret = 0
    if N_pos > 0:
        ret = ret - (N_pos/N)*math.log(N_pos/N,2)
    if N_neg > 0:
        ret = ret - (N_neg/N)*math.log(N_neg/N,2)
    return ret

def getDataByCategory(S, a, category):
    return list(filter(lambda x: x[a]==category ,S))

def getExpectedEntropyWithSplit(S, a):
    S_a_T = getDataByCategory(S, a, T)
    S_a_F = getDataByCategory(S, a, F)
    # print(len(S_a_pos))
    # print(len(S_a_neg))
    # print()

    S_a_T_entropy = 0 if len(S_a_T)==0 else (len(S_a_T)/len(S))*getEntropy(S_a_T)
    S_a_F_entropy = 0 if len(S_a_F)==0 else (len(S_a_F)/len(S))*getEntropy(S_a_F)

    return S_a_T_entropy+S_a_F_entropy

def getConditionalEntropy(S, Y, Y_vals, X, X_vals):
    ret = 0
    for x_val in X_vals:
        S_x_val = getDataByCategory(S, X, x_val)
        entropy_y = getEntropy(S_x_val, Y, Y_vals[0])
        ret = ret + (len(S_x_val)/len(S))*entropy_y
    return ret


# 1.(c) calculate decision tree
recur(data)
for nodeId in tree:
    print(nodeId)
    print(tree[nodeId])
    print()
    print()

# 1.(d) calculate H(Y) and H(Y|X)
print(getEntropy(data,"r","+"))
print(getConditionalEntropy(data, "r",["+","-"], "a1",[T,F]))
