import numpy as np
import cv2

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
cv2.createTrackbar('delta','image',100,100,nothing)
cv2.createTrackbar('R','image',123,255,nothing)
cv2.createTrackbar('G','image',95,255,nothing)
cv2.createTrackbar('B','image',17,255,nothing)
cv2.createTrackbar('L','image',234,255,nothing)

def ImgProc(img):
    h,w = img.shape[:2]
    scalar = np.zeros((h,w), np.float32)
    r_c = np.zeros((h,w), np.uint8)
    g_c = np.zeros((h,w), np.uint8)
    b_c = np.zeros((h,w), np.uint8)
    l_c = np.zeros((h,w), np.uint8)
    r=img[:,:,2]
    g=img[:,:,1]
    b=img[:,:,0]

    #thresh = 120
    #tr = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    #tr = cv2.cvtColor(tr, cv2.COLOR_BGR2GRAY)
    #a_min = cv2.getTrackbarPos('min','image')
    delta = cv2.getTrackbarPos('delta','image')
    r_d = np.float32(cv2.getTrackbarPos('R','image'))
    g_d = np.float32(cv2.getTrackbarPos('G','image'))
    b_d = np.float32(cv2.getTrackbarPos('B','image'))
    lum_d = np.float32(cv2.getTrackbarPos('L','image'))

    scalar.fill(delta)
    r_c.fill(r_d)
    g_c.fill(g_d)
    b_c.fill(b_d)
    l_c.fill(lum_d)

    luma = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    lmax = luma.__lt__(l_c.__add__(scalar))
    lmin = luma.__gt__(l_c.__sub__(scalar))
    l_bool = lmax.__and__(lmin)

    r_y = r.astype(np.float32).__sub__(luma.astype(np.float32))
    g_y = g.astype(np.float32).__sub__(luma.astype(np.float32))
    b_y = b.astype(np.float32).__sub__(luma.astype(np.float32))

    rmax = r_y.__lt__(r_c.__add__(scalar))
    rmin = r_y.__gt__(r_c.__sub__(scalar))
    r_bool = rmax.__and__(rmin)

    gmax = g_y.__lt__(g_c.__add__(scalar))
    gmin = g_y.__gt__(g_c.__sub__(scalar))
    g_bool = gmax.__and__(gmin)

    bmax = b_y.__lt__(b_c.__add__(scalar))
    bmin = b_y.__gt__(b_c.__sub__(scalar))
    b_bool = bmax.__and__(bmin)

    mix_bool = r_bool.__and__(g_bool).__and__(b_bool).__and__(l_bool).astype(np.uint8)



    #gb_max_bool = g.__gt__(b)
    #gr_max_bool = g.__gt__(r)
    #gmax_bool = gb_max_bool.__and__(gr_max_bool)

    #rg_max = rmax_bool.____(gmax_bool).astype(np.uint8)

    rg_max_rgb = cv2.cvtColor(mix_bool, cv2.COLOR_GRAY2BGR)

    img_mod = img.__mul__(rg_max_rgb)


    borderK = np.array([[ 0, 0, 0, 0, 0],
                        [ 0, 0, 2, 0, 0],
                        [ 0, 2, -8, 2, 0],
                        [ 0, 0, 2, 0, 0],
                        [ 0, 0, 0, 0, 0]])
    res = cv2.filter2D(img_mod, -1, borderK)


    img_mod_gray = cv2.cvtColor(img_mod, cv2.COLOR_BGR2GRAY)


    max_area=100
    draw = False

    contours, hierarchy = cv2.findContours(img_mod_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            draw = True
            max_area=area
            ci=i
    if(draw):
		cnt=contours[ci]
		hull = cv2.convexHull(cnt)
		cv2.drawContours(img,[cnt],0,(0,255,0),2)
		cv2.drawContours(img,[hull],0,(0,0,255),2)


    #tr = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    #scalar.fill(a_max)
    #res = tr.__gt__(scalar).astype(np.float32)
    #res = r.__gt__(b).astype(np.float32).__mul__(tr)
    return img


while(1):
    ret, frame = cap.read()

    frame = ImgProc(frame)

    cv2.imshow('image',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()