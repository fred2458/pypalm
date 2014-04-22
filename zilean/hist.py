import cv2
import numpy as np

bgr = cv2.imread("maki/Ariel1.jpg")
Y = bgr#cv2.cvtColor(bgr, cv2.COLOR_BGR2YCR_CB)
h,w = bgr.shape[:2]

graf = np.zeros((256,256), np.int32)
ngraf = np.zeros((256,256), np.uint8)
for y in range(h):
    for x in range(w):
        if graf[Y[y,x,1],Y[y,x,2]] < 255: 
            graf[Y[y,x,1],Y[y,x,2]]+=1
#print graf.max()        
ngraf=(graf/graf.max()*255).astype(np.uint8)

#print ngraf.max()        
cv2.imshow('hist',ngraf)

cv2.waitKey()

