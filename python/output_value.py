#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考

import numpy as np
import json
import math
import time
import serial

#########################################################
RB_PORT = "/dev/ttyUSB0"#シリアルポート設定
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

Angle_R_before = 0.0
Angle_L_before = 0.0
# 引数：エンコーダ値, 時間
def EncVelCalculation(enc, t):
    #1時刻前の値
    global Angle_R_before, Angle_L_before, delta_t
    # タイヤ半径[m]
    r = 0.036
    # 移動距離計算
    L_R = (2*math.pi*r)*(enc[0]/508.8)
    L_L = (2*math.pi*r)*(enc[1]/508.8)
    # 角度計算
    Angle_R = (2*math.pi)*(enc[0]/508.8)
    Angle_L = (2*math.pi)*(enc[1]/508.8)
    # 角速度計算
    w_L = (Angle_L - Angle_L_before) / delta_t
    w_R = (Angle_R - Angle_R_before) / delta_t
    # 速度計算
    v_L = r * w_L
    v_R = r * w_R
    # 計算の為に値を変数に保存
    Angle_R_before = Angle_R
    Angle_L_before = Angle_L
    return [v_L, v_R]

def LocationCalculation():
    global delta_t, angular_vel, angle, vel, before_angular_vel, before_angle, before_vel, x, before_x, y, before_y

    # 現在の角度を算出（角速度の積分）
    #print(vel, before_vel)
    angle = before_angular_vel*delta_t + before_angle
    # 現在のx座標を算出（x軸方向の速度の積分）
    x = before_vel*math.cos(angle)*delta_t + before_x
    # 現在のy座標を算出（y軸方向の速度の積分）
    y = before_vel*math.sin(angle)*delta_t + before_y
    
    before_angular_vel = angular_vel
    before_angle = angle
    before_x = x
    before_y = y
    before_vel = vel
    
    return x, y, angle


delta_t = 0.0
angular_vel = 0.0
angle = 0.0
vel = 0.0
x = 0.0
y = 0.0
before_angular_vel = 0.0
before_angle = 0.0
before_vel = 0.0
before_x = 0.0
before_y = 0.0

def main():
    global delta_t, angular_vel, vel   # 微小時間
    '''シリアル通信用変数'''
    RB_START = bytes([128])
    RB_RESET = bytes([7])

    RB_STOP  = bytes([173])
    RB_SAFE  = bytes([131])
    RB_FULL  = bytes([132])
    RB_SEEK_DOCK  = bytes([143]) #//ドックを探す
    RB_RATE = 115200
    
    print("--- Roomba Control via python ---")
    #print("Start Serial Communication")
    '''シリアル通信開始'''
    ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)
    stop_flag=1
    
    data_dict = {}
    before_t = 0.0  # 1時刻前の時間
    T = 0.235  # 車輪間隔
    # START
    print("START")
    stop_flag = 1
    oimode1 = GetOIMode(ser)
    ser.write(RB_START)
    oimode2 = GetOIMode(ser)
    print("OIMode:"+str(oimode1)+"->"+str(oimode2))
    # SAFE
    print("SAFE")
    stop_flag = 1
    oimode1 = GetOIMode(ser)
    ser.write(RB_SAFE)
    oimode2 = GetOIMode(ser)
    print("OIMode:"+str(oimode1)+"->"+str(oimode2))
    start_time = time.time()
    # 経過時間、エンコーダ値出力処理
    before_x = 0.0
    # 初期化用変数
    first_flg = True
    x_init = 0.0
    y_init = 0.0
    angle_init = 0.0
    # 比例制御ゲイン
    k1 = 100
    k2 = 0.0
    # ウェイポイントの指定
    wp = [0.3, 0.0]
    try:
        while True:
            time.sleep(0.05)
            now_time = time.time() - start_time
            now_time = round(now_time, 3)  # 有効数字3桁に丸める(値が小さすぎると見にくいため)
            # 微小時間の計算
            delta_t = now_time - before_t
            # エンコーダの値取得
            el,er = GetEncs(ser)
            # エンコーダ速度計算
            enc_vel_list = EncVelCalculation([el, er], now_time)
            # 並進速度計算
            vel = sum(enc_vel_list)/2
            # 回転角速度計算
            angular_vel = (enc_vel_list[0] - enc_vel_list[1])/T
            # ロボットの座標計算
            x, y, angle = LocationCalculation()
            
            # 最初だけ初期化
            if first_flg and not x == 0.0:
                x_init = x
                y_init = y
                angle_init = angle
                #print(x_init, y_init, angle_init)
                first_flg = False 
            x -= x_init
            y -= y_init
            angle -= angle_init

            # 値出力
            #print(f"Time[{now_time}], Enc[L: {el} R: {er}]")
            #print(f"Enc_vel[L: {enc_vel_list[0]}  R: {enc_vel_list[1]}]")
            #print(f"Liner_vel[{vel}]")
            #print(f"Anglar_vel[{angular_vel}]")
            print(f"x, y, Angle: {x}, {y}, {math.degrees(angle)}\n")
            before_t = now_time

            # 値格納
            data_dict[now_time] = [x, y, math.degrees(angle)]

            # ウェイポイント計算
            robot_x = -x*10
            robot_y = y
            angle_wp = math.degrees(math.atan2(wp[1]-robot_y, wp[0]-robot_x))
            dist_wp = math.sqrt((wp[1]-robot_y)**2 + (wp[0]-robot_x)**2)

            # 足回り制御
            print(f"diff >>> x:{wp[0]-robot_x}, y: {wp[1]-robot_y}")
            if not wp[0]-robot_x <= 0.1 and wp[1]-robot_y <= 0.1:
                # 制御量計算
                left_vel = k1*dist_wp - k2*angle_wp
                right_vel = k1*dist_wp + k2*angle_wp
                # PWM
                DrivePWM(ser, int(left_vel), int(right_vel))

    except KeyboardInterrupt:
        # 値保存
        with open('angle_data.txt', 'w') as f:
            f.write(json.dumps(data_dict))


main()
