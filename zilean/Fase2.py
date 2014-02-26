import cv2
import numpy as np
from os import walk

def ImgProc(FileName):
    img = cv2.imread(FileName)
    h,w = img.shape[:2]
    img3 = np.zeros((h,w,1), np.uint8)
    r=img[:,:,2]
    g=img[:,:,1]
    #img2 = r.__gt__(g)
    #img2 = r.__gt__(g).astype(np.float32)
    img2 = r.__ge__(g*0.8)

    img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) < 70
    
    res = img2.__or__(img3).astype(np.float32)

    res[:,0:200]=0
    res[:,800:]=0
    res[0:10,:]=0



    """
    borderK = np.array([[ 0, 0, 0, 0, 0],
                        [ 0, 0, 1, 0, 0],
                        [ 0, 1, -4, 1, 0],
                        [ 0, 0, 1, 0, 0],
                        [ 0, 0, 0, 0, 0]])
    diffK = np.array([[ 1, 1, 1],
                      [ 1, 1, 1],
                      [ 1, 1, 1]])
    cv2.filter2D(img2, -1, borderK, img3)
    cv2.filter2D(img3, -1, diffK, img3)
    """

    return res

def resta(img1, img2):
    return img1.__sub__(img2)

dirpath, dirnames, filenames = list(walk("./maki"))[0]

for filename in filenames:
    img = np.abs(resta(ImgProc("maki/IMG_20140224_213716.jpg"), ImgProc("maki/" + filename)))
    var = np.var(img)
    media = np.mean(img)
    if media < 0.025:
        print "-------------------------------------------------"
        print "Contra: ", filename
        print "Varianza: ", var
        print "Media: ", media
        print "Std: ", np.std(img)
#cv2.imshow('1-2', img)
cv2.waitKey()

"""

File1 = './maki/IMG_20140224_213716.jpg'
File2 = './maki/IMG_20140224_213716.jpg'
Img1 = ImgProc(File1)
Img2 = ImgProc(File2)

#Img1[:,0:200]=0
cv2.imshow('Tuneada', Img1)
#cv2.imshow('Tuneada1', Img2)
#cv2.imshow('Img1', np.abs(Img1))
#cv2.imshow('Img2', np.abs(Img2))
#cv2.imshow('1-2', np.abs(Img1-Img2))
#cv2.imshow('2-1', np.abs(Img2-Img1))
print File1 + '-' + File2 + ': ' + str(np.var(np.abs(Img1-Img2)))
cv2.waitKey()
"""