import numpy as np
import cv2
import os
import scipy
from scipy import fftpack
import matplotlib.pyplot as plt
from PIL import Image
import random as rd

N = 10
r_b_co = np.zeros(N)
r_g_co = np.zeros(N)
b_g_co = np.zeros(N)
y_u_co = np.zeros(N)
y_v_co = np.zeros(N)
u_v_co = np.zeros(N)


def RGB2YUV(bgr):
    m = np.array([[0.29900 ,-0.14713,0.61500],
                  [0.58700,-0.28886,-0.51499],
                  [0.11400,0.43600,-0.10001]])
    yuv = np.dot(bgr, m)
    yuv[:,:,1:] += 128.0
    return yuv

####################< 이미지파일 가져오기 >##########################
path = "C:\\Users\\LG\\Desktop\\Image\\"
file_list = os.listdir(path)
img_list = np.zeros((N,192,192,3)).astype(np.uint8)

red_list = np.zeros((N,192,192,3)).astype(np.uint8)
green_list = np.zeros((N,192,192,3)).astype(np.uint8)
blue_list = np.zeros((N,192,192,3)).astype(np.uint8)

y_list = np.zeros((N,192,192)).astype(np.uint8)
u_list = np.zeros((N,192,192)).astype(np.uint8)
v_list = np.zeros((N,192,192)).astype(np.uint8)

for i,file in enumerate(file_list):
    bgr = cv2.imread(path+file)
    img = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    img_list[i]=img
a,b,c = cv2.split(img_list[0])

count = 0
while count < 10:
    red_list[count] = img_list[count].copy() # 2번
    red_list[count][:,:,1] = 0
    red_list[count][:,:,2] = 0

    blue_list[count] = img_list[count].copy() # 0번
    blue_list[count][:, :, 0] = 0
    blue_list[count][:, :, 1] = 0

    green_list[count] = img_list[count].copy() # 1번
    green_list[count][:, :, 0] = 0
    green_list[count][:, :, 2] = 0

    y_list[count] = RGB2YUV(img_list[count])[:,:,0]
    u_list[count] = RGB2YUV(img_list[count])[:,:,1]
    v_list[count] = RGB2YUV(img_list[count])[:,:,2]
    count += 1
print(RGB2YUV(img_list[0]))
print(cv2.cvtColor(img_list[0],cv2.COLOR_RGB2YUV))
def correl(x,y):
    meanx = np.mean(x)
    meany = np.mean(y)
    stdx = np.std(x)
    stdy = np.std(y)
    ret = (np.mean((x-meanx)*(y-meany)))/(stdx*stdy)
    return ret


count = 0
while count < 10:
    r_b_co[count] = correl(red_list[count][:,:,0],blue_list[count][:,:,2])
    r_g_co[count] = correl(red_list[count][:,:,0],green_list[count][:,:,1])
    b_g_co[count] = correl(blue_list[count][:,:,2],green_list[count][:,:,1])
    y_u_co[count] = correl(y_list[count],u_list[count])
    y_v_co[count] = correl(y_list[count],v_list[count])
    u_v_co[count] = correl(u_list[count],v_list[count])
    count +=1

count = 0
while count < 10:
    print(r_b_co[count],end='  ')
    print(r_g_co[count],end='  ')
    print(b_g_co[count],end='  ')
    print(y_u_co[count], end='  ')
    print(y_v_co[count], end='  ')
    print(u_v_co[count], end='  ')
    print("")
    count +=1

plt.plot(r_b_co,'r')
plt.plot(r_g_co,'g')
plt.plot(b_g_co,'b')
plt.plot(y_u_co,'c')
plt.plot(y_v_co,'m')
plt.plot(u_v_co,'y')

plt.show()