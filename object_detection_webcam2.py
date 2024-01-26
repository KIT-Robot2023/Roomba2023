import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
# from ultralytics.solutions import heatmap
import math

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

before_distace = 0
before_angle = 0

# heatmap_obj = heatmap.Heatmap()
# heatmap_obj.set_args(colormap=cv2.COLORMAP_PARULA, imw=640, imh=480, view_img=True, shape='circle')


#YOLOのモデルをロード
model = YOLO('best.pt')#400 8x 90deg


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
        print(distance)
        point = np.array([x_center, y_center, distance])
        x_center = point[0]
        y_center = point[1]
        z = point[2]
        x, y, z=rs.rs2_deproject_pixel_to_point(color_intr, [x_center, y_center], z)
        print(f'angle: {math.degrees(math.atan2(x, z))}')
        

        x_boxsize = rs.rs2_deproject_pixel_to_point(color_intr, [int(xmax), int(ymax)], distance) #ピクセル座標系からワールド座標へ座標返還        
        y_boxsize = rs.rs2_deproject_pixel_to_point(color_intr, [int(xmin), int(ymin)], distance) #ピクセル座標系からワールド座標へ座標返還        
        x_world = float(x_boxsize[0]) - float(y_boxsize[0])
        y_world = float(x_boxsize[1]) - float(y_boxsize[1])        

        
        threeD = rs.rs2_deproject_pixel_to_point(color_intr, [int(x_center), int(y_center)], distance) #ピクセル座標系からワールド座標へ座標返還
        return distance, math.degrees(math.atan2(x, z))




#メイン処理
def main():
    # Start streaming
    profile=pipeline.start(config)
    global before_distace, before_angle
    try:
        before_distance, before_angle = 0, 0
        while True:
            
            # Wait for a coherent pair of frames: depth and color
            try:
                frames = pipeline.wait_for_frames()
            except:
                break
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #推論実行
            result = model(color_image, conf=0.80)
            color_image =  result[0].plot()
            
            color_ir = rs.video_stream_profile(profile.get_stream(rs.stream.color)).get_intrinsics()
            #距離を出力
            result = output_distance(result, depth_frame, color_ir, color_image)

            if result is not None:
                distance, angle = result
                if before_distace != 0:
                    print(distance / before_distace)
                before_distace = distance

                if before_angle != 0:
                    print(angle / before_angle)
                before_angle = angle
            else:
                print("Output from output_distance is None.")
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # tracks = model.track(color_image, persist=True, show=False)
            # heatmap_image = heatmap_obj.generate_heatmap(color_image, tracks)

            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))


            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            print('pass')
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        # Stop streaming
        pipeline.stop()
        #cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':

    main()