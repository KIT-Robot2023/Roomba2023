#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考

import numpy as np
import math
import time
import serial
import matplotlib as plt
import keyboard

################################################
RB_PORT = "COM6"#シリアルポート設定
################################################

'''ルンバ実機の長さなどの値'''
TREAD = 235 # (mm)  単位はミリ
TIRE_R = 36 # (mm)  単位はミリ

'''シリアル通信用変数'''
RB_LEFT_ENC = 43 #左エンコーダカウントのOPcode
RB_RIGHT_ENC = 44 #//右エンコーダカウントのOPcode

RB_SONG  = 140 #//メロディ記憶モードのOPcode
RB_PLAY  = 141 #//メロディ再生のOPcode　このOPcodeの後ろに，曲を選択する数字（４まで）が必要（１バイト？）ser.write(bytes([141, →song_number←]))とすればよい
RB_OI_MODE  = 35 #//ルンバの現在のモードを返す
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

'''センサ値取得関数''' #指定されたセンサーに対してリクエストを送信して、そのセンサーからの応答を整数として返す。符号つき整数に変換するかどうかは、sign_flg をTrueにするかで決める。
def GetSensor(ser, p_id, len, sign_flg):
    ser.write(bytes([142, p_id]))
    ser.flushInput() #シリアル通信でデータを受信する際のバッファを保存しているところをクリアにする
    data = ser.read(len) #指定した長さ分だけ読み取る
    
    return int.from_bytes(data, "big", signed=sign_flg) #sign_flgとは？？　←符号つけるかどうかのフラグ　ここではbigというやり方で，取得したdataをバイト列から整数に変換している　　具体的には、dataに格納されたバイト列を大端 (big endian) フォーマットで整数に変換

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
    time.sleep(0.5)
#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃


def main():
    '''シリアル通信用変数'''
    RB_START = bytes([128]) #各モードを起動するためのバイトコードを送るためのもの
    RB_RESET = bytes([7])
    RB_STOP  = bytes([173])
    RB_SAFE  = bytes([131])
    RB_FULL  = bytes([132])
    RB_SEEK_DOCK  = bytes([143]) #//ドックを探す
    RB_LED = bytes([139]) #LED制御のOPcode　使い方→　Serial sequence: [139] [LED Bits (0 - 255)] [Power Color] [Power Intensity]
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
            print('出てますか？')
        elif val=='3':
            print("BACK(3)")
            stop_flag = 0
            DrivePWM(ser, -speed,-speed)
        elif val=='key_ctrl':
            print("キーボード操作モードです")
            stop_flag = 0
            while True:
                if keyboard.is_pressed('up'):
                    print("キー '↑'")
                    DrivePWM(ser, 200,200)
                    # 'a'キーに対する処理をここに記述
                elif keyboard.is_pressed('right'):
                    print("キー '→' ")
                    DrivePWM(ser, 200,-200)
                    # 'b'キーに対する処理をここに記述
                elif keyboard.is_pressed('left'):
                    print("キー '←' ")
                    DrivePWM(ser, -200,200)
                    # 'c'キーに対する処理をここに記述
                elif keyboard.is_pressed('down'):
                    print("キー '↓' ")
                    DrivePWM(ser, -200,-200)
                    # 'c'キーに対する処理をここに記述
                elif keyboard.is_pressed('q'):
                    print("キーボード捜査モード終了")
                    DrivePWM(ser, -200,200)
                    #break  # どのキーも押されていなければループを抜ける
                else:
                    print("いずれのキーも押されていません。")
                    DrivePWM(ser, 0,0)
                    # 'c'キーに対する処理をここに記述

                time.sleep(0.1)  # ループの速度を制御

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

            # ser.write(bytes([140, 1, 18, 74, 16, 74, 16, 76, 32,74, 32, 79, 32, 78, 64, 74, 16, 74, 16, 76, 32, 74, 32, 81, 32, 79, 64, 74, 16, 74, 16, 88, 32, 84, 32, 81, 32, 79, 64]))
            ser.write(bytes([140, 1, 6, 74, 16, 74, 16, 76, 32,74, 32, 79, 32, 78, 64,]))
            # time.sleep(2)  # 2秒待つ
            play_song(ser, 1)
            time.sleep(1)  # 2秒待つ

        elif val=='l':
            print("LED_MODE!")
            ser.write(bytes([139, 8, 0, 255]))
            time.sleep(1)  # 1秒待つ
            # ser.write(RB_SEEK_DOCK)

        elif val=='z':
            print("SENSOR")
            el,er = GetEncs(ser)
            oimode = GetOIMode(ser)
            vol = GetSensor(ser, RB_VOLTAGE, 2, False)
            cur = GetSensor(ser, RB_CURRENT, 2, False)
            
            print("Enc L:"+str(el)+" R:"+str(er))
            print("OIMode:"+str(oimode))
            print("Votage/Current ="+str(vol)+"[mV]/"+str(cur)+"[mA]")

        elif val=='od':
            print("Odometry test mode ON!")
            ser.write(bytes([140, 0, 4, 60, 8, 62, 8, 64, 8, 66, 8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(2)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = (math.pi/2) #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0

            #モータを動かす．（まずは直進させてみる）
            print("Go_Straight！！")
            stop_flag = 0
            DrivePWM(ser, 70,70)

            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("最初のエンコーダの値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間も取得しました")

            start_time = time.time()
            while time.time() - start_time < 5:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, 70,70)
                time.sleep(0.01) # 一定時間待機
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                delta_t = t_prev - now_time #経過時間（秒）を取得

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * encR #各タイヤの移動量を，エンコーダの値の差から算出

                rotation_angle_L = ((2*math.pi)/508.8) * encL
                rotation_angle_R = ((2*math.pi)/508.8) * encR #出たパルス分（encL,R）の回転角度を計算

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                # 並進V,旋回 ω を計算
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                print("ルンバのｘ座標：" + str(Roomba_xpos))
                print("ルンバのｙ座標：" + str(Roomba_ypos))
                #以前の値更新
                encL_prev = encL
                encR_prev = encR
                t_prev = now_time

        elif val=='t2': 
            print("test_2")
            stop_flag = 0
            DrivePWM(ser, 70,70)
            start_time = time.time()
            while time.time() - start_time < 5:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                print("encL:" + str(encL) + ",  encR:" + str(encR))

                now_time = time.time()
                print("time:" + now_time) # 現在の時刻を表示
                time.sleep(0.2)

        elif val=='t3': 
            print("Odometry test mode ON!")
            ser.write(bytes([140, 0, 4, 60, 8, 62, 8, 64, 8, 66, 8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(2)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = (math.pi/2) #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0

            #モータを動かす．（まずは直進させてみる）
            print("Go_Straight！！")
            stop_flag = 0
            DrivePWM(ser, -70,-70)

            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("最初のエンコーダの値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間も取得しました")

            start_time = time.time()
            while time.time() - start_time < 3:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, 100,100)
                time.sleep(0.2) # 一定時間待機
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                print("ΔencL:" + str(delta_encL))
                print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                print("L速度:" + str(vL))
                print("R速度:" + str(vR))

                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
            DrivePWM(ser, 0,0)

        elif val=='t4': 
            print("Odometry test mode ON!")
            ser.write(bytes([140, 0, 4, 60, 8, 62, 8, 64, 8, 66, 8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(2)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = (math.pi/2) #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0

            #モータを動かす．（まずは直進させてみる）
            print("kaiten")
            stop_flag = 0
            DrivePWM(ser, 70,-70)

            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("最初のエンコーダの値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間も取得しました")

            start_time = time.time()
            while time.time() - start_time < 3:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす.
                print("Go！！")
                stop_flag = 0
                DrivePWM(ser, 70,-70)
                time.sleep(0.2) # 一定時間待機
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                print("ΔencL:" + str(delta_encL))
                print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t #タイヤの移動量を時間で割ることで，速度を求める
                vR = move_range_R / delta_t
                print("Lタイヤの速度:" + str(vL) + "mm/s")
                print("Rタイヤの速度:" + str(vR) + "mm/s")


                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                print("Lタイヤの角速度:" + str(rotation_angle_L))
                print("Rタイヤの角速度:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                print("ルンバの旋回角速度ω：" + str(math.degrees(Roomba_senkai_speed)) + "度/秒")
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                # print("L速度:" + str(L_vel))
                # print("R速度:" + str(R_vel))
                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
            DrivePWM(ser, 0,0)





        elif val=='t5':  #左右差
            print("Odometry test mode ON!")
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("1/3・直進 最初のエンコーダの値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"1/3・直進")


            start_time = time.time()
            while time.time() - start_time < 2:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, 70,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed) + "[rad/s]")
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang)))

            start_time = time.time()
            while time.time() - start_time < 2:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                print("2/3 その場旋回")
                stop_flag = 0
                DrivePWM(ser, -70,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang)))

            start_time = time.time()
            while time.time() - start_time < 2:  # 現在の時刻と開始時刻の差が5秒未満の間 つまり5秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                print("3/3直進")
                stop_flag = 0
                DrivePWM(ser, 70,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang)))
            DrivePWM(ser, 0,0)






##################################################################################################################################################################
        elif val=='test_st':  #kouzi
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("直進 最初enc値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間も取得しました ")


            start_time = time.time()
            while time.time() - start_time < 1:  # 現在の時刻と開始時刻の差が3秒未満の間 つまり3秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, 70,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの今の値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理未実装＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang)))

            start_time = time.time()
            
            DrivePWM(ser, 0,0)
##################################################################################################################################################################

        elif val=='test_turn':  #kouzi
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("その場旋回 最初enc値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間も取得しました 変数準備完了")


            start_time = time.time()
            while time.time() - start_time < 1:  # 現在の時刻と開始時刻の差が3秒未満の間 つまり3秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, -70,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの今の値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理未実装＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang)))

            start_time = time.time()
            
            DrivePWM(ser, 0,0)
##################################################################################################################################################################

        elif val=='test_cur':  #kouzi
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("カーブ 最初enc値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間取得 変数準備完了")


            start_time = time.time()
            while time.time() - start_time < 2:  # 現在の時刻と開始時刻の差が3秒未満の間 つまり3秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                DrivePWM(ser, 35,70)
    
                encL, encR = GetEncs(ser) # 左右のエンコーダの今の値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理未実装＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                print(str(-Roomba_xpos),str(-Roomba_ypos),str(math.degrees(sennkai_delta_ang))) #今のルンバのx座標，ｙ座標，角度であるので，あとはこの情報を使ってif文書けばいい！

            start_time = time.time()
            
            DrivePWM(ser, 0,0)
##################################################################################################################################################################
#################################################################################################################################################################
            #################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
#ウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイントウェイポイント
##################################################################################################################################################################
#################################################################################################################################################################
#################################################################################################################################################################


        elif val=='wayp':  #kouzi
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            #######目標座標（ウェイポイント）設定
            x_wp = 1000
            y_wp = 2000
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0
            #目標位置，角度を設定


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("カーブ 最初enc値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間取得 変数準備完了")


            start_time = time.time()
            while time.time() - start_time < 20:  # 現在の時刻と開始時刻の差が3秒未満の間 つまり3秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                # DrivePWM(ser, 35,70)

                encL, encR = GetEncs(ser) # 左右のエンコーダの今の値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理未実装＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                now_ang = math.degrees(sennkai_delta_ang)
                # print(str(-Roomba_xpos),str(-Roomba_ypos),str(now_ang)) #今のルンバのx座標，ｙ座標，角度であるので，あとはこの情報を使ってif文書けばいい！

                
                thita_wayp = math.atan2(y_wp - Roomba_ypos, x_wp - Roomba_xpos)
                delta_thita_wayp = thita_wayp - now_ang #これで、目標座標への方角のずれがわかった
                distance_wayp = math.sqrt((y_wp - Roomba_ypos)*(y_wp - Roomba_ypos)+(x_wp - Roomba_xpos)*(x_wp - Roomba_xpos))
                print("方位のずれ：",delta_thita_wayp,"距離d：",distance_wayp)


                if distance_wayp >=100: # 目標の位置の方位と今のルンバの向きの方位の差が５以上だったら　旋回して角度合わせる，
                    DrivePWM(ser, int(0.05*distance_wayp-30*delta_thita_wayp) , int(0.05*distance_wayp+30*delta_thita_wayp)) #差の大きさの変数をそのまま出力にするのが一番よさそう（P制御）

                    print(int(0.05*distance_wayp-30*delta_thita_wayp) , int(0.05*distance_wayp+30*delta_thita_wayp))

            start_time = time.time()
            
            DrivePWM(ser, 0,0)
##################################################################################################################################################################
            

        elif val=='twayp2':  #kouzi
            ser.write(bytes([140, 0, 4, 60,8, 62,8, 64,8, 66,8]))  # オドメトリモード起動音セット　　60と62はノート番号、32は持続時間 つまり，bytesを使えば簡単にシリアルデータを送信できるぞ
            # ここで，140はモード，0は曲の番号（０番目の曲に音をセットする），音を出す数は２音，６０の音を32という時間だけ流す，６２という音を３２という時間だけ流す
            play_song(ser, 0) #オドメトリ起動音再生
            #######目標座標（ウェイポイント）設定
            x_wp = 1000
            y_wp = 1000
            print("目標座標：x=",x_wp,", y=",y_wp)
            time.sleep(0.1)  # 2秒待つ

            #初期角度と位置を設定
            sennkai_delta_ang = 0 #初期の角度は2分のパイつまりxy平面でy軸方向を向いている
            Roomba_xpos = 0
            Roomba_ypos = 0
            #目標位置，角度を設定


            # まずは最初のエンコーダ値取得，そして開始時間も取得
            # print("get encoder value...")
            encL_prev, encR_prev = GetEncs(ser) # 左右のエンコーダの値取得
            t_prev = time.time() # プログラムの実行開始時刻を取得 time.time()は，システムが起動してから何秒経ったかを取得してくれる関数　よってこれを引き算することで経過時間（秒）を得られる
            print("カーブ 最初enc値は:左が"+str(encL_prev)+"で，右が"+str(encL_prev)+"です．時間取得 変数準備完了")


            start_time = time.time()
            while time.time() - start_time < 20:  # 現在の時刻と開始時刻の差が3秒未満の間 つまり3秒間ループ処理
                #モータを動かす．（まずは直進させてみる）
                # print("Go_Straight！！")
                stop_flag = 0
                # DrivePWM(ser, 35,70)

                encL, encR = GetEncs(ser) # 左右のエンコーダの今の値再び取得
                now_time = time.time() # 現在の時刻を取得

                #微小区間の値を取得
                delta_encL = encL_prev - encL
                delta_encR = encR_prev - encR #エンコーダの値の差を取る
                #(＃＃＃＃＃＃65535繰り上げ処理未実装＃＃＃＃＃＃＃＃＃＃＃＃)
                # print("ΔencL:" + str(delta_encL))
                # print("ΔencR:" + str(delta_encR))
                delta_t = t_prev - now_time #経過時間（秒）を取得
                # print("Δt:" + str(delta_t))

                #計算
                move_range_L = ((2*math.pi*TIRE_R)/508.8) * delta_encL
                move_range_R = ((2*math.pi*TIRE_R)/508.8) * delta_encR #各タイヤの移動量を，エンコーダの値の差から算出

                vL = move_range_L / delta_t
                vR = move_range_R / delta_t
                # print("L速度:" + str(vL))
                # print("R速度:" + str(vR))

                rotation_angle_L = ((2*math.pi)/508.8) * delta_encL
                rotation_angle_R = ((2*math.pi)/508.8) * delta_encR #出たパルス分（delta_encL,R）の回転角度を計算
                # print("角速度L:" + str(rotation_angle_L))
                # print("角速度R:" + str(rotation_angle_R))

                rotational_ang_vel_L = rotation_angle_L / delta_t #単位時間当たりの回転角度を計算すると，角速度が求められる 各タイヤの回転角速度
                rotational_ang_vel_R = rotation_angle_R / delta_t #
                Roomba_senkai_speed = (vL - vR)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                # print("旋回角速度ω：" + str(Roomba_senkai_speed))
                # v_L, v_R 計算
                L_vel = TIRE_R * rotational_ang_vel_L #角速度に半径をかけると，速度になる（v = rω）
                R_vel = TIRE_R * rotational_ang_vel_R
                Roomba_speed = (L_vel + R_vel)/2 # 並進速度(左右の速度の平均) つまりルンバ自体の速度となる＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
                Roomba_senkai_speed = (L_vel - R_vel)/TREAD #ルンバ自体の回転（旋回）速度を計算 方向は符号で判断可能＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃

                #あとは，微笑時間ごとにルンバの速度と旋回から，進んだ方向と長さを計算して足していけばよい！（厳密な積分ではなく離散積分になるので，リーマン和という）
                #まずはルンバの向きを算出し，微笑時間ごとの角度変化を累積していくことで現在のルンバの向き情報を取得する．
                # ルンバの向きは，微小時間の旋回速度の旋回の和より， (距離＝速度×時間)を使って，方向の変化を求める．そして足していく
                sennkai_delta_ang += Roomba_senkai_speed * delta_t #Δtを使った離散積分で（θ，x，y）を更新
                # print("ルンバの角度："+str(math.degrees(sennkai_delta_ang))+"度  （x座標軸から）")
                #ルンバ自体の速度の情報から移動距離を計算できるので，微笑時間ごとの移動距離を計算して足しこんでいく．そして向きの情報から，cosとsinを使って，x軸方向の移動距離とy軸方向の移動距離を計算して累積していくことで移動した座標が推定できる（尾止め鳥）
                Roomba_xpos += Roomba_speed * math.cos(sennkai_delta_ang) * delta_t #ルンバの速度のx成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得
                Roomba_ypos += Roomba_speed * math.sin(sennkai_delta_ang) * delta_t #ルンバの速度のy成分を微小時間ごとに足しこんて累積していくことでx座標の微小区間の移動距離を取得

                # print("ルンバのｘ座標：" + str(Roomba_xpos))
                # print("ルンバのｙ座標：" + str(Roomba_ypos))


                encL_prev = encL
                encR_prev = encR
                t_prev = now_time
                now_ang = math.degrees(sennkai_delta_ang)
                print("x座標：",str(-Roomba_xpos),"y座標：",str(-Roomba_ypos),"現在角度：",str(now_ang)) #今のルンバのx座標，ｙ座標，角度であるので，あとはこの情報を使ってif文書けばいい！

                
                thita_wayp = math.atan2(y_wp - Roomba_ypos, x_wp - Roomba_xpos)
                delta_thita_wayp = thita_wayp - sennkai_delta_ang #これで、目標座標への方角のずれがわかった
                distance_wayp = math.sqrt((y_wp - -1*Roomba_ypos)*(y_wp - -1*Roomba_ypos)+(x_wp - -1*Roomba_xpos)*(x_wp - -1*Roomba_xpos))
                print("方位のずれ：",math.degrees(delta_thita_wayp),"距離d：",distance_wayp)


                if distance_wayp >=100: # 目標の位置の方位と今のルンバの向きの方位の差が５以上だったら　旋回して角度合わせる，
                        # DrivePWM(ser, int(0.15*distance_wayp-20*delta_thita_wayp) , int(0.15*distance_wayp+20*delta_thita_wayp)) #差の大きさの変数をそのまま出力にするのが一番よさそう（P制御）
                        # print(int(0.15*distance_wayp-20*delta_thita_wayp+29) , int(0.15*distance_wayp+20*delta_thita_wayp+29))
                        DrivePWM(ser, int(0.15*distance_wayp-150*delta_thita_wayp+4)+10 , int(0.15*distance_wayp+150*delta_thita_wayp+4)+10) #差の大きさの変数をそのまま出力にするのが一番よさそう（P制御）
                        print(int(0.15*distance_wayp-50*delta_thita_wayp)+10 , int(0.15*distance_wayp+50*delta_thita_wayp)+10)


                        # 直進
                        # DrivePWM(ser, int(0.15*distance_wayp)+29 , int(0.15*distance_wayp)+29) #差の大きさの変数をそのまま出力にするのが一番よさそう（P制御）
                        # print(int(0.15*distance_wayp)+25 , int(0.15*distance_wayp)+25)
                else:
                    DrivePWM(ser, 0,0)


            start_time = time.time()
            
            DrivePWM(ser, 0,0)
###########################################################################
##################################################################################################################################################################



#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
            # ser.write(bytes([139, 8, 0, 255]))
            # time.sleep(1)  # 1秒待つ
            # # ser.write(RB_SEEK_DOCK)
            # plt.plot(Roomba_xpos, Roomba_ypos)
            # plt.title('Roomba_pos_predict')
            # # plt.show()
            # # 画像ファイルに保存する
            # plt.savefig('output.png')
#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
        # else:
        #     print("Input val="+val)
            

main()