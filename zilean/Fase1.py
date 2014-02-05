import cv2
import numpy as np

img = cv2.imread('NicoNoche.jpg')
cv2.imshow('Original', img)

h,w = img.shape[:2]

img2 = np.zeros((h,w,1), np.uint8)

for y in range(h):
    for x in range(w):
        r = img[y,x][2]
        g = img[y,x][1]
        img2[y,x] =  (r > g) * 255

cv2.imshow('Filtrada', img2)

while True:
    ch = 0xFF & cv2.waitKey()
    
    if ch == 27:
        break
cv2.destroyAllWindows()
