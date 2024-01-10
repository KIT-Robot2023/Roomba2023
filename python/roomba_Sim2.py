import numpy as np
import random
import cv2

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RoombaSimulator:
    def __init__(self):
        self.world_pos_position = [0, 0]  # 初期位置 [x, y]
        self.world_pos_position_pre = [0, 0]
        self.ball_pos_position = [0, 0]  # ボールの初期位置 [x, y]
        self.odometry_position = [0, 0]  # オドメトリ
        self.odometry_position_pre = [0, 0]

        self.world_orientation = 0   # 初期姿勢 (rad)
        self.orientation = 0

        self.left_wheel_rotation = 0  # 左車輪の回転角度 (rad)
        self.right_wheel_rotation = 0  # 右車輪の回転角度 (rad)

        self.wheel_radius = 0.072  # 車輪の半径 (50mmをmに変換)
        self.tread = 0.235  # トレッド
        self.size = 0.165 # Roombaの半径

        self.one_side_of_area = 1 #行動環境の一辺の長さ

        self.delta_x = 0
        self.delta_y = 0
        self.delta_theta = 0

        self.vertex1 = (0,0)
        self.vertex2 = (0,0)
        self.vertex3 = (0,0)
        self.vertex4 = (0,0)

        self.animation = []

        '''openCV'''
        self.fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        self.video = cv2.VideoWriter('out.mp4', self.fourcc, 20.0, (1000, 1000))
        self.fig = plt.figure(figsize=(10,10))

    def random_pos(self):
        self.world_pos_position = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]  # 初期位置 [x, y]
        self.ball_pos_position = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]  # ボールの初期位置 [x, y]
        self.world_orientation = random.uniform(-3.14, 3.14)


    def odometry_update(self, left_wheel_rotation_delta, right_wheel_rotation_delta):
        # 車輪の回転角度を更新
        self.left_wheel_rotation += left_wheel_rotation_delta
        self.right_wheel_rotation += right_wheel_rotation_delta

        # Roombaの位置と姿勢を更新
        left_wheel_distance = left_wheel_rotation_delta * self.wheel_radius
        right_wheel_distance = right_wheel_rotation_delta * self.wheel_radius

        delta_distance = (left_wheel_distance + right_wheel_distance) / 2
        self.delta_theta = (right_wheel_distance - left_wheel_distance) / self.tread

        self.delta_x = delta_distance * np.cos(self.orientation)
        self.delta_y = delta_distance * np.sin(self.orientation)

        self.odometry_position[0] += self.delta_x
        self.odometry_position[1] += self.delta_y
        self.orientation += self.delta_theta


    def world_pos_update(self):
        # Roombaのワールド座標系での移動を計算
        world_delta_x = np.cos(self.world_orientation) * self.delta_x - np.sin(self.world_orientation) * self.delta_y
        world_delta_y = np.sin(self.world_orientation) * self.delta_x + np.cos(self.world_orientation) * self.delta_y

        # Roombaのワールド座標系での位置を更新
        self.world_pos_position[0] += world_delta_x
        self.world_pos_position[1] += world_delta_y

        #壁に突っ込んだら，座標を更新しない．
        if abs(self.world_pos_position[0])+self.size < self.one_side_of_area/2 and\
           abs(self.world_pos_position[1])+self.size < self.one_side_of_area/2:

            self.world_pos_position_pre[0] = self.world_pos_position[0]
            self.world_pos_position_pre[1] = self.world_pos_position[1]

            self.odometry_position_pre[0] = self.odometry_position[0]
            self.odometry_position_pre[1] = self.odometry_position[1]

        else:
            self.world_pos_position[0] = self.world_pos_position_pre[0]
            self.world_pos_position[1] = self.world_pos_position_pre[1]

            self.odometry_position[0] = self.odometry_position_pre[0]
            self.odometry_position[1] = self.odometry_position_pre[1]

        # Roombaのワールド座標系での回転を更新
        self.world_orientation += self.delta_theta

        '''ホモグラフィ変換された視野'''
        trapezoid_length_Top_side = 0.2  # 台形の下辺の長さ
        trapezoid_length_Bottom_side = 0.5  # 台形の下辺の長さ
        trapezoid_height = 0.5  # 台形の高さ

        top_side_offset_Xcom = trapezoid_length_Top_side/2 * np.cos(self.world_orientation + np.pi/2)
        top_side_offset_Ycom = trapezoid_length_Top_side/2 * np.sin(self.world_orientation + np.pi/2)
        bottom_side_offset_Xcom = trapezoid_length_Bottom_side/2 * np.cos(self.world_orientation + np.pi/2)
        bottom_side_offset_Ycom = trapezoid_length_Bottom_side/2 * np.sin(self.world_orientation + np.pi/2)

        height_offset_Xcom = trapezoid_height * np.cos(self.world_orientation)
        height_offset_Ycom = trapezoid_height * np.sin(self.world_orientation)

        size_offset_Xcom = self.size * np.cos(self.world_orientation)
        size_offset_Ycom = self.size * np.sin(self.world_orientation)

        # 台形の頂点座標
        # 左端
        self.vertex1 = (self.world_pos_position[0] -  top_side_offset_Xcom + size_offset_Xcom,
                   self.world_pos_position[1] -  top_side_offset_Ycom + size_offset_Ycom)

        # 左上
        self.vertex4 = ((self.world_pos_position[0] -  bottom_side_offset_Xcom) + height_offset_Xcom,
                   (self.world_pos_position[1] -  bottom_side_offset_Ycom) + height_offset_Ycom)

        # 右端
        self.vertex2 = (self.world_pos_position[0] +  top_side_offset_Xcom + size_offset_Xcom,
                   self.world_pos_position[1] +  top_side_offset_Ycom + size_offset_Ycom)

        # 右上
        self.vertex3 = ((self.world_pos_position[0] +  bottom_side_offset_Xcom) + height_offset_Xcom,
                   (self.world_pos_position[1] +  bottom_side_offset_Ycom) + height_offset_Ycom)

    def plot(self):
        # Roombaの位置と姿勢をMatplotlibでプロット
        plt.clf()

        # 青い点でRoombaの中心を表現
        plt.plot(self.world_pos_position[0], self.world_pos_position[1], 'bo')

        # 赤い点でballの中心を表現
        plt.plot(self.ball_pos_position[0], self.ball_pos_position[1], 'ro')

        # 半径0.165の円をプロット
        circle = plt.Circle((self.world_pos_position[0], self.world_pos_position[1]), 0.165, color='cyan', fill=False)
        plt.gca().add_patch(circle)

        # 赤い矢印で姿勢を表現
        line_length = 0.3
        line_dx = line_length * np.cos(self.world_orientation)
        line_dy = line_length * np.sin(self.world_orientation) #:.2f .format(self.world_pos_position[0])

        plt.arrow(self.world_pos_position[0], self.world_pos_position[1], line_dx, line_dy, color='red', width=0.02)

        # 視野を描画
        trapezoid = plt.Polygon([self.vertex1, self.vertex2,self.vertex3,self.vertex4], fill=False, edgecolor='green')

        plt.gca().add_patch(trapezoid)

        # print('{:.3f}'.format(self.world_pos_position[0]),
        #       ',','{:.3f}'.format(self.world_pos_position[1]),
        #       ',','{:.3f}'.format(self.world_orientation),
        #       ',','{:.3f}'.format(self.odometry_position[0]),
        #       ',','{:.3f}'.format(self.odometry_position[0]),
        #       ',','{:.3f}'.format(self.orientation))

        # グラフを正方形にし、目盛りを1ずつ増加
        plt.axis('equal')
        plt.xticks(np.arange(-2, 3, 0.5))
        plt.yticks(np.arange(-2, 3, 0.5))

        plt.title("Roomba Simulator")
        plt.grid(True)

        '''動画作成'''
        self.fig.canvas.draw()
        image_array = np.array(self.fig.canvas.renderer.buffer_rgba())
        im = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
        self.video.write(im)

    def is_inside_trapezoid(self):
        def cross_product(ax, ay, bx, by, cx, cy):
            return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

        # 連続する頂点の各ペアについて外積を計算する．
        cross_product_ver1to2 = cross_product(self.vertex1[0], self.vertex1[1], self.vertex2[0], self.vertex2[1], self.ball_pos_position[0], self.ball_pos_position[1])
        cross_product_ver2to3 = cross_product(self.vertex2[0], self.vertex2[1], self.vertex3[0], self.vertex3[1], self.ball_pos_position[0], self.ball_pos_position[1])
        cross_product_ver3to4 = cross_product(self.vertex3[0], self.vertex3[1], self.vertex4[0], self.vertex4[1], self.ball_pos_position[0], self.ball_pos_position[1])
        cross_product_ver4to1 = cross_product(self.vertex4[0], self.vertex4[1], self.vertex1[0], self.vertex1[1], self.ball_pos_position[0], self.ball_pos_position[1])

        # ballが台形内に入っているかを判定する．
        if (cross_product_ver1to2 >= 0 and cross_product_ver2to3 >= 0 and
                cross_product_ver3to4 >= 0 and cross_product_ver4to1 >= 0) or \
        (cross_product_ver1to2 <= 0 and cross_product_ver2to3 <= 0 and
                cross_product_ver3to4 <= 0 and cross_product_ver4to1 <= 0):
            return True
        else:
            return False

    def get_world_pos_ori(self):
        return self.world_pos_position[0],self.world_pos_position[1],self.world_orientation

    def get_ball_pos(self):
        if self.is_inside_trapezoid():
            return self.ball_pos_position[0], self.ball_pos_position[1]
        else:
            return [-10,-10]

    def touch_ball(self):
        if np.sqrt((self.world_pos_position[0]-self.ball_pos_position[0])**2
                   +(self.world_pos_position[0]-self.ball_pos_position[0])**2) <= 0.165:
            return True
        else:
            return False

    def animate(self):
        print("hoge")
        # one_frame = self.plot()
        # self.animation.append(one_frame)

    def save_animation(self):
        self.video.release()
        print("アニメーションが正常に保存されました。")