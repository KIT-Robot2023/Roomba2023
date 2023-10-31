import cv2
import numpy as np
import math

# Setup Paramater
# HSV_Param = [ [0,64,0], [30,255,255], [150,64,0], [179,255,255], [90, 64, 0], [150,255,255] ]  # Sample1
# HSV_Param = [ [0,70,0], [10,255,255], [170,70,0], [179,255,255], [110, 64, 0], [130,255,255] ]  # Sample2

# hsv_min_red1 = np.array( HSV_Param[0] )
# hsv_max_red1 = np.array( HSV_Param[1] )
# hsv_min_red2 = np.array( HSV_Param[2] )
# hsv_max_red2 = np.array( HSV_Param[3] )
# hsv_min_blue = np.array( HSV_Param[4] )
# hsv_max_blue = np.array( HSV_Param[5] )

hsv_min_orange = (90,100,10)
hsv_max_orange = (110,255,255)
hsv_min_green = (58,60,100)
hsv_max_green = (70,255,255)

PointOrder_lst = ['1','4','2','3']

# Take Photo and Image Processing, Make Image-Feature Function
def CircleDetection(Img):

    Color = Img
    Hsv = cv2.cvtColor(Color, cv2.COLOR_RGB2HSV)

    mask_green = cv2.inRange(Hsv, hsv_min_green, hsv_max_green)

    mask_orange = cv2.inRange(Hsv, hsv_min_orange, hsv_max_orange)

    Binari = mask_green + mask_orange

    contours, hierarchy = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Circles = len(contours)
    Param_lst = []
    
    if Circles >= 4:

        for i in range(Circles):
            (x, y), radius= cv2.minEnclosingCircle(contours[i])
            x = int(x)
            y = int(y)
            radius = int(radius)

            # b, g, r = Color[y, x]
            # if b < r:
            #     color = "Red"
            # elif b > r:
            #     color = "Blue"
            # else:
            #     color = "None"

            Param_lst.append([x, y, radius])
        
        Param_lst.sort(reverse = True, key = lambda x: x[2])
        del Param_lst[4:]
        
        for i in range(4):
            if i == 0:
                norm = 0
            else:
                y = Param_lst[i][0] - Param_lst[0][0]
                x = Param_lst[i][1] - Param_lst[0][1]
                norm = np.uint32( math.sqrt( y*y + x*x ) )
            Param_lst[i].append(norm)
            
        Param_lst.sort(reverse = False, key = lambda x : x[3])

        cv2.putText(Color, PointOrder_lst[0], (Param_lst[0][0]-120, Param_lst[0][1]-120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        cv2.putText(Color, PointOrder_lst[1], (Param_lst[1][0]-120, Param_lst[1][1]+120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        cv2.putText(Color, PointOrder_lst[2], (Param_lst[2][0]+120, Param_lst[2][1]-120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        cv2.putText(Color, PointOrder_lst[3], (Param_lst[3][0]+120, Param_lst[3][1]+120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)

        for i in range(4):
            cv2.circle(Color, (Param_lst[i][1],Param_lst[i][2]), Param_lst[i][3], (0,255,0), 8)
            cv2.circle(Color, (Param_lst[i][1],Param_lst[i][2]), 5, (0,255,0), -1)

    return Color , Binari
