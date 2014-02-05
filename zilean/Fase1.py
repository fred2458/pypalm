import cv2
import numpy as np

img = cv2.imread('NicoNoche.jpg')
cv2.imshow('Original', img)

h,w = img.shape[:2]

#img2 = np.zeros((h,w,1), np.uint8)

r=img[:,:,2]
g=img[:,:,1]
img2 = (r>g).astype(np.uint8)*255

cv2.imshow('Filtrada', img2)

while True:
    ch = 0xFF & cv2.waitKey()
    
    if ch == 27:
        break
cv2.destroyAllWindows()
