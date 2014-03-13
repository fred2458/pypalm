import cv2
import numpy as np
from os import walk

def nothing(x):
    pass


def bgcolor(bgn):
    hsv = cv2.cvtColor(bgn, cv2.COLOR_BGR2YCR_CB) 
    filler = hsv[130,400,:]
    #hsv[120:140,390:410,:] = (255,0,0)

    hsv[:,0:250,:]=filler
    hsv[:,800:,:]=filler
    hsv[0:50,:,:]=filler
    hsv[650:,:,:]=filler

    hsv[215+40:293+40,260+50:345+50,:]=filler
    hsv[128+40:241+40,503:614,:]=filler
    hsv[340:410,530:600,:]=filler
    hsv[500:584,410+40:480+40,:]=filler

    #cv2.imshow('calibration', hsv)

    return np.array([np.mean(hsv[:,:,0]).astype(np.int32), np.mean(hsv[:,:,1]).astype(np.int32), np.mean(hsv[:,:,2]).astype(np.int32)])

def handcolor(hand):
    hsv = cv2.cvtColor(hand, cv2.COLOR_BGR2YCR_CB) 

    color = hsv[230:550,270:320,:]
    
    #hsv[230:550,270:320,:] = (255,0,0)

    #cv2.imshow('calibration', hsv)

    return np.array([np.mean(color[:,:,0]).astype(np.int32), np.mean(color[:,:,1]).astype(np.int32), np.mean(color[:,:,2]).astype(np.int32)])



def ImgProc(new, key, tol, defo):

    h,w = new.shape[:2]
    keym = np.zeros((h,w,3), np.float32)
    keym[:,:,:] = key

    color = cv2.cvtColor(new, cv2.COLOR_BGR2YCR_CB)

    temp = keym - color

    temp2 = temp * temp

    dist = temp2[:,:,1] + temp2[:,:,2]# + temp2[:,:,0] * defo[0]

    out = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

    res = dist > tol

    return res.astype(np.uint8) * 255

cv2.namedWindow('controls')
cv2.createTrackbar('k_Y','controls',0,255,nothing)
#cv2.createTrackbar('k_Cb','controls',51,255,nothing) #retro
#cv2.createTrackbar('k_Cr','controls',185,255,nothing) #retro
#cv2.createTrackbar('tol','controls',5000,15000,nothing) #retro


#455 321



img = cv2.imread("maki/v4/img.jpg")
img = cv2.resize(img, (1024,768))
bgn = cv2.imread("maki/v4/bgn.jpg")
bgn = cv2.resize(bgn, (1024,768))

key = bgcolor(bgn)
hcolor = handcolor(img)
print key
print hcolor

dire = key - hcolor
dire[0] = 0
dire = dire.astype(np.float32) / np.linalg.norm(dire)
print dire


cv2.createTrackbar('k_Cr','controls',key[1] + (dire[1]*50).astype(np.int8),255,nothing) #sin retro
cv2.createTrackbar('k_Cb','controls',key[2] + (dire[2]*50).astype(np.int8),255,nothing) #sin retro
cv2.createTrackbar('tol','controls',3500,45000,nothing) #sin retro
cv2.createTrackbar('k_u','controls',65535,65535,nothing)
cv2.createTrackbar('k_v','controls',65535,65535,nothing)
cv2.createTrackbar('sum','controls',0,655360,nothing)

while(1):
    
    k_Y = np.uint8(cv2.getTrackbarPos('k_Y','controls'))
    k_Cb = np.uint8(cv2.getTrackbarPos('k_Cb','controls'))
    k_Cr = np.uint8(cv2.getTrackbarPos('k_Cr','controls'))
    tol = np.float32(cv2.getTrackbarPos('tol','controls'))

    k_u = np.float32(cv2.getTrackbarPos('k_u','controls'))/65535
    k_v = np.float32(cv2.getTrackbarPos('k_v','controls'))/65535

    frame = ImgProc(img, (k_Y,k_Cr,k_Cb), tol, (0,k_u,k_v))

    #frame[300:50+300,590:50+590] = 127



    frame[:,0:250]=0
    frame[:,800:]=0
    frame[0:50,:]=0
    frame[650:,:]=0

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