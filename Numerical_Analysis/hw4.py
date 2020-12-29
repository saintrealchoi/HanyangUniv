import numpy as np
import numpy.linalg as lin

M = np.array([[-2.9,35.4],
              [-2.1,19.7],
              [-0.9,5.7],
              [1.1,2.1],
              [0.1,1.2],
              [1.9,8.7]]) # 첫번째 예시

M = np.array([[4.0,41.5],
              [3.1,25.7],
              [-0.9,5.7],
              [-2.9,35.4],
              [0.1,1.2],
              [1.9,8.7]]) # 두번째 예시

M = np.array([[1.1,2.1],
              [3.1,25.7],
              [-0.9,5.7],
              [-2.9,35.4],
              [0.1,1.2],
              [1.9,8.7]]) # 세번째 예시

def matrix(M): # x의 제곱, x, 1로 구성된 A행렬 만들기
    M1 = np.zeros((6,3))
    i = range(6)
    j = range(3)
    for i in range(0,6) :
        for j in range(0,3) :
            if j == 0:
                M1[i,j] = M[i,0]**2
            if j == 1:
                M1[i,j] = M[i,0]
            if j == 2:
                M1[i,j] = 1
    return M1

Amat = matrix(M) # A
AmatT = np.transpose(Amat) # At
yMat = np.array([M[:,1]]) # Y
yMatT = np.transpose(yMat) # Yt

M1 = np.dot(AmatT,yMatT) # At X Yt
M2 = np.dot(AmatT,Amat) # A X At
answer = np.dot(np.dot(lin.inv(np.dot(AmatT,Amat)),AmatT),yMatT) # (inv(At X A)) X At X b ( Psuedo-inverse )

print(answer) # a,b,c