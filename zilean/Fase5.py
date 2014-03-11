import cv2
import numpy as np
from os import walk

def nothing(x):
    pass

def ImgProc(new, key, tol, defo):

    h,w = new.shape[:2]
    keym = np.zeros((h,w,3), np.float32)
    keym[:,:,:] = key

    color = cv2.cvtColor(new, cv2.COLOR_BGR2YCR_CB)

    print color[300,590]

    temp = keym - color


    temp2 = temp * temp

    dist = temp2[:,:,1] + temp2[:,:,2]# + temp2[:,:,0] * defo[0]

    out = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

    res = dist < tol

    return res.astype(np.uint8) * 255

cv2.namedWindow('controls')
cv2.createTrackbar('k_Y','controls',0,255,nothing)
#cv2.createTrackbar('k_Cb','controls',51,255,nothing) #retro
#cv2.createTrackbar('k_Cr','controls',185,255,nothing) #retro
#cv2.createTrackbar('tol','controls',5000,15000,nothing) #retro


#455 321

cv2.createTrackbar('k_Cb','controls',92,255,nothing) #sin retro
cv2.createTrackbar('k_Cr','controls',125,255,nothing) #sin retro
cv2.createTrackbar('tol','controls',500,45000,nothing) #sin retro


cv2.createTrackbar('k_u','controls',65535,65535,nothing)
cv2.createTrackbar('k_v','controls',65535,65535,nothing)

cv2.createTrackbar('sum','controls',0,655360,nothing)


img = cv2.imread("maki/v4/DSC_0402.jpg")
img = cv2.resize(img, (1024,768))

while(1):
    
    k_Y = np.uint8(cv2.getTrackbarPos('k_Y','controls'))
    k_Cb = np.uint8(cv2.getTrackbarPos('k_Cb','controls'))
    k_Cr = np.uint8(cv2.getTrackbarPos('k_Cr','controls'))
    tol = np.float32(cv2.getTrackbarPos('tol','controls'))

    k_u = np.float32(cv2.getTrackbarPos('k_u','controls'))/65535
    k_v = np.float32(cv2.getTrackbarPos('k_v','controls'))/65535

    frame = ImgProc(img, (k_Y,k_Cb,k_Cr), tol, (0,k_u,k_v))

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