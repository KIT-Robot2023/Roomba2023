#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考


import numpy as np
import math
import time
import serial
import keyboard

#########################################################
RB_PORT = "COM10"#シリアルポート設定
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

'タイヤに対する速度制御'
def DriveVelocity(ser, vel_L, vel_R):
    L_HB, L_LB = _CalcHLByte(vel_L)
    R_HB, R_LB = _CalcHLByte(vel_R)
            
    ser.write(bytes([145, R_HB, R_LB, L_HB, L_LB]))

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


def main():
    '''シリアル通信用変数'''
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

    ser.write(RB_START)#スタート
    ser.write(RB_SAFE)#セーフ
    velocity = 200
    
    while True:

        if keyboard.is_pressed('w'):
            DriveVelocity(ser,velocity,velocity)
        elif keyboard.is_pressed('a'):
            DriveVelocity(ser,-velocity,velocity)
        elif keyboard.is_pressed('s'):
            DriveVelocity(ser,-velocity,-velocity)
        elif keyboard.is_pressed('d'):
            DriveVelocity(ser,velocity,-velocity)
        if keyboard.is_pressed('q'):
            DriveVelocity(ser,velocity/2,velocity)
        elif keyboard.is_pressed('e'):
            DriveVelocity(ser,velocity,velocity/2)
        elif keyboard.is_pressed('z'):
            DriveVelocity(ser,-velocity/2,-velocity)
        elif keyboard.is_pressed('c'):
            DriveVelocity(ser,-velocity,-velocity/2)
        else:
            DriveVelocity(ser,0,0)

        time.sleep(0.02)

main()