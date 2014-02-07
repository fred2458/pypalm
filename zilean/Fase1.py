import cv2
import numpy as np
import time as t

img = cv2.imread('Ariel 2.jpg')


h,w = img.shape[:2]

img3 = np.zeros((h,w,1), np.uint8)


r=img[:,:,2]
g=img[:,:,1]
img2 = r.__gt__(g).astype(np.uint8)*255

<<<<<<< HEAD
kernel = np.array([[ 0, 0, 1, 0, 0],
				   [ 0, 0, 1, 0, 0],
          		   [ 1, 1,-8, 1, 1],
          		   [ 0, 0, 1, 0, 0],
          		   [ 0, 0, 1, 0, 0]])
=======
borderK = np.array([[ 0, 0, 0, 0, 0],
                    [ 0, 0, 1, 0, 0],
                    [ 0, 1, -4, 1, 0],
                    [ 0, 0, 1, 0, 0],
                    [ 0, 0, 0, 0, 0]])
>>>>>>> a0d3c809e78d057c7f0079d4ac20641acefa7b1b

diffK = np.array([[ 1, 1, 1],
                  [ 1, 1, 1],
                  [ 1, 1, 1]])

cv2.filter2D(img2, -1, borderK, img3)
cv2.filter2D(img3, -1, diffK, img3)

cv2.imshow('Original', img)
cv2.imshow('Filtrada', img2)
cv2.imshow('Tuneada', img3)

exit
while True:
    ch = 0xFF & cv2.waitKey()
    
    if ch == 27:
        break
cv2.destroyAllWindows()




