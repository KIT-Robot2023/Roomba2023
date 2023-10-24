#!/usr/bin/env python
# coding: utf-8
#2020.1.14西野君ソースコードQlearn_and_run.pyを参考

import numpy as np
import math
import time
import serial
import threading
import socket, struct

#########################################################
RB_PORT = "COM5"#シリアルポート設定
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

def print_function():
    global exit_signal
    exit_signal = threading.Event()
    th = threading.Thread(target = print_encs_value, args=(ser, memory))
    th.start()

'''各エンコーダ値取得関数'''

def print_encs_value(ser, memory):
    Ser = ser
    Memory = memory
    while not exit_signal.is_set():
        start = time.time()
        EncL = GetSensor(Ser, RB_LEFT_ENC, 2, False)
        EncR = GetSensor(Ser, RB_RIGHT_ENC, 2, False)
        time.sleep(0.01)
        print(EncL, EncR)
        end = time.time() - start
        
        SendData = struct.pack(
            'fffff',
            float( EncR ),
            float( EncL ),
            float( Memory[0] ),
            float( Memory[1] ),
            float( end )
        )
        
        # Send data with UDP
        Sender.sendto(SendData, Destination)

        Memory[0] = EncR
        Memory[1] = EncL

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

# Set UDP-Receive
# Argument 1,2 : Information of Receiver (by oneself)
def Set_UDP_Receive(IP, Port):
    Address = (IP, Port)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.bind(Address)

    # Return Socket object
    return Socket

def main():
    global ser, Sender, Destination, memory
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

    local = '127.0.0.1'
    send_port = 50000
    dist_port = 51000
    recv_port = 52000

    Sender, Destination = Set_UDP_Send(
        local, send_port,
        local, dist_port
    )

    Reciever = Set_UDP_Receive(local, recv_port)

    memory = [0, 0]

    stop_flag=1
    speed=70
    speed_rot=50

    oimode1 = GetOIMode(ser)
    ser.write(RB_RESET)
    time.sleep(0.5)
    ser.write(RB_START)
    time.sleep(0.5)
    ser.write(RB_SAFE)
    time.sleep(0.5)
    ser.write(RB_FULL)
    oimode2 = GetOIMode(ser)
    print("OIMode:"+str(oimode1)+"->"+str(oimode2))

    # time.sleep(1)

    # print_function()
    time.sleep(1)
    DrivePWM(ser, speed,speed)
    
    # try:
    while True:
        RecvData = Reciever.recvfrom(4)
        Data = struct.unpack('f', RecvData[0])
        # re_Data =int(Data)
        mode = list( map(int, Data) )
        # print(mode)
        start = time.time()
        # print(type(mode[0]))

        # val=input('Input command char: ')
        #print("Input val="+val)
        if mode[0] == 0:
            # print("STOP MOTOR")
            # stop_flag = 1
            DrivePWM(ser, 0,0)
            # time.sleep(0.1)
            EncL = GetSensor(ser, RB_LEFT_ENC, 2, False)
            EncR = GetSensor(ser, RB_RIGHT_ENC, 2, False)
            time.sleep(0.01)
            print(EncL, EncR)
            end = time.time() - start
            
            SendData = struct.pack(
                'fffff',
                float( EncR ),
                float( EncL ),
                float( memory[0] ),
                float( memory[1] ),
                float( end )
            )
            
            # Send data with UDP
            Sender.sendto(SendData, Destination)

            memory[0] = EncR
            memory[1] = EncL
        elif mode[0] == 2:
            # print("FWR(1)")
            stop_flag = 0
            DrivePWM(ser, speed,speed)
            # time.sleep(0.1)
            EncL = GetSensor(ser, RB_LEFT_ENC, 2, False)
            EncR = GetSensor(ser, RB_RIGHT_ENC, 2, False)
            time.sleep(0.01)
            print(EncL, EncR)
            end = time.time() - start
            
            SendData = struct.pack(
                'fffff',
                float( EncR ),
                float( EncL ),
                float( memory[0] ),
                float( memory[1] ),
                float( end )
            )
            
            # Send data with UDP
            Sender.sendto(SendData, Destination)

            memory[0] = EncR
            memory[1] = EncL
        else:
            # print("STOP MOTOR")
            # stop_flag = 1
            DrivePWM(ser, 0,0)
            time.sleep(0.01)
            # print("ROT-R(0)")
            # stop_flag = 0
            # DrivePWM(ser, speed_rot,-speed_rot)
        # elif val=='2':
        #     print("ROT-L(2)")
        #     stop_flag = 0
        #     DrivePWM(ser, -speed_rot,speed_rot)
        # elif val=='1':
        #     print("FWR(1)")
        #     stop_flag = 0
        #     DrivePWM(ser, speed,speed)
        # elif val=='3':
        #     print("BACK(3)")
        #     stop_flag = 0
        #     DrivePWM(ser, -speed,-speed)
        # elif val=='d':
        #     print("RESET")
        #     stop_flag = 1
        #     ser.write(RB_RESET)
        #     str1 = ser.read(234)
        #     print(str1)
        # elif val=='a':
        #     print("START")
        #     stop_flag = 1
        #     oimode1 = GetOIMode(ser)
        #     ser.write(RB_START)
        #     oimode2 = GetOIMode(ser)
        #     print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        # elif val=='g':
        #     print("SAFE")
        #     stop_flag = 1
        #     oimode1 = GetOIMode(ser)
        #     ser.write(RB_SAFE)
        #     oimode2 = GetOIMode(ser)
        #     print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        # elif val=='f':
        #     print("FULL")
        #     stop_flag = 1
        #     oimode1 = GetOIMode(ser)
        #     ser.write(RB_FULL)
        #     oimode2 = GetOIMode(ser)
        #     print("OIMode:"+str(oimode1)+"->"+str(oimode2))
        # elif val=='w':
        #     print("DOCK")
        #     ser.write(RB_SEEK_DOCK)
        # elif val=='z':
        #     print("SENSOR")
        #     # el,er = GetEncs(ser)
        #     oimode = GetOIMode(ser)
        #     vol = GetSensor(ser, RB_VOLTAGE, 2, False)
        #     cur = GetSensor(ser, RB_CURRENT, 2, False)
            
        #     # print("Enc L:"+str(el)+" R:"+str(er))
        #     print("OIMode:"+str(oimode))
        #     print("Votage/Current ="+str(vol)+"[mV]/"+str(cur)+"[mA]")

        # else:
        #     print("Input val="+val)

    # except KeyboardInterrupt:
    #     exit_signal.set()
            
if __name__ == '__main__':
    main()