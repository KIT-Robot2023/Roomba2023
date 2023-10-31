
import numpy as np
import math
import time
import serial
import keyboard

#########################################################
RB_PORT = "COM5"#シリアルポート設定
#########################################################



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
    
print("--- Roomba Control via python ---")
'''シリアル通信開始'''
ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)

stop_flag=1

while True:
    speed=70
    speed_rot=50
    stop_flag = 0
    start = time.time()
    DrivePWM(ser, speed_rot,-speed_rot)
    EncL, EncR = GetEncs(ser)
    end = time.time()
    active_time = end - start
    print(f"{active_time} - Left Encoder: {EncL}, Right Encoder: {EncR}")

"""
    if keyboard.is_pressed('q'):  # Qキーが押されたら
        print("STOP MOTOR")
        DrivePWM(ser, 0,0)
        break
"""