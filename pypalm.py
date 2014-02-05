import numpy as np
import cv2

cap = cv2.VideoCapture(0)

p_x = 0
p_y = 0
pf_x = 0
pf_y = 0
drawing = False

def nothing(x):
    pass

cv2.namedWindow('frame')

img = cv2.imread('zilean/NicoNoche.jpg',0)

li = img.tolist()



def pix_dif(i,j,delta):
	x_dif = abs(li[i][j]-li[i][j+delta])
	y_dif = abs(li[i][j]-li[i+delta][j])
	return x_dif + y_dif

def pix_det(i,j,delta,limit):
	cont = 0
	for dx in [-3,-2,-1,0,1,2,3]:
		for dy in [-3,-2,-1,0,1,2,3]:
			try:
				p_dif = pix_dif(i+dx,j+dy,delta)
			except IndexError:
				pass
			if p_dif > limit:
				cont += 1
	if cont > 5:
		return 255
	else:
		return 0


delta = 1
limit = 80
dif = []
for i in range(len(li) - delta):
    dif.insert(i, [])
    for j in range(len(li[i]) - delta):
        try:
            dif[i].insert(j, pix_dif(i,j,delta))
        except:
			pass
		

img = np.array(dif, np.uint8)

while(True):
    global img
    first = cv2.getTrackbarPos('first','frame')
    second = cv2.getTrackbarPos('second','frame')
    #frame = cv2.Laplacian(img,cv2.CV_64F)
    frame = img
    # write the flipped frame
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cv2.destroyAllWindows()