import numpy as np
import math
import time
import serial
import keyboard
import matplotlib.pyplot as plt

# Constants and initial settings
RB_PORT = "COM7"  # Serial port setting
r = 36  # Radius of the wheel (mm)
T = 235  # Distance between wheels (mm)

# Roomba control commands
RB_LEFT_ENC = 43  # Left encoder count
RB_RIGHT_ENC = 44  # Right encoder count
RB_OI_MODE = 35  # Roomba mode
RB_START = bytes([128])
RB_SAFE = bytes([131])
RB_FULL = bytes([132])
RB_STOP = bytes([173])
RB_RATE = 115200  # Baud rate for serial communication

def GetOIMode(ser):
    return GetSensor(ser, RB_OI_MODE, 1, False)

def DrivePWM(ser, L_PWM, R_PWM):
    L_HB, L_LB = _CalcHLByte(L_PWM)
    R_HB, R_LB = _CalcHLByte(R_PWM)          
    ser.write(bytes([146, R_HB, R_LB, L_HB, L_LB]))

def GetEncs(ser):
    EncL = GetSensor(ser, RB_LEFT_ENC, 2, False)
    EncR = GetSensor(ser, RB_RIGHT_ENC, 2, False)
    return (EncL, EncR)

def GetSensor(ser, p_id, length, sign_flg):
    ser.write(bytes([142, p_id]))
    ser.flushInput()
    data = ser.read(length)
    return int.from_bytes(data, "big", signed=sign_flg)

def _CalcHLByte(value):
    HB = (value >> 8) & 0xFF
    LB = value & 0xFF
    return (HB, LB)

def calculate_theta(dEncL, dEncR):
    L_theta = 2 * math.pi * dEncL / 508.8
    R_theta = 2 * math.pi * dEncR / 508.8    
    return (L_theta, R_theta)


def calculate_rotation(dEncL, dEncR, t):
    L_theta, R_theta = calculate_theta(dEncL, dEncR)
    omegaL = L_theta / t
    omegaR = R_theta / t
    vr = r * omegaR
    vl = r * omegaL
    vt = (vr + vl) / 2
    omegav = (vr - vl) / T
    dtheta = omegav * t
    #dtheta=math.degrees(dtheta)
    distance=vt*t
    move_x=distance*math.cos(dtheta)
    move_y=distance*math.sin(dtheta)
    return dtheta,move_x,move_y,distance

def calculate_target_position(Gx, Gy):
    Gtheta = math.atan2(Gy, Gx)
    #Gtheta=math.degrees(Gtheta)
    Gdistance = math.sqrt(Gx**2 + Gy**2)
    print(Gtheta)
    dx=Gdistance*math.cos(Gtheta)
    dy=Gdistance*math.sin(Gtheta)
    NEn_dis = Gdistance * 508.8 / (2 * math.pi * r)
    NEn_theta = Gtheta * 508.8 / (2 * math.pi)
    return Gdistance, Gtheta,dx,dy

def calculate_target_En(Gx, Gy):
    Gtheta = math.atan2(Gy, Gx)
    Gdistance = math.sqrt(Gx**2 + Gy**2)
    NEnR_dis = abs(Gdistance * 508.8 / (2 * math.pi * r))
    NEnR_theta = abs(Gtheta * 508.8 / (2 * math.pi))
    NEnL_dis = abs(Gdistance * 508.8 / (2 * math.pi * r))
    NEnL_theta = abs(Gtheta * 508.8 / (2 * math.pi))    
    return NEnR_dis,NEnR_theta,NEnL_dis,NEnL_theta

# Initialize serial communication
ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)
ser.write(RB_START)
ser.write(RB_SAFE)

def make_graph(x_list,y_list,theta_list,time_list):
    fig = plt.figure(figsize = (10,6), facecolor='lightblue')
    
    #グラフを描画するsubplot領域を作成。
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)


    ax1.plot(time_list,x_list,label='List X')
    ax2.plot(time_list,y_list,label='List Y')
    ax3.plot(time_list, theta_list,label='List theta')

    plt.show()

def make_graph_cal(GEncL,GEncR,t):
                
    x_list=[]
    y_list=[]
    theta_c, move_x, move_y, Cdistance = calculate_rotation(GEncL, GEncR, t)
    x_list.append(move_x)
    y_list.append(move_y)
    
    return x_list,y_list,theta_c
    

def main():
    x_list=[]
    y_list=[]
    x1_list=[]
    y1_list=[]
    theta_list=[]   
    time_list=[]
    BGx=[]
    BGy=[]
    Btheta=[]
    Ntheta, move_x,theta_c,Cdistance,active_time,Nx,Ny = 0, 0, 0, 0,0,0,0
    coordinates = []
    num_coordinates = int(input("Enter the number of coordinates: "))
    
    for _ in range(num_coordinates):
        Gx, Gy = map(int, input("Enter target coordinates (Gx, Gy): ").split())
        coordinates.append((Gx, Gy))
    
    for Gx, Gy in coordinates:
        Gx=Gx-sum(BGx)
        Gy=Gy-sum(BGy)
        distance, dtheta, dx, dy = calculate_target_position(Gx, Gy)
        dtheta=dtheta-sum(Btheta)
        Ntheta = dtheta
        #Nx = dx
        #Ny = dy

        EncL0, EncR0 = GetEncs(ser)
        EncL,EncR=EncL0,EncR0
        
        speed = 140
        speed_rot = 50
        previous_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = max(current_time - previous_time, 0.001)
            previous_time = current_time
            active_time +=elapsed_time

            EncL1, EncR1 = GetEncs(ser)
            dEncL = EncL1 - EncL
            dEncR = EncR1 - EncR
            EncL = EncL1
            EncR = EncR1
            
            GEncL=EncL1-EncL0
            GEncR=EncR1-EncR0
            
            x1,y1,thetax=make_graph_cal(GEncL,GEncR,elapsed_time)
            x1_list.append(x1)
            y1_list.append(y1)
            theta_list.append(thetax)
                       
            
            theta_c, move_x, move_y, Cdistance = calculate_rotation(dEncL, dEncR, elapsed_time)
            move_x=math.cos(theta_c)*Cdistance
            move_y=math.sin(theta_c)*Cdistance
            Nx=Nx+move_x
            Ny=Ny+move_y
            x_list.append(Nx)
            y_list.append(Ny)
            time_list.append(active_time)
            
            distance = distance - Cdistance

            # Rotate the robot
            if abs(Ntheta) > 0.01:  # Threshold for rotation
                if Ntheta > 0:
                    DrivePWM(ser, speed_rot, -speed_rot)
                    Ntheta = Ntheta + theta_c
                elif Ntheta < 0:
                    DrivePWM(ser, -speed_rot, speed_rot)
                    Ntheta = Ntheta + theta_c
            else:
                # Move towards the target
                DrivePWM(ser, speed, speed)

            # Update current position

            # Check if target is reached
            if abs(distance) < 10:  # abs(Nx) < 30 and abs(Ny) < 30:
                DrivePWM(ser, 0, 0)  # Stop the robo
                print("finish move to target")
                print(f"x_list{x1_list}\n\ny_list{y1_list}\n\ntheta_list{theta_list}")
                break
        BGx.append(Gx)
        BGy.append(Gy)
        Btheta.append(dtheta)
    
    make_graph(x1_list,y1_list,theta_list,time_list)



if __name__ == "__main__":
    main()

