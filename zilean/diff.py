import cv2
import numpy as np
from os import walk

def nothing(x):
    pass

def ImgProc(new, bgn, tol):

    key =  cv2.cvtColor(bgn, cv2.COLOR_BGR2YCR_CB).astype(np.float32)
    #key =  bgn.astype(np.float32)

    color = cv2.cvtColor(new, cv2.COLOR_BGR2YCR_CB)
    #color = new

    temp = key - color

    temp2 = temp * temp

    dist = np.abs(temp[:,:,0] - temp[:,:,1] - temp[:,:,2]) * (temp2[:,:,1] + temp2[:,:,2])# + temp2[:,:,0]

    out = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

    res = dist > tol

    #return out
    return res.astype(np.uint8) * 255

cv2.namedWindow('controls')

cv2.createTrackbar('tol','controls',500,45000,nothing) #sin retro

cv2.createTrackbar('sum','controls',0,655360,nothing)



img = cv2.imread("maki/v4/img.jpg")
img = cv2.resize(img, (1024,768))
bgn = cv2.imread("maki/v4/bgn.jpg")
bgn = cv2.resize(bgn, (1024,768))

while(1):
    tol = np.float32(cv2.getTrackbarPos('tol','controls'))

    frame = ImgProc(img, bgn, tol)

    #frame[300:50+300,590:50+590] = 127

    """
    frame[:,0:170]=0
    frame[:,860:]=0
    frame[0:10,:]=0
    frame[730:,:]=0
    """


    cv2.setTrackbarPos('sum','controls',(frame == 255).sum())

    cv2.imshow('filtrado',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()