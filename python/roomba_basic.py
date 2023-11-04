#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考

import numpy as np
import math
import time
import serial

###############################################################
RB_PORT = "COM4"#シリアルポート設定
######################################################################

'''シリアル通信用変数'''
RB_LEFT_ENC = 43 #左エンコーダカウント
RB_RIGHT_ENC = 44 #//右エンコーダカウント

RB_SONG  = 140 #//メロディ記憶．
RB_PLAY  = 141 #//メロディ再生．1バイトデータ必要
RB_OI_MODE  = 35 #//ルンバのモードを返す
RB_LEDS  = 139 #//LED制御

RB_VOLTAGE = 22 #バッテリー電圧
RB_CURRENT = 23 #バッテリー電圧

'''モータ入力用バイト計算関数''' #引数nの，上の８バイト分をHB，下の８バイト分をLBとして分割してreturnする関数．0xff00と両方1のところのみ１にするから
def _CalcHLByte(n):
    HB = n & 0xff00
    HB >>= 8
    LB = n & 0x00ff
    
    return (HB, LB)

'''モータへのPWM信号入力関数'''
def DrivePWM(ser, L_PWM, R_PWM): # 両輪のPWM信号を，上位と下位のビットで分割して保存，その後ser.writeする関数　serはserialのインスタンスで，mainで作成されている
    L_HB, L_LB = _CalcHLByte(L_PWM) #左のモータのPWM値をバイト計算して上位と下位に分けて変数に保存
    R_HB, R_LB = _CalcHLByte(R_PWM) #右のモータのPWM値をバイト計算して上位と下位に分けて変数に保存
            
    ser.write(bytes([146, R_HB, R_LB, L_HB, L_LB])) #146, (10010010)の後に，分けたバイトデータを並べてる

'''センサ値取得関数'''
def GetSensor(ser, p_id, len, sign_flg):
    ser.write(bytes([142, p_id]))
    ser.flushInput() #シリアル通信でデータを受信する際のバッファを保存しているところをクリアにする
    data = ser.read(len) #指定した長さ分だけ読み取る
    
    return int.from_bytes(data, "big", signed=sign_flg) #sign_flgとは？？？

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

#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃オリジナル
def play_song(ser, song_number):
    # # RoombaをSafeモードに設定
    # ser.write(b'\x83')
    
    # 選択した曲を再生
    ser.write(bytes([141, song_number]))
    time.sleep(0.5)  # 必要に応じて適切な待ち時間を追加してください
#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃


def main():
    '''シリアル通信用変数'''
    RB_START = bytes([128]) #各モードを起動するためのバイトコードを送るためのもの
    RB_RESET = bytes([7])
    RB_STOP  = bytes([173])
    RB_SAFE  = bytes([131])
    RB_FULL  = bytes([132])
    RB_SEEK_DOCK  = bytes([143]) #//ドックを探す
    # RB_PLAY = bytes([118])
    RB_RATE = 115200
    
    print("--- Roomba Control via python ---")
    #print("Start Serial Communication")
    '''シリアル通信開始'''
    ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)

    stop_flag=1
    
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
            DrivePWM(ser, speed,speed)
        elif val=='3':
            print("BACK(3)")
            stop_flag = 0
            DrivePWM(ser, -speed,-speed)
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
        elif val=='w':
            print("DOCK")
            ser.write(RB_SEEK_DOCK)

        elif val=='p':# 音を再生
            ser.write(bytes([140, 0, 2, 60, 32, 62, 32]))  # 60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0)
            time.sleep(2)  # 2秒待つ

            ser.write(bytes([140, 1, 18, 74, 16, 74, 16, 76, 32,74, 32, 79, 32, 78, 64, 74, 16, 74, 16, 76, 32, 74, 32, 81, 32, 79, 64, 74, 16, 74, 16, 88, 32, 84, 32, 81, 32, 79, 64]))
            play_song(ser, 1)
            time.sleep(2)  # 2秒待つ例

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
            

main()
