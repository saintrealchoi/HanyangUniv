import numpy as np
import cv2
import os
import scipy
from scipy import fftpack
import matplotlib.pyplot as plt
from PIL import Image
import random as rd

x = rd.randint(0,128)
y = rd.randint(0,128)
choice = np.array([45,96,162,226,288])
def crop(img): # 각 이미지별로 같은 x,y좌표에서의 crop을 위한 함수
    w = 64
    h = 64
    img_crop = img[y:y+h,x:x+w]
    return img_crop

def crop2(img): # 각 이미지별로 다른 x,y 좌표에서의 crop을 위한 함수
    x = rd.randint(0, 128)
    y = rd.randint(0, 128)
    w = 64
    h = 64
    img_crop = img[y:y + h, x:x + w]
    return img_crop

####################< 이미지파일 가져오기 >##########################
path = "C:\\Users\\LG\\Desktop\\pattern\\"
file_list = os.listdir(path)
N = 20 # (# of the pattern)
img_list = np.zeros((N,192,192)).astype(np.uint8)
img_list2 = np.zeros((N,64,64)).astype(np.uint8)
#np.zeros((N,1024)).astype(np.uint8)

# image read
for i,file in enumerate(file_list):
    img = cv2.imread(path+file,0)
    img_list[i]=img

fig = plt.figure()

####################< fft실험 >##########################

i = 0
j=1
p = 0

# image crop randomly
while p < 20:
    img_list2[p] = crop(img_list[p])
    p += 1

# while i < 20:
#     f = np.fft.fft2(img_list2[i])
#     fshift = np.fft.fftshift(f)
#     mag = 20*np.log(np.abs(fshift))
#     plt.subplot(5,8,j),plt.imshow(img_list2[i], cmap = 'gray')
#     plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#     plt.subplot(5,8,j+1), plt.imshow(mag, cmap='gray')
#     plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#     i+=1
#     j= i*2+1
####################< mag 분석 >##########################

# x = range(-2048,2048)
# sum = np.zeros((64,64))
# while i < 20:
#     f = np.fft.fft2(img_list2[i])
#     fshift = np.fft.fftshift(f)
#     mag = 20*np.log(np.abs(fshift))
#     mag_re = np.resize(mag,(64*64))
#     plt.xlim(-50,50)
#     sum += mag
#     plt.plot(x,mag_re)
#     i+=1
#     j= i*2+1
# plt.show()

################## <magnitude average 함수> #############################

x = range(-2048,2048) # 4096차원 magnitude 계수 살펴보기
def avgmag(img):
    avg1 = np.zeros((64,64))
    count = 0
    while count < 5:
        img2 = crop2(img)
        f = np.fft.fft2(img2)
        shifted = np.fft.fftshift(f)
        mag = 20*np.log(np.abs(shifted))
        avg1 += mag
        count += 1
    avg1 /= count
    return np.resize(avg1,(64*64))

################ <vector distance함수> ######################
def vecdis(avg,img):
    count = 0
    min2 =0
    min = 0
    while count < 10:
        img2 = crop2(img)
        f = np.fft.fft2(img2)
        vecdisshi = np.fft.fftshift(f)
        mag = 20 * np.log(np.abs(vecdisshi))
        img2_re = np.resize(mag,(64*64))
        min = np.abs((avg)-(img2_re))
        min2 += np.sum(min)
        count+=1
    return min2/count
################### < average 2함수 > ####################
def avgmag2(img1):
    avg1 = np.zeros((64,64))
    avg2 = np.zeros(5)
    count = 0
    while count < 10:
        img2 = crop2(img1)
        avg1 += img2
        count +=1
    avg1 /= count
    avg1 = np.resize(avg1,(64*64))
    count = 0
    while count < 5:
        avg2[count] = avg1[choice[count]]
        count +=1

    return avg2
###################################################

def differ(arr1,arr2):
    count = 0
    acc = 0
    while count < 5:
        acc += np.abs(arr1[count]-arr2[count])
        count += 1
    return acc
################## < recognize 함수 > #####################

def rec(img1,img2):
    ret = 0

    avg1 = avgmag(img1)
    avg2_ori = avgmag2(img1)
    avg2 = avgmag2(img1)
    avg3 = avgmag2(img2)

    thres = 0.20
    origin1 = vecdis(avg1,img1)
    pick1 = vecdis(avg1,img2)
    result = np.abs(origin1-pick1)

    origin2 = differ(avg2_ori,avg2)
    p = differ(avg2,avg3)
    # print(origin2)
    # print(p)
    # print("----------")
    # print(result)
    # print(origin1)

    if (result / origin1) < thres:
        ret+=1

    if (np.abs(p-origin2) / origin2) < 2:
        ret+=1

    return ret
#
# 45번,96번,162번,226번,288번
#########################################################

i=0
j=0


while j < 20:
    i=0
    while i < 20:
        find = rec(img_list[j], img_list[i])
        if find == 2:
            print("기준 = ",j," ", "인식대상 = ",i,"same pattern")
        else:
            print("기준 = ",j," ", "인식대상 = ",i,"different pattern")
        i += 1
    j += 1
