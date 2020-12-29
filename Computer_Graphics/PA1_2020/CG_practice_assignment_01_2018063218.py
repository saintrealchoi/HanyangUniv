#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples belowf

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import time
import math

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)


def size(A):
    return math.sqrt(np.dot(A,A))

def unitv(A):
    if(size(A)!=0):
        return A/size(A)
    else:
        return 9999999

def main():

    starttime=time.time()

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    # set default values
    viewDir = np.array([0,0,-1]).astype(np.float)
    viewUp = np.array([0,1,0]).astype(np.float)
    viewProjNormal = -1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0

    viewx = np.array([0, 0, 0]).astype(np.float)
    viewy = np.array([0, 0, 0]).astype(np.float)
    stype = "Sphere"
    
    scenter = np.array([0,0,0]).astype(np.float)
    sradius = 1

    minPt = np.array([0,0,0]).astype(np.float)
    maxPt = np.array([0,0,0]).astype(np.float)

    intensity = {}  # how bright the light is.
    colname = {}
    col = {}
    coltype = {}
    position = {}
    specol = {}
    exp = {}

    imgSize = np.array(root.findtext('image').split()).astype(np.int)

    print('imgSize',imgSize)
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        print('viewpoint', viewPoint)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        print('viewDir', viewDir)
        viewProjNormal = -1*viewDir
        print('viewProjNormal', viewProjNormal)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        print('viewUp', viewUp)

        tmp = c.findtext('projDistance')
        projDistance=projDistance if tmp == None else float(tmp)
        
        print('projDistance',projDistance)
        viewWidth = float(c.findtext('viewWidth'))
        print('viewWidth',viewWidth)
        viewHeight = float(c.findtext('viewHeight'))
        print('viewHeight',viewHeight)

    
    viewx = np.cross(viewDir, viewUp)
    print('viewx',viewx)
    viewy = np.cross(viewDir, viewx)
    print('viewy',viewy)

    inten = 0
    count = 0
    for c in root.findall('light'):
        position[count] = np.array(c.findtext('position').split()).astype(np.float)
        intensity[count] = np.array(c.findtext('intensity').split()).astype(np.float)
        inten = inten+intensity[count][0]
        count = count+1
    print('position', position)
    print('intensity', intensity)

    count = 0
    for c in root.findall('shader'):
        diffuseColor_c = np.array(c.findtext('diffuseColor').split()).astype(np.float)
        print('name', c.get('name'))
        print('diffuseColor c', diffuseColor_c)
                
        colname[count]=c.get('name')
        col[colname[count]]=diffuseColor_c
        coltype[colname[count]]=c.get('type')
        if(coltype[colname[count]]=='Phong'):
            specol[colname[count]]=np.array(c.findtext('specularColor').split()).astype(np.float)
            exp[colname[count]]=float(c.findtext('exponent'))
        count=count+1

    for c in root.findall('surface'):    
        stype=c.get('type')
        print('stype',stype)
        if(stype=='Sphere'):
            scenter=np.array(c.findtext('center').split()).astype(np.float)
            print('center', scenter)
            sradius=float(c.findtext('radius'))
            print('radius',sradius)
        if(stype=='Box'):
            minPt=np.array(c.findtext('minPt').split()).astype(np.float)
            print('minPt', minPt)
            maxPt=np.array(c.findtext('maxPt').split()).astype(np.float)
            print('maxPt', maxPt)

    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:] = 0

    delta = 0
    h = 0
    lmada = 0
    colt = 0
    distance = 0
    mint = 0
    p = 0
    q = 0
    plane = np.array([0,0,0]).astype(np.float)
    temp = np.array([0,0,0]).astype(np.float)

    lp = np.array([0,0,0]).astype(np.float)
    lv = np.array([0,0,0]).astype(np.float)
    ln = np.array([0,0,0]).astype(np.float)

    stypel = {}
    rcolnamel = {}
    scenterl = {}
    sradiusl = {}
    minPtl = {}
    maxPtl = {}

    count = 0
    for c in root.findall('surface'):
        stypel[count] = c.get('type')
        rcolnamel[count] = c.find('shader').get('ref')
        if(stypel[count] == 'Sphere'):
            scenterl[count] = np.array(c.findtext('center').split()).astype(np.float)
            sradiusl[count] = float(c.findtext('radius'))
        elif(stypel[count] == 'Box'):
            minPtl[count] = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPtl[count] = np.array(c.findtext('maxPt').split()).astype(np.float)
        count = count+1

    txmin=0
    tymin=0
    tzmin=0
    txmax=0
    tymax=0
    tzmax=0
    wayx=0
    wayy=0
    wayz=0
    tswap=0
    
    tmin=0
    tmax=0
    
    mycol=Color(0,0,0)
    
    rcolname=""
    realcol=""
    dot=0
    
    last=np.array([0,0,0]).astype(np.float)
    rcount=0
    
    light = 0

    # replace the code block below!
    for x in np.arange(imgSize[0]): 
        
        for y in np.arange(imgSize[1]):
            count=0
            p=((x-imgSize[0]/2)/imgSize[0])*viewWidth
            q=((y-imgSize[1]/2)/imgSize[1])*viewHeight
            mint=9999999
            plane=(unitv(viewDir)*projDistance)+(unitv(viewx)*p)+(unitv(viewy)*q)+np.array([0.00001,0.00001,0.00001]).astype(np.float)
            plane=unitv(plane) 
            for c in stypel:
                stype=stypel[count]
                rcolname=rcolnamel[count]

                if(stype=='Sphere'):

                    scenter=scenterl[count]
                    sradius=sradiusl[count]
                    temp=scenter-viewPoint

                    distance=np.dot(unitv(temp),plane)*size(temp)
                    h=size(temp)*size(temp)-distance*distance

                    if(h<sradius*sradius):
                        delta=distance-math.sqrt(sradius*sradius-h)
                        if(delta<mint):
                            mint=delta
                            realcol=rcolname
                            rcount=count
                            lp=(plane*mint)+viewPoint
     
                            ln=unitv(lp-scenter)

                if(stype=='Box'):
                    
                    minPt=minPtl[count]  
                    maxPt=maxPtl[count]

                    txmin=(minPt[0]-viewPoint[0])/(plane[0])
                    txmax=(maxPt[0]-viewPoint[0])/(plane[0])
                    if(txmin>txmax):
                        tswap=txmin
                        txmin=txmax
                        txmax=tswap
                        wayx=1
                    else:
                        wayx=-1
                    tymin=(minPt[1]-viewPoint[1])/(plane[1])
                    tymax=(maxPt[1]-viewPoint[1])/(plane[1])
                    if(tymin>tymax):
                        tswap=tymin
                        tymin=tymax
                        tymax=tswap
                        wayy=1
                    else:
                        wayy=-1
                    tzmin=(minPt[2]-viewPoint[2])/(plane[2])
                    tzmax=(maxPt[2]-viewPoint[2])/(plane[2])
                    if(tzmin>tzmax):
                        tswap=tzmin
                        tzmin=tzmax
                        tzmax=tswap
                        wayz=1
                    else:
                        wayz=-1
                    tmin=max(txmin,tymin,tzmin)
                    tmax=min(txmax,tymax,tzmax)



                    if(tmin<tmax):
                        
                        delta=size(tmin*plane)
                        if(delta<mint):
                            mint=delta
                            rcount=count
                            realcol=rcolname
                            if(tmin==txmin):
                                ln=wayx*(np.array([1,0,0]).astype(np.float))
                            elif(tmin==tymin):
                                ln=wayy*(np.array([0,1,0]).astype(np.float))
                            elif(tmin==tzmin):
                                ln=wayz*(np.array([0,0,1]).astype(np.float))

                count=count+1
            if(mint<99999): 
                lp=(plane*mint)+viewPoint
                colt=9999
                last=np.array([0,0,0]).astype(np.float)
                for cnt in range(0,len(position)):
                    count = 0
                    light = 0
                    for c in stypel:
                        stype=stypel[count]
                        rcolname=rcolnamel[count]
                        
                        if(count==rcount):
                            
                            continue

                        if(stype=='Sphere'):

                            
                            scenter=scenterl[count]
                            sradius=sradiusl[count]
                           
                            temp=scenter-lp
                            
                            distance=np.dot(unitv(position[cnt]-lp),temp)
                            if(distance<0):
                                
                                continue
                            h=size(temp)*size(temp)-distance*distance

                            if(h<sradius*sradius):
                                if((distance-math.sqrt(sradius*sradius-h))>0):
                                    light=1
                                
                                    break

                        if(stype=='Box'):

                            minPt=minPtl[count]
                            maxPt=maxPtl[count]

                            txmin=(minPt[0]-lp[0])/(position[cnt][0]-lp[0])
                            txmax=(maxPt[0]-lp[0])/(position[cnt][0]-lp[0])
                            if(txmin>txmax):
                                tswap=txmin
                                txmin=txmax
                                txmax=tswap
                            tymin=(minPt[1]-lp[1])/(position[cnt][1]-lp[1])
                            tymax=(maxPt[1]-lp[1])/(position[cnt][1]-lp[1])
                            if(tymin>tymax):
                                tswap=tymin
                                tymin=tymax
                                tymax=tswap
                            tzmin=(minPt[2]-lp[2])/(position[cnt][2]-lp[2])
                            tzmax=(maxPt[2]-lp[2])/(position[cnt][2]-lp[2])
                            if(tzmin>tzmax):
                                tswap=tzmin
                                tzmin=tzmax
                                tzmax=tswap
                            tmin=max(txmin,tymin,tzmin)
                            tmax=min(txmax,tymax,tzmax)

                            if(tmin<tmax):
                                
                                if(tmin<0):
                                    continue
                                light=1
                                
                                break

                        count=count+1
                        
                    if(light == 1):
                        last = last+np.array([0,0,0]).astype(np.float)
                    else:
                        lv = unitv(position[cnt]-lp)
                        lamda = np.dot(lv,ln)
                        if(lamda < 0):
                            lamda = 0
                        last = last+np.array([col[realcol][0]*intensity[cnt][0]*lamda,col[realcol][1]*intensity[cnt][1]*lamda,col[realcol][2]*intensity[cnt][2]*lamda]).astype(np.float)
                        
                        if(coltype[realcol]=='Phong'):


                            dot=np.dot(unitv(lv-plane),ln)
                            dot=pow(dot,exp[realcol])

                            last=last+np.array([specol[realcol][0]*intensity[cnt][0]*dot,specol[realcol][1]*intensity[cnt][1]*dot,specol[realcol][2]*intensity[cnt][2]*dot]).astype(np.float)

                mycol=Color(last[0],last[1],last[2])
                mycol.gammaCorrect(2.2)
                img[y][x]=mycol.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')

if __name__== "__main__":
    main()
