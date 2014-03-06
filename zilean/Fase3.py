import cv2
import numpy as np
from os import walk

def Calibrate(FileName, Margin):
    bgr = cv2.imread(FileName)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCR_CB)
    filler = hsv[130,400,:]
    hsv[:,0:170,:]=filler
    hsv[:,860:,:]=filler
    hsv[0:10,:,:]=filler
    hsv[730:,:,:]=filler

    hsv[215:293,260:345,:]=filler
    hsv[128:241,503:614,:]=filler
    hsv[340:410,530:600,:]=filler
    hsv[500:584,410:480,:]=filler

    cv2.imshow('calibration', hsv)
    
    h = [hsv[:,:,0].min()-Margin, hsv[:,:,0].max()+Margin]
    s = [hsv[:,:,1].min()-Margin, hsv[:,:,1].max()+Margin]
    v = [hsv[:,:,2].min()-Margin, hsv[:,:,2].max()+Margin]

    return h, s, v


def ImgProc(FileName, Cal):
    bgr = cv2.imread(FileName)

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCR_CB)

    pG = (bgr[:,:,1]>bgr[:,:,2]) & (bgr[:,:,1]>bgr[:,:,0])
    

    pH = (hsv[:,:,0]>Cal[0][0]) & (hsv[:,:,0]<Cal[0][1])
    pS = (hsv[:,:,1]>Cal[1][0]) & (hsv[:,:,1]<Cal[1][1])
    pV = (hsv[:,:,2]>Cal[2][0]) & (hsv[:,:,2]<Cal[2][1])

    res = pH & pS & pV | pG
    res[:,0:170]=1
    res[:,860:]=1
    res[0:10,:]=1
    res[730:,:]=1
    cv2.imshow('asd', pG.astype(np.uint8)*255)
    #cv2.imshow('peron', hsv)
    return res.astype(np.uint8)*255

"""
    ## Esto es solo para probar detectar detalles en la mano en si ##
    filler = 1 # Hay que ver la forma o bien que las clavijas no salgan, o se puedan enmascarar quizas en la calibracion
    res[215:293,260:345]=filler
    res[128:241,503:614]=filler
    res[340:410,530:600]=filler
    res[500:584,410:480]=filler
    
    res = res.astype(np.int8)
    pic = bgr[:,:,0].astype(np.uint8) * np.logical_not(res)

    return pic
"""
Cal = Calibrate("maki/IMG_20140224_213449.jpg",4)
print Cal
img = ImgProc("maki/IMG_20140224_213502.jpg", Cal)

cv2.imshow('Tuneada1', img)
cv2.waitKey()
