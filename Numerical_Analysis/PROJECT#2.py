import numpy as np
import cv2
import copy
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib import style
import random

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

np.random.seed(seed=1)

def scatterData(xmu,xsigma,ymu,ysigma,zmu,zsigma):
    x = np.random.normal(xmu, xsigma, size=300).reshape(-1, 1)
    y = np.random.normal(ymu, ysigma, size=300).reshape(-1, 1)
    z = np.random.normal(zmu, zsigma, size=300).reshape(-1, 1)

    data = np.hstack((x,y,z))

    return data

def scatterData2(xmu,xsigma,ymu,ysigma,zmu,zsigma):
    x = np.random.normal(xmu, xsigma, size=100).reshape(-1, 1)
    y = np.random.normal(ymu, ysigma, size=100).reshape(-1, 1)
    z = np.random.normal(zmu, zsigma, size=100).reshape(-1, 1)

    data = np.hstack((x,y,z))

    return data

######################[ 클러스터의 최대 거리 ]#########################
def setMaximum(A,meanA,percent): # A = 클러스터, meanA = 클러스터평균, percent = 데이터를 포함할 범위
    shapeM = np.shape(A)
    x = np.zeros(shapeM[0]).reshape(-1,1)
    for i in range(shapeM[0]):
        x[i] = (A[i][0]-meanA[0])**2+(A[i][1]-meanA[1])**2+(A[i][2]-meanA[2])**2

    indices = x.reshape(1,-1).argsort()
    num = int(shapeM[0] * percent)
    x = x[indices[0]]

    return x[num-1]

############### < 군집이 떨어져있을 때 > #################
# set1 = scatterData(0.0,1.0, 0.0,1.0, 1.0,2.0)
# set2 = scatterData(10.0,1.0, 5.0,1.0, 5.0,1.5)
# set3 = scatterData(10.0,1.0, 5.0,1.5, 20.0,2.0)
# set4 = scatterData(15.0,1.0, 10.0,1.0, 15.0,2.0)
# set5 = scatterData(20.0,1.0, 15.0,1.0, 25.0,1.0)

####################< 실험용 >##########################
set1 = scatterData(5.0,1.5, 5.0,1.5, 5.1,1.5)
set2 = scatterData(5.2,0.5, 5.1,0.3, 5.0,0.7)
set3 = scatterData(5.1,1.0, 5.2,2.0, 5.2,0.7)
set4 = scatterData(7.0,1.5, 8.0,1.5, 1.0,1.0)
set5 = scatterData(13.0,0.5, 13.0,1.0, 14.0,0.8)

# testset = scatterData(5.0,1.0,7.0,1.0,6.0,1.0)
testset = scatterData(10.0,5.0,10.0,5.0,10.0,1.0)
integratedSet = np.vstack([set1,set2,set3,set4,set5])

integratedSet2 = copy.copy(integratedSet)
integratedSet = np.float32((integratedSet))

criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 1000, 1.0)
ret, label, center = cv2.kmeans(integratedSet,5,None,criteria,1000,cv2.KMEANS_RANDOM_CENTERS)

originSet = np.zeros((1500,1),dtype=np.uint8)


A = integratedSet[label.ravel()==0]
B = integratedSet[label.ravel()==1]
C = integratedSet[label.ravel()==2]
D = integratedSet[label.ravel()==3]
E = integratedSet[label.ravel()==4]


maxA = setMaximum(A,center[0],0.95)
maxB = setMaximum(B,center[1],0.95)
maxC = setMaximum(C,center[2],0.95)
maxD = setMaximum(D,center[3],0.95)
maxE = setMaximum(E,center[4],0.95)

maxarray = np.array([maxA,maxB,maxC,maxD,maxE])

def findCluster(set,center,max):
    shapeA = np.shape(set)
    retA = np.zeros(shapeA[0])
    retB = np.zeros(shapeA[0])
    for i in range(shapeA[0]):
        dist = np.sum((set[i][0]-center[0][0])**2+(set[i][1]-center[0][1])**2+(set[i][2]-center[0][2])**2)
        if dist < max[0]:
            retA[i] = 0
            continue
        dist = np.sum((set[i][0]-center[1][0])**2+(set[i][1]-center[1][1])**2+(set[i][2]-center[1][2])**2)
        if dist < max[1]:
            retA[i] = 1
            continue
        dist = np.sum((set[i][0]-center[2][0])**2+(set[i][1]-center[2][1])**2+(set[i][2]-center[2][2])**2)
        if dist < max[2]:
            retA[i] = 2
            continue
        dist = np.sum((set[i][0]-center[3][0])**2+(set[i][1]-center[3][1])**2+(set[i][2]-center[3][2])**2)
        if dist < max[3]:
            retA[i] = 3
            continue
        dist = np.sum((set[i][0]-center[4][0])**2+(set[i][1]-center[4][1])**2+(set[i][2]-center[4][2])**2)
        if dist < max[4]:
            retA[i] = 4
            continue
        retA[i] = 5


    return retA

find = findCluster(integratedSet2,center,maxarray) # 원래 데이터를 재 배치
count = 0

for j in range(5):
    for k in range(300):
        originSet[k + j * 300] = count + j

find2 = copy.copy(find)
index = find.argsort()
findlabel = find2[index].astype(np.uint8)
originSet = originSet.astype(np.uint8).reshape(-1,1)

correct = np.zeros((5,1000),dtype=np.uint8)

intsetA = integratedSet2[find.ravel()==0]
intsetB = integratedSet2[find.ravel()==1]
intsetC = integratedSet2[find.ravel()==2]
intsetD = integratedSet2[find.ravel()==3]
intsetE = integratedSet2[find.ravel()==4]
intsetF = integratedSet2[find.ravel()==5]

#########################맥시멈적용 셋###############################
fillA = np.full((np.shape(intsetA[:,0])), 0, dtype=int).reshape(-1,1)
fillB = np.full((np.shape(intsetB[:,0])), 1, dtype=int).reshape(-1,1)
fillC = np.full((np.shape(intsetC[:,0])), 2, dtype=int).reshape(-1,1)
fillD = np.full((np.shape(intsetD[:,0])), 3, dtype=int).reshape(-1,1)
fillE = np.full((np.shape(intsetE[:,0])), 4, dtype=int).reshape(-1,1)

#########################원래 셋#################################3
# fillA = np.full((np.shape(A[:,0])), 0, dtype=int).reshape(-1,1)
# fillB = np.full((np.shape(B[:,0])), 1, dtype=int).reshape(-1,1)
# fillC = np.full((np.shape(C[:,0])), 2, dtype=int).reshape(-1,1)
# fillD = np.full((np.shape(D[:,0])), 3, dtype=int).reshape(-1,1)
# fillE = np.full((np.shape(E[:,0])), 4, dtype=int).reshape(-1,1)

integratedSet3 = np.vstack([fillA,fillB,fillC,fillD,fillE])
# zeros = np.zeros((1,1))
# integratedSet3 = np.vstack([integratedSet3,zeros])
# originSet = np.vstack([originSet,zeros])
# print(np.shape(originSet))

rangeset = np.array([np.shape(fillA[:,0]),np.shape(fillB[:,0]),np.shape(fillC[:,0]),np.shape(fillD[:,0]),np.shape(fillE[:,0])])
rangeset2 = copy.copy(rangeset)
rangeset[1] = rangeset[1]+rangeset[0]
rangeset[2] = rangeset[2] + rangeset[1]
rangeset[3] = rangeset[3] + rangeset[2]

for i in range(5):
    j=0
    while j < rangeset2[i]:

        if i == 0:
            if label[j] == originSet[j]:
                if j == 300:
                    break
                correct[i][j]=1
                j+=1
                continue
            else :
                correct[i][j]=0
                j+=1
                continue
        else:
            if j+i*300==1500:
                break
            if label[j + rangeset[i - 1]] == originSet[j + i * 300]:
                correct[i][j] = 1
                j += 1
                continue
            else:
                correct[i][j] = 0
                j += 1
                continue

#########################[k-means]##################################
print("------------------------<kmeans clustering>----------------------------")
print(np.shape(A),np.shape(B),np.shape(C),np.shape(D),np.shape(E))
print("-------------------------<Maximum applied>-----------------------------")
print(np.shape(intsetA),np.shape(intsetB),np.shape(intsetC),np.shape(intsetD),np.shape(intsetE))
print("-----------------------<Print correct number>--------------------------")
print(np.sum(correct[0]),np.sum(correct[1]),np.sum(correct[2]),np.sum(correct[3]),np.sum(correct[4]))

# find = findCluster(testset,center,maxarray).reshape(-1,1) # testset
# testsetA = testset[find.ravel()==0]
# testsetB = testset[find.ravel()==1]
# testsetC = testset[find.ravel()==2]
# testsetD = testset[find.ravel()==3]
# testsetE = testset[find.ravel()==4]
# testsetF = testset[find.ravel()==5]
# find = findCluster(integratedSet_100,center,maxarray).reshape(-1,1)
# testsetA0 = integratedSet_100[find.ravel()==0]
# testsetB0 = integratedSet_100[find.ravel()==1]
# testsetC0 = integratedSet_100[find.ravel()==2]
# testsetD0 = integratedSet_100[find.ravel()==3]
# testsetE0 = integratedSet_100[find.ravel()==4]
# testsetF0 = integratedSet_100[find.ravel()==5]

fig = plt.figure()
ax = fig.gca(projection='3d')
#############< k-means cluster >################
# ax.scatter(A[:,0],A[:,1],A[:,2],color='b')
# ax.scatter(B[:,0],B[:,1],B[:,2],color='g')
# ax.scatter(C[:,0],C[:,1],C[:,2],color='r')
# ax.scatter(D[:,0],D[:,1],D[:,2],color='c')
# ax.scatter(E[:,0],E[:,1],E[:,2],color='m')

###############< new k-means cluster >############
# ax.scatter(intsetA[:,0],intsetA[:,1],intsetA[:,2],color='b') #분류된 데이터셋
# ax.scatter(intsetB[:,0],intsetB[:,1],intsetB[:,2],color='g') #분류된 데이터셋
# ax.scatter(intsetC[:,0],intsetC[:,1],intsetC[:,2],color='r') #분류된 데이터셋
# ax.scatter(intsetD[:,0],intsetD[:,1],intsetD[:,2],color='c') #분류된 데이터셋
# ax.scatter(intsetE[:,0],intsetE[:,1],intsetE[:,2],color='m') #분류된 데이터셋
# ax.scatter(intsetF[:,0],intsetF[:,1],intsetF[:,2],color='k') #포함되지 않은 데이터셋

# ax.scatter(center[:,0],center[:,1],center[:,2],marker = 's',color='b',s = 100)
# ax.scatter(center[0,0],center[0,1],center[0,2],color = 'b')
# ax.scatter(center[1,0],center[1,1],center[1,2],color = 'g')
# ax.scatter(center[2,0],center[2,1],center[2,2],color = 'r')
# ax.scatter(center[3,0],center[3,1],center[3,2],color = 'c')
# ax.scatter(center[4,0],center[4,1],center[4,2],color = 'm')


#############< original >################
ax.scatter(set1[:,0],set1[:,1],set1[:,2],color='b')
ax.scatter(set2[:,0],set2[:,1],set2[:,2],color='g')
ax.scatter(set3[:,0],set3[:,1],set3[:,2],color='r')
ax.scatter(set4[:,0],set4[:,1],set4[:,2],color='c')
ax.scatter(set5[:,0],set5[:,1],set5[:,2],color='m')

plt.grid(True)
plt.show()