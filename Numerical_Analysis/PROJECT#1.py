import os
import cv2
import numpy as np
################### path ##################
path = "./resize/"
file_list = os.listdir(path)
###########################################

N = 5000 #벡터공간을 생성할 이미지의 개수
train_data = np.zeros((N,1024)).astype(np.uint8) #이미지를 행벡터로 나열하여 Matrix 구성
for i,file in enumerate(file_list):
    if i == N:
        break
    img = cv2.imread(path+file)[:,:,0] #png파일의 맨마지막채널만 읽음
    train_data[i] = np.resize(img,(1024))

M = np.mean(train_data,axis=0) # mean vector
A = train_data - M # normalize
A_T = np.transpose(A,(1,0))
mat = np.matmul(A_T,A) # covariance matrix
value,vector = np.linalg.eig(mat)

############ threshold ################
index = sorted(range(len(value)), key=lambda k: value[k])
index.reverse()
total_sum = value.sum()
vec_list = []
cur_sum = 0
for i in index:
    cur_sum += value[i]
    if cur_sum/total_sum > 0.95:
        break
    vec_list.append(vector[:,i])

vec = np.array(vec_list)
c = np.zeros(len(vec_list))
img = cv2.imread(path+file_list[N+500])[:,:,0]
test = img.reshape(1024)
test = test-M

for i in range(len(vec_list)):
    c[i] = (test * vec[i]).sum()

result = np.zeros((1024))
for i in range(len(vec_list)):
    result += (c[i] * vec[i])

result+=M
result = result.reshape((32,32)).astype(np.uint8)
ret = np.concatenate((img, result), axis=0)

ret = cv2.resize(ret,(320,640),interpolation=cv2.INTER_LANCZOS4)
cv2.imshow("frame",ret)
#dst2 = cv2.resize(src, dsize=(0, 0), fx=0.3, fy=0.7, interpolation=cv2.INTER_LINEAR)
key = cv2.waitKey(0)
cv2.destroyAllWindows()