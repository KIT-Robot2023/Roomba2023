#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math
import time
import serial
import keyboard
import Q_ctrl
import os
import shutil
import object_detection_webcam3

import socket
import threading
import queue
import time



class Receiver(threading.Thread):
    def __init__(self, address, timeout=0.5, buf_size=256, max_receive_size=1024):
        super().__init__()
        self.daemon = True
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socketの生成(UDP)
        self.__sock.settimeout(timeout)                 # Socketのタイムアウトの設定. この値を設定しないとrecvfromで永遠に受信待ちすることになる.
        self.__sock.bind(address)                       # 受信アドレスの設定
        self.__rev_buf = queue.Queue(buf_size)          # 受信データのバッファ(キュー)
        self.data_list = []
        self.__max_receive_size = max_receive_size
        self.__is_receive = False
        self.start()    # スレッドの開始(UDP受信の処理はスレッドで行われる)

    def __del__(self):
        self.__sock.close()

    def startReceiving(self):
        """受信を開始する"""
        self.__is_receive = True

    def stopReceiving(self):
        """受信を停止する"""
        self.__is_receive = False

    def run(self):
        while True:
            if self.__is_receive == True:
                try:
                    data, address = self.__sock.recvfrom(self.__max_receive_size)   # 受信(タイムアウトで例外(socket.timeout)が送出される)
                    # msg = data.decode(encoding="utf-8")
                    # self.__rev_buf.put(msg, False)      # 受信データをバッファ(キュー)に追加する
                    received_list = data.decode("utf-8").split(",")
                    float_received_list = [float(item) for item in received_list]
                    # self.__rev_buf.put(received_list, False)
                    self.data_list.insert(0, float_received_list)
                    self.data_list.pop(-1)
                    # try:
                    #     self.__rev_buf.put(received_list, False)
                    # except queue.Full:
                    #     # キューが満杯の場合、先頭のデータを削除してから追加
                    #     self.__rev_buf.get_nowait()
                    #     self.__rev_buf.put(received_list, False)

                except socket.timeout:
                    pass
            else:
                time.sleep(0.01)

    def read(self):
        """
        データバッファ(キュー)からデータを1つ取り出す\n
        バッファが空の場合は例外(queue.Empty)が送出される
        """
        return self.__rev_buf.get(block=False)

    def empty(self):
        """
        受信データのバッファ(キュー)が空かの判定\n
        空の場合: True, 空でない場合: False
        """
        return self.__rev_buf.empty()




#########################################################
RB_PORT = "COM7"#シリアルポート設定
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
    agent = Q_ctrl.Action_decide()

    # receive_address = ("127.0.0.1",3000)    # 受信アドレス
    # receiver = Receiver(receive_address)
    # receiver.startReceiving()               # 受信開始
    receive_address = "127.0.0.1"
    receive_port = 3000

    print("--- Serial start ---")
    '''シリアル通信開始'''
    ser = serial.Serial(RB_PORT, RB_RATE, timeout=10)

    stop_flag=1

    ser.write(RB_START)#スタート
    ser.write(RB_SAFE)#セーフ
    velocity = 200
    key = 1
    while True:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((receive_address, receive_port))
        try:
            while True:
                print("now loding")
                data, client_address = udp_socket.recvfrom(1024)
                received_list = data.decode("utf-8").split(",")
                obs = [float(item) for item in received_list]

                if obs:
                    break
        except KeyboardInterrupt:
            print("Receiver stopped.")
        finally:
            udp_socket.close()

        try:
            # if keyboard.is_pressed('w'):
            #     DriveVelocity(ser,velocity,velocity)
            # elif keyboard.is_pressed('a'):
            #     DriveVelocity(ser,-velocity,velocity)
            # elif keyboard.is_pressed('s'):
            #     DriveVelocity(ser,-velocity,-velocity)
            # elif keyboard.is_pressed('d'):
            #     DriveVelocity(ser,velocity,-velocity)
            # if keyboard.is_pressed('q'):
            #     DriveVelocity(ser,velocity/2,velocity)
            # elif keyboard.is_pressed('e'):
            #     DriveVelocity(ser,velocity,velocity/2)
            # elif keyboard.is_pressed('z'):
            #     DriveVelocity(ser,-velocity/2,-velocity)
            # elif keyboard.is_pressed('c'):
            #     DriveVelocity(ser,-velocity,-velocity/2)
            # else:
            #     DriveVelocity(ser,0,0))
            # print(float_obs)
            # print("ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")

            action = agent.ctrl(observation = obs)

            if action == 0:
                DriveVelocity(ser,velocity,velocity)
            elif action == 1:
                DriveVelocity(ser,int(velocity/2),velocity)
            elif action == 2:
                DriveVelocity(ser,velocity,int(velocity/2))
            else:
                DriveVelocity(ser,0,0)

            print('select action %d, obs[0] = %.1lf, obs[1] = %.1lf' % (action, obs[0],obs[1]))

            key += 1

            time.sleep(0.5)
        # DriveVelocity(ser,0,0)

        # if keyboard.is_pressed('q'):
            # break
        except KeyboardInterrupt:

            print("--- Roomba_Q_ctrl_stop ---")
            break

if __name__ == "__main__":
    print("--- Roomba_Q_ctrl_start ---")
    main()
# object_detection_webcam2_1.images_2_video('./Roomba_move_img','./movies')

# target_dir = 'Roomba_move_img'
# shutil.rmtree(target_dir)
# os.mkdir(target_dir)