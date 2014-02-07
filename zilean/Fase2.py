import cv2
import numpy as np

def ImgProc(FileName):
    img = cv2.imread(FileName)
    h,w = img.shape[:2]
    img3 = np.zeros((h,w,1), np.uint8)
    r=img[:,:,2]
    g=img[:,:,1]
    #img2 = r.__gt__(g)
    img2 = r.__gt__(g).astype(np.float32)


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

    return img2

File1 = 'A1.jpg'
File2 = 'N6.jpg'
Img1 = ImgProc(File1)
Img2 = ImgProc(File2)

Img1[:,0:200]=0
Img2[:,0:200]=cv2.imshow('Tuneada', Img1)
#cv2.imshow('Tuneada1', Img2)
#cv2.imshow('Img1', np.abs(Img1))
#cv2.imshow('Img2', np.abs(Img2))
cv2.imshow('1-2', np.abs(Img1-Img2))
#cv2.imshow('2-1', np.abs(Img2-Img1))
print File1 + '-' + File2 + ': ' + str(np.var(np.abs(Img1-Img2)))
cv2.waitKey()
