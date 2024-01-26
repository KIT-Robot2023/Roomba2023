from multiprocessing import Process
import object_detection_webcam3
import Roomba_Q

# def main():
#     # キューの初期化（サイズは3）

#     yld = threading.Thread(target=object_detection_webcam3.object_detection_webcam3)
#     # if my_queue.empty():
        
#     # obs = my_queue.get()
#     # print(obs)
#     Roomba_ctrl = threading.Thread(target=Roomba_Q.main) # , args=(obs,)

#     # スレッドを開始
#     yld.start()
#     Roomba_ctrl.start()

#     try:
#         while True:
#             # main.pyが無限ループで処理を続ける
#             # print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
#             pass
#     except KeyboardInterrupt:
#         # Ctrl+Cが押されたらプログラムを終了する
#         yld.join()
#         Roomba_ctrl.join()
#         print("--- program stop ---")
#         # object_detection_webcam3.images_2_video('./Roomba_move','./img,movies')

if __name__ == "__main__":
    print("--- program start ---")
    p1 = Process(target=object_detection_webcam3.object_detection_webcam3)
    p2 = Process(target=Roomba_Q.main)
    # サブプロセスを開始します
    p1.start()
    p2.start()
    try:
        while True:
            # main.pyが無限ループで処理を続ける
            # print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
            pass
    except KeyboardInterrupt:
        p1.join()
        p2.join()
        print("--- program stop ---")
