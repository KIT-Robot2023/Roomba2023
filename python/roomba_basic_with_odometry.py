#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考


import numpy as np
import math
import time
import serial

#########################################################
RB_PORT = "COM6"#シリアルポート設定
#########################################################

'''シリアル通信用変数'''
RB_LEFT_ENC = 43 #左エンコーダカウント
RB_RIGHT_ENC = 44 #//右エンコーダカウント

RB_SONG  = 140 #//メロディ記憶．
RB_PLAY  = 141 #//メロディ再生．1バイトデータ必要
RB_OI_MODE  = 35 #//ルンバのモードを返す
RB_LEDS  = 139 #//LED制御

RB_VOLTAGE = 22 #バッテリー電圧
RB_CURRENT = 23 #バッテリー電圧

TIRE = 36
TREAD = 235


'''モータ入力用バイト計算関数'''
def _CalcHLByte(n):
    HB = n & 0xff00
    HB >>= 8
    LB = n & 0x00ff
    return (HB, LB)


'''モータへのPWM信号入力関数'''
def DrivePWM(ser, L_PWM, R_PWM):
    L_HB, L_LB = _CalcHLByte(L_PWM)
    R_HB, R_LB = _CalcHLByte(R_PWM)
    ser.write(bytes([146, R_HB, R_LB, L_HB, L_LB]))


'''センサ値取得関数'''
def GetSensor(ser, p_id, len, sign_flg):
    ser.write(bytes([142, p_id]))
    ser.flushInput()
    data = ser.read(len)
    return int.from_bytes(data, "big", signed=sign_flg)


'''各エンコーダ値取得関数'''
def GetEncs(ser):
    EncL = GetSensor(ser, RB_LEFT_ENC, 2, False)
    EncR = GetSensor(ser, RB_RIGHT_ENC, 2, False)
    return (EncL, EncR)


'''モード取得関数'''
def GetOIMode(ser):
    oimode = GetSensor(ser, RB_OI_MODE, 1, False)
    return (oimode)


'''赤外線センサ平均値取得関数'''
def GetBumps(ser):
    BL = GetSensor(ser, 48, 2, False)
    BR = GetSensor(ser, 49, 2, False)
    BumpC = (BR+BL)/2
    return BumpC


def odometry(ser, time_before, encoder_before, theta_now, x, y):
    time_now = time.time()
    time_difference = (time_now - time_before)/1000

    left, right = GetEncs(ser)
    encoder_now = np.array([float(left), float(right)])     #left encoder value is 0th. right encoder value is 1st.
    encoder_difference = encoder_now - encoder_before
    theta_enc_difference = (2 * math.pi  / 508.8) * encoder_difference
    omega = theta_enc_difference / time_difference
    velocity = omega * (TIRE / 1000)

    omega_now = (velocity[0] - velocity[1]) / (TREAD / 1000)
    velocity_st_now = (velocity[0] + velocity[1]) / 2

    distance = velocity_st_now * time_difference

    theta_now += omega_now * time_difference
    x += distance * math.cos(theta_now)
    y += distance * math.sin(theta_now)
    return time_now, encoder_now, theta_now, omega_now, velocity_st_now, x, y


def main():
    '''シリアル通信用変数'''
    RB_START = bytes([128])
    RB_RESET = bytes([7])
    RB_STOP  = bytes([173])
    RB_SAFE  = bytes([131])
    RB_FULL  = bytes([132])
    RB_SEEK_DOCK  = bytes([143]) #//ドックを探す
    RB_RATE = 115200

    time_before = time.time()
    encoder_before = 0
    theta_before = 0   #Roomba angle
    x = 0   #Roomba x coordinate
    y = 0   #Roomba y coordinate
    
    print("--- Roomba Control via python ---")
    #print("Start Serial Communication")
    '''シリアル通信開始'''
    ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)

    stop_flag=1
    odometry(ser, time_before, encoder_before, theta_before, x, y)
    while True:
        val=input('Input command char: ')
        #print("Input val="+val)
        speed=70
        speed_rot=50
        if stop_flag != 1:
            print("STOP MOTOR")
            stop_flag = 1
            DrivePWM(ser, 0,0)
        elif val=='0':
            print("ROT-R(0)")
            stop_flag = 0
            DrivePWM(ser, speed_rot,-speed_rot)
        elif val=='2':
            print("ROT-L(2)")
            stop_flag = 0
            DrivePWM(ser, -speed_rot,speed_rot)
        elif val=='1':
            print("FWR(1)")
            stop_flag = 0
            time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
            print("\n")
            print("odometry")
            print(f"Roomba speed is {velocity_st_now}[m/s]. Roomba rotation angular velocity is {omega_now}[rad/s]")
            print(f"Roomba angle is {theta_now}")
            print(f"current Roomba coordinates is ({x_now},{y_now})")
            time_before = time_now
            encoder_before = encoder_now
            theta_before = theta_now
            x = x_now
            y = y_now
            DrivePWM(ser, speed,speed)
            time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
            print("\n")
            print("odometry")
            print(f"Roomba speed is {velocity_st_now}[m/s]. Roomba rotation angular velocity is {omega_now}[rad/s]")
            print(f"Roomba angle is {theta_now}")
            print(f"current Roomba coordinates is ({x_now},{y_now})")
            time_before = time_now
            encoder_before = encoder_now
            theta_before = theta_now
            x = x_now
            y = y_now
        elif val=='3':
            print("BACK(3)")
            stop_flag = 0
            time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
            print("\n")
            print("odometry")
            print(f"Roomba speed is {velocity_st_now}[m/s]. Roomba rotation angular velocity is {omega_now}[rad/s]")
            print(f"Roomba angle is {theta_now}")
            print(f"current Roomba coordinates is ({x_now},{y_now})")
            time_before = time_now
            encoder_before = encoder_now
            theta_before = theta_now
            x = x_now
            y = y_now
            DrivePWM(ser, -speed,-speed)
            time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
            print("\n")
            print("odometry")
            print(f"Roomba speed is {velocity_st_now}[m/s]. Roomba rotation angular velocity is {omega_now}[rad/s]")
            print(f"Roomba angle is {theta_now}")
            print(f"current Roomba coordinates is ({x_now},{y_now})")
            time_before = time_now
            encoder_before = encoder_now
            theta_before = theta_now
            x = x_now
            y = y_now
        elif val=='d':
            print("RESET")
            stop_flag = 1
            ser.write(RB_RESET)
            str1 = ser.read(234)
            print(str1)
        elif val=='a':
            print("START")
            stop_flag = 1
            oimode1 = GetOIMode(ser)
            ser.write(RB_START)
            oimode2 = GetOIMode(ser)
            print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        elif val=='g':
            print("SAFE")
            stop_flag = 1
            oimode1 = GetOIMode(ser)
            ser.write(RB_SAFE)
            oimode2 = GetOIMode(ser)
            print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        elif val=='f':
            print("FULL")
            stop_flag = 1
            oimode1 = GetOIMode(ser)
            ser.write(RB_FULL)
            oimode2 = GetOIMode(ser)
            print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        elif val == "o":
            print("odometry")
            stop_flag = 1
            time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
            print("\n")
            print("odometry")
            print(f"Roomba speed is {velocity_st_now}[m/s]. Roomba rotation angular velocity is {omega_now}[rad/s]")
            print(f"Roomba angle is {theta_now}")
            print(f"current Roomba coordinates is ({x_now},{y_now})")
            time_before = time_now
            encoder_before = encoder_now
            theta_before = theta_now
            x = x_now
            y = y_now
        elif val=='w':
            print("DOCK")
            ser.write(RB_SEEK_DOCK)
        elif val=='z':
            print("SENSOR")
            el,er = GetEncs(ser)
            oimode = GetOIMode(ser)
            vol = GetSensor(ser, RB_VOLTAGE, 2, False)
            cur = GetSensor(ser, RB_CURRENT, 2, False)
            
            print("Enc L:"+str(el)+" R:"+str(er))
            print("OIMode:"+str(oimode))
            print("Votage/Current ="+str(vol)+"[mV]/"+str(cur)+"[mA]")

        else:
            print("Input val="+val)

        time_now, encoder_now, theta_now, omega_now, velocity_st_now, x_now, y_now = odometry(ser, time_before, encoder_before, theta_before, x, y)
        time_before = time_now
        encoder_before = encoder_now
        theta_before = theta_now
        x = x_now
        y = y_now
            
main()
