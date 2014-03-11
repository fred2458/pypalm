import cv2
import numpy as np
from os import walk


def LumAdapt(new, cal):
    lum_cal = cv2.cvtColor(cal, cv2.COLOR_BGR2GRAY)
    lum_new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    adapt = (lum_cal.astype(np.float32) / lum_new)
    h,w = new.shape[:2]
    ret = np.zeros((h,w,3), np.float32)
    ret[:,:,0] = adapt
    ret[:,:,1] = adapt
    ret[:,:,2] = adapt
    return ret


def ImgProc(new, cal, adapt):

    bgr = new * adapt
    cv2.imshow('cal', cal)
    cv2.imshow('InAdapted', new)
    cv2.imshow('adapted', bgr.astype(np.uint8))


    g = cal[:,:,1].astype(np.float32) - bgr[:,:,1].astype(np.float32)
    r = bgr[:,:,2].astype(np.float32) - cal[:,:,2].astype(np.float32)
    b = cal[:,:,0].astype(np.float32) - bgr[:,:,0].astype(np.float32)
    B = np.abs(b) < 35
    G = np.abs(g) < 10
    R = np.abs(r) < 35

    res = B & G & R
    bgr[:,:,0] = 0
    bgr[:,:,1] = 0

    cal[:,:,0] = 0
    cal[:,:,1] = 0



    return res.astype(np.uint8) * 255

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


bgr = cv2.imread("maki/loco.jpg")
cal = cv2.imread("maki/peron.jpg")


adapt = LumAdapt(bgr, cal)

img = ImgProc(bgr, cal, adapt)

cv2.imshow('Tuneada1', img)
cv2.waitKey()
