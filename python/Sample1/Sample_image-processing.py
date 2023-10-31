import ctypes
import tisgrabber as tis
import cv2
import numpy as np
import math
import socket, struct

hsv_min_green = (58,60,100)
hsv_max_green = (70,255,255)

PointOrder_lst = ['1','4','2','3']

UDP_Sender_Address = "127.0.0.1"
UDP_Sender_Port = 50000
Destination_Address = "127.0.0.1"
Destination_Port = 51000

# Take Photo and Image Processing, Make Image-Feature Function
def CircleDetection(Img):

    Color = Img
    Hsv = cv2.cvtColor(Color, cv2.COLOR_RGB2HSV)

    mask_green = cv2.inRange(Hsv, hsv_min_green, hsv_max_green)

    # mask_orange = cv2.inRange(Hsv, hsv_min_orange, hsv_max_orange)

    Binari = mask_green #+ mask_orange

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

        # cv2.putText(Color, PointOrder_lst[0], (Param_lst[0][0]-120, Param_lst[0][1]-120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        # cv2.putText(Color, PointOrder_lst[1], (Param_lst[1][0]-120, Param_lst[1][1]+120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        # cv2.putText(Color, PointOrder_lst[2], (Param_lst[2][0]+120, Param_lst[2][1]-120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)
        # cv2.putText(Color, PointOrder_lst[3], (Param_lst[3][0]+120, Param_lst[3][1]+120), cv2.FONT_HERSHEY_SIMPLEX, 3, (100,0,100), 8)

        # for i in range(4):
        #     cv2.circle(Color, (Param_lst[i][1],Param_lst[i][2]), Param_lst[i][3], (0,255,0), 8)
        #     cv2.circle(Color, (Param_lst[i][1],Param_lst[i][2]), 5, (0,255,0), -1)

    return Param_lst, Color, Binari

# ImageProcessing Function
def ImageProcess(image):

    Img = cv2.resize(image, (1280, 720))
    
    cv2.imshow('Window', Img)
    cv2.waitKey(1)

    return Img

# Set UDP-Send
# Argument 1,2 : Information of Sender (by oneself)
# Argument 3,4 : Information of Destination
def Set_UDP_Send(IP_src, Port_src, IP_dst, Port_dst):
    Address_src = (IP_src, Port_src)
    Address_dst = (IP_dst, Port_dst)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.bind(Address_src)

    # Return Socket object and Address of destination
    return Socket, Address_dst

# Main Function
def Main():
    # Import "tisgrabber_x64.dll"
    ic = ctypes.cdll.LoadLibrary("./tisgrabber_x64.dll")
    tis.declareFunctions(ic)

    # Initialize "ICImagingControl" class library
    # This function must be called only once before any other function in this library is called
    ic.IC_InitLibrary(0)

    # Create a new grabber handle
    hGrabber = ic.IC_CreateGrabber()

    # Open Device
    ic.IC_OpenVideoCaptureDevice(hGrabber, tis.T("DFK 33UX178"))

    # Check if the device is valid
    if(ic.IC_IsDevValid(hGrabber)):
        # Set videoFormat and resolution
        ic.IC_SetVideoFormat(hGrabber, tis.T("RGB32 (3072x2048)"))
        # Set framerate
        ic.IC_SetFrameRate(hGrabber, ctypes.c_float(30.0))
        # Live start
        # 1 -> Show, 0 -> Not show
        print(' Start Live')
        ic.IC_StartLive(hGrabber, 0)

        Sender_f, Destination_f = Set_UDP_Send(
            UDP_Sender_Address, UDP_Sender_Port,
            Destination_Address, Destination_Port
    )

        try:
            while True:
                if ic.IC_SnapImage(hGrabber, 2000) == tis.IC_SUCCESS:
                    # Declare variables of image description
                    Width = ctypes.c_long()
                    Height = ctypes.c_long()
                    BitsPerPixel = ctypes.c_int()
                    colorformat = ctypes.c_int()

                    # Query the values of image description
                    ic.IC_GetImageDescription(hGrabber, Width, Height,
                                                BitsPerPixel, colorformat)

                    # Calculate the buffer size
                    bpp = int(BitsPerPixel.value / 8.0)
                    buffer_size = Width.value * Height.value * BitsPerPixel.value

                    # Get the image data
                    imagePtr = ic.IC_GetImagePtr(hGrabber)

                    imagedata = ctypes.cast(imagePtr,
                                            ctypes.POINTER(ctypes.c_ubyte *
                                                            buffer_size))

                    # Create the numpy array
                    image = np.ndarray(buffer=imagedata.contents,
                                        dtype=np.uint8,
                                        shape=(Height.value,
                                                Width.value,
                                                bpp))

                    # Apply some OpenCV functions on the image
                    image = cv2.flip(image, 0)
                    
                    # ImageProcessing
                    image = ImageProcess(image)
                    Param_list, Color, Binary = CircleDetection(image)

                    if len(Param_list) == 8:
                        # Pack Send-Data
                        SendData_f = struct.pack(
                            'ffffffff',
                            float( Param_list[0] ),
                            float( Param_list[1] ),
                            float( Param_list[4] ),
                            float( Param_list[5] ),
                            float( Param_list[6] ),
                            float( Param_list[7] ),
                            float( Param_list[2] ),
                            float( Param_list[3] )
                        )
                        
                        # Send data with UDP
                        Sender_f.sendto(SendData_f, Destination_f)
                    
                else:
                    print("No frame received in 2 seconds.")

        except KeyboardInterrupt:
            print(' KeyboardInterrupt')

        finally:
            print(' Stop Live')
            ic.IC_StopLive(hGrabber)

    else:
        ic.IC_MsgBox(tis.T("No device opened"), tis.T("Simple Live Video"))

    ic.IC_ReleaseGrabber(hGrabber)
    print(' Finish')

if __name__ == '__main__':
    Main()