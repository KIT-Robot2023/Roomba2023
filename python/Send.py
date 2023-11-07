import socket, struct
import time
import sys
import math
from typing import Counter

# 送信者自身の Socket オブジェクトと送信先のアドレスの生成
# 第 1，2 引数は送信者の情報，第 3，4 引数は送信先の情報
def Set_UDP_Send(IP_src, Port_src, IP_dst, Port_dst):

    Address_src = (IP_src, Port_src)
    Address_dst = (IP_dst, Port_dst)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.bind(Address_src)

    # 送信者の Socket オブジェクトと送信先のアドレスを返す
    return Socket, Address_dst

if __name__ == "__main__":

    try:

        deg = 0

        # 送信者の Socket オブジェクト (Sender) と送信先のアドレス (Destination) を生成
        Sender, Destination = Set_UDP_Send("192.168.11.4", 5000, "192.168.11.2", 4000)

        print("\n == Sned Data Start == \n")
        time.sleep(1.5)

        while True:
            
            # Step.1　送信したいデータを生成
            Send_Data1 = float(math.sin( math.radians(deg) ))
            Send_Data2 = float(Send_Data1 * 2)
            Send_Data3 = float(Send_Data1 * 3)
            Send_Data4 = float(Send_Data1 * 4)
            Send_Data5 = float(Send_Data1 * 5)
            Send_Data6 = float(Send_Data1 * 6)

            # Step.2　データを送信できるように Pack し・バイナリデータを作成
            Send_Data_Binari = struct.pack( "ffffff",
                                            Send_Data1,
                                            Send_Data2,
                                            Send_Data3,
                                            Send_Data4,
                                            Send_Data5,
                                            Send_Data6
                                         )

            # Step.3　データを送信先に送信
            Sender.sendto( Send_Data_Binari, Destination )

            deg += 0.1
            time.sleep(0.01)

    except KeyboardInterrupt:
        
        print("\n == Sned Data Stop == \n")
        sys.exit()