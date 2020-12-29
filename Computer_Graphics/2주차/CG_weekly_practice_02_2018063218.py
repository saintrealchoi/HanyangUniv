import numpy as np

M=np.arange(2,27) #2부터 26까지의 배열
print(M)
M=M.reshape(5,5) #(5,5)행렬로 reshape
print(M)
M[:,0]=0 #첫번째 열을 0으로 변경
print(M)
M=M@M #M^2
print(M)
v = M[0,:]*M[0,:] #v벡터의 각 성분의 제곱을 v에 저장
v_m = np.sqrt(v[0]+v[1]+v[2]+v[3]+v[4]) #v벡터의 크기를 v_m에 저장
print(v_m)

