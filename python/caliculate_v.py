
import numpy as np
import math
import time
import serial
import keyboard

#########################################################
RB_PORT = "COM5"#シリアルポート設定
#########################################################

def GetOIMode(ser):
    oimode = GetSensor(ser, RB_OI_MODE, 1, False)
    
    return (oimode)

def DrivePWM(ser, L_PWM, R_PWM):
    L_HB, L_LB = _CalcHLByte(L_PWM)
    R_HB, R_LB = _CalcHLByte(R_PWM)
            
    ser.write(bytes([146, R_HB, R_LB, L_HB, L_LB]))

def GetEncs(ser):
    EncL = GetSensor(ser, RB_LEFT_ENC, 2, False)
    EncR = GetSensor(ser, RB_RIGHT_ENC, 2, False)
    
    return (EncL, EncR)

def GetSensor(ser, p_id, len, sign_flg):
    ser.write(bytes([142, p_id]))
    ser.flushInput()
    data = ser.read(len)
    
    return int.from_bytes(data, "big", signed=sign_flg)

def _CalcHLByte(n):
    HB = n & 0xff00
    HB >>= 8
    LB = n & 0x00ff
    
    return (HB, LB)

def caliculate_theta(dEncL,dEncR):
    #L_length=2*math.pi*r*dEncL/508.8
    L_theta=2*math.pi*dEncL/508.8
    #R_length=2*math.pi*r*dEncR/508.8
    R_theta=2*math.pi*dEncR/508.8    
    return (L_theta,R_theta)

def omega(dEncL,dEncR):
    L_theta,R_theta=caliculate_theta(dEncL,dEncR)
    omegaL=L_theta/2
    omegaR=R_theta/2
    
    vr=r*omegaR
    vl=r*omegaL
    
    return (omegaL,omegaR,vr,vl)

def caliculate_v(vr,vl):
    vt=(vr+vl)/2    
    return vt

def calivulate_omega(vr,vl):
    omegav=(vr+vl)/T
    
    return omegav

def calculate_distances(vr, vl, t):
    distance_right = t * vr
    distance_left = t * vl
    return distance_right, distance_left

    



'''シリアル通信用変数'''
RB_LEFT_ENC = 43 #左エンコーダカウント
RB_RIGHT_ENC = 44 #//右エンコーダカウント

RB_SONG  = 140 #//メロディ記憶．
RB_PLAY  = 141 #//メロディ再生．1バイトデータ必要
RB_OI_MODE  = 35 #//ルンバのモードを返す
RB_LEDS  = 139 #//LED制御

RB_VOLTAGE = 22 #バッテリー電圧
RB_CURRENT = 23 #バッテリー電圧

RB_START = bytes([128])
RB_RESET = bytes([7])
RB_STOP  = bytes([173])
RB_SAFE  = bytes([131])
RB_FULL  = bytes([132])
RB_SEEK_DOCK  = bytes([143]) #//ドックを探す
RB_RATE = 115200
    
r=36
T=235
    
print("--- Roomba Control via python ---")
'''シリアル通信開始'''
ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)

stop_flag=1
oimode1 = GetOIMode(ser)
ser.write(RB_START)
oimode2 = GetOIMode(ser)

 
oimode1 = GetOIMode(ser)
ser.write(RB_SAFE)
oimode2 = GetOIMode(ser)

start=time.time()


speed=70
speed_rot=50
stop_flag = 0
    
cstart=time.time()
DrivePWM(ser, speed,speed)
EncL0, EncR0 = GetEncs(ser)
t=time.sleep(2)
EncL1,EncR1=GetEncs(ser)
dEncL=EncL1-EncL0
dEncR=EncR1-EncR0
omegaL,omegaR,vr,vl=omega(dEncL,dEncR)
vt=caliculate_v(vr,vl)
omegav=calivulate_omega(vr,vl)
dr,dl=calculate_distances(vr, vl, t)
print(f"ω_L: {omegaL}, ω_R: {omegaR}, vr: {vr},vl: {vl},vt:{vt},ω:{omegav}")
print(f"dr:{dr},dl:{dl}")
DrivePWM(ser, 0,0)
