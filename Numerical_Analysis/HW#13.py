import numpy as np
import cv2
import random as rd
import numpy.linalg as lin

def matrix(M): # x, 1로 구성된 A행렬 만들기 (6개의 샘플)
    M1 = np.zeros((6,2))
    i = range(6)
    j = range(2)
    for i in range(0,6) :
        for j in range(0,2) :
            if j == 0:
                M1[i,j] = M[i,0]
            if j == 1:
                M1[i, j] = 1

    return M1

def matrix_all(M): # x, 1로 구성된 A행렬 만들기 (12개의 샘플)
    M1 = np.zeros((12,2))
    i = range(12)
    j = range(2)
    for i in range(0,12) :
        for j in range(0,2) :
            if j == 0:
                M1[i,j] = M[i,0]
            if j == 1:
                M1[i, j] = 1

    return M1

np.random.seed(12) # 특정한 평균과, 분산을 가진 정규분포로 노이즈 생성
mu, sigma = 0, np.sqrt(2)
noise = np.random.normal(mu,sigma,size=12)

all_x = np.arange(-5,7) # 모든 샘플들을 가지고 최소제곱해를 만들기기
all_y = 2*all_x-1+noise[all_x+5]

########################### <RANSAC> #############################3
i=0
RANSAC = np.zeros((6,2))
err = 999999 # err가 최소가 될때의 최소제곱해를 구하자
count = 0

while i <924: # 경우의 수는 총 12C6 = 924
    np.random.seed(i)

    x = np.arange(-5, 7)
    pick_x = np.random.choice(x, 6, replace=False) # random으로 x를 추출
    y = 2 * pick_x - 1
    pick_y = 2 * pick_x - 1 + noise[pick_x + 5]

    find = np.sum(np.square(pick_y - y))

    if find < err: # 최소의 err를 가지는 샘플들을 찾기
        err = find
        p = 0
        q = 0
        count = i
        for p in range(0, 6):
            for q in range(0, 2):
                if q == 0:
                    RANSAC[p, q] = pick_x[p]
                else:
                    RANSAC[p,q] = pick_y[p]
    i+=1

print(count,"번째에 error가 최소인 해를 구했습니다.")
print("")
################ <RANSAC을 이용한 최소제곱해> ################
############# < Psuedo-inverse 를 이용한 최소제곱해 > ############

Amat = matrix(RANSAC) # A
AmatT = np.transpose(Amat) # At
yMat = np.array([RANSAC[:,1]]) # Y
yMatT = np.transpose(yMat) # Yt

answer = np.dot(np.dot(lin.inv(np.dot(AmatT,Amat)),AmatT),yMatT) # (inv(At X A)) X At X b ( Psuedo-inverse )

print("################ <RANSAC을 이용한 최소제곱해> ################")
print("x의 계수 : ",answer[0],"상수계수 : ",answer[1])
print("")

############## <모든 샘플들을 이용한 최소제곱해> ##############
ALL = np.zeros((12,2))
for p in range(0, 12):
    for q in range(0, 2):
        if q == 0:
            ALL[p, q] = all_x[p]
        else:
            ALL[p, q] = all_y[p]
Amat = matrix_all(ALL) # A
AmatT = np.transpose(Amat) # At
yMat = np.array([ALL[:,1]]) # Y
yMatT = np.transpose(yMat) # Yt

answer = np.dot(np.dot(lin.inv(np.dot(AmatT,Amat)),AmatT),yMatT) # (inv(At X A)) X At X b ( Psuedo-inverse )
#
print("############## <모든 샘플들을 이용한 최소제곱해> ##############")
print("x의 계수 : ",answer[0],"상수계수 : ",answer[1])