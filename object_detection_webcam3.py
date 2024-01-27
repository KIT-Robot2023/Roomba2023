#!/usr/bin/env python
# coding: utf-8

import socket
import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
# from ultralytics.solutions import heatmap
import math
import time
import os


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

before_distace = 0
before_angle = 0

shared_val = []

# heatmap_obj = heatmap.Heatmap()
# heatmap_obj.set_args(colormap=cv2.COLORMAP_PARULA, imw=640, imh=480, view_img=True, shape='circle')

key_2 = 0

#YOLOのモデルをロード
model = YOLO('models/best.pt')#400 8x 90deg


#YOLOを使った物体検出
def output_distance(predict_result, depth_frame, color_intr, color_im):
    
    nowbox = []
    nowboxbig = []
    
    boxes = predict_result[0].boxes
    names = predict_result[0].names
    classes = predict_result[0].boxes.cls
    
    for box, cls in zip(boxes, classes):
        name = names[int(cls)]
        xmin, ymin, xmax, ymax = [int(i)for i in box.xyxy[0]]
        
        nowbox = [xmin, ymin, xmax, ymax]#バウンディングボックスの4つの座標を格納
        nowboxbig.append(nowbox)#さらにリストに格納
        
        #中央座標計算
        x_length = xmax - xmin #バウンディングボックス長さ
        y_length = ymax - ymin #バウンティングボックス高さ

        x_center = xmin + (x_length / 2) #中央X座標
        y_center = ymin + (y_length / 2) #中央y座標
        

        #距離を取得
        distance = depth_frame.get_distance(int(x_center), int(y_center))
        # print(distance)
        point = np.array([x_center, y_center, distance])
        x_center = point[0]
        y_center = point[1]
        z = point[2]
        x, y, z=rs.rs2_deproject_pixel_to_point(color_intr, [x_center, y_center], z)
        # print(f'angle: {math.degrees(math.atan2(x, z))}')
        

        x_boxsize = rs.rs2_deproject_pixel_to_point(color_intr, [int(xmax), int(ymax)], distance) #ピクセル座標系からワールド座標へ座標返還        
        y_boxsize = rs.rs2_deproject_pixel_to_point(color_intr, [int(xmin), int(ymin)], distance) #ピクセル座標系からワールド座標へ座標返還        
        x_world = float(x_boxsize[0]) - float(y_boxsize[0])
        y_world = float(x_boxsize[1]) - float(y_boxsize[1])        

        
        threeD = rs.rs2_deproject_pixel_to_point(color_intr, [int(x_center), int(y_center)], distance) #ピクセル座標系からワールド座標へ座標返還
        return distance, math.degrees(math.atan2(x, z))

def images_2_video(self,input_dir, output_dir, fps=30):
    images = []

    # 画像を読み込む
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(input_dir, filename)
            img = cv2.imread(img_path)
            images.append(img)

    # 画像のサイズを取得
    height, width, layers = images[0].shape

    # 動画の設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 出力動画のコーデック

    # 連番の動画名を生成
    output_path = os.path.join(output_dir, f"test_video.mp4")

    # VideoWriterを作成
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 画像を動画に書き込む
    for img in images:
        video.write(img)

    # リソースを解放
    video.release()

    print(f"動画が保存されました: {output_path}")

def get_shared_val():
    global shared_val
    return shared_val

#メイン処理
def object_detection_webcam3():

    # Start streaming
    profile=pipeline.start(config)
    global before_distace, before_angle,shared_val
    flag = 0
    # print("objobjobjobjobj")
    target_address = ("127.0.0.1",3000)                         # 送信アドレス
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Socketの生成(UDP)
    ini_distances = []
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color

            try:
                frames = pipeline.wait_for_frames()
            except:
                pass
                # break
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                # pass
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())


            #推論実行
            result = model(color_image, conf=0.80)
            color_image =  result[0].plot()
            
            # time.sleep(1)
            color_ir = rs.video_stream_profile(profile.get_stream(rs.stream.color)).get_intrinsics()


            # count += 1

            # if count == 3:
            #     return -1,-1
                # break

            #距離を出力
            result = output_distance(result, depth_frame, color_ir, color_image)
            

            if result is not None:
                distance, angle = result

                if flag == 0:
                    time.sleep(10)

                if flag < 10:
                    ini_distances.append(distance)
                    flag += 1

                if flag == 10:
                    ini_distances.pop(ini_distances.index(max(ini_distances)))
                    ini_distances.pop(ini_distances.index(min(ini_distances)))
                    flag += 1
                if flag > 10:
                    ini_distance = sum(ini_distances) / len(ini_distances)


                # if before_distace != 0:
                    print(ini_distance)
                    normalized_distance = distance / ini_distance
                    before_distace = distance

                    # if before_angle != 0:
                    # print(angle / before_angle)
                            # -90度から90度の範囲に収める
                    if angle < -90:
                        angle += 180
                    elif angle > 90:
                        angle -= 180

                        # 角度を0から1に射影する
                    normalized_angle = (angle + 90) / 180

                    shared_val =[normalized_distance,normalized_angle]
                # my_queue.put(normalized_distance,normalized_angle)

            else:
                # print("Output from output_distance is None.")
                # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                # images = np.hstack((color_image, depth_colormap))
                # cv2.imwrite(f"Roomba_move_img/image_{key_2 + 1:03d}.png", images)
                # my_queue.put(-1,-1)
                shared_val = [-1,-1]

            # msg = shared_val
            # sock.sendto(msg.encode(encoding="utf-8"), target_address)
            msg_str = [str(item) for item in shared_val]
            sock.sendto(",".join(msg_str).encode(encoding="utf-8"), target_address)

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # tracks = model.track(color_image, persist=True, show=False)
            # heatmap_image = heatmap_obj.generate_heatmap(color_image, tracks)

            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            # cv2.imwrite(f"Roomba_move_img/image_{key_2 + 1:03d}.png", images)
            cv2.imshow('RealSense', images)
            # print('pass')
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break



    # except KeyboardInterrupt:
    #     print("--- program stop at OBJ3---")

    except KeyboardInterrupt:
        # Stop streaming
        pipeline.stop()
        #cap.release()
        sock.close()
        cv2.destroyAllWindows()
        print("--- OBJ3 stop ---")

# object_detection_webcam3()

if __name__ == "__main__":
    print("--- OBJ3 start ---")
    object_detection_webcam3()