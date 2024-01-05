import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

class RoombaSimulator:
    def __init__(self):
        self.world_pos_position = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)]  # 初期位置 [x, y]
        self.odometry_position = [0, 0]  # オドメトリ

        self.world_orientation = random.uniform(-3.14, 3.14)  # 初期姿勢 (rad)
        self.orientation = 0

        self.left_wheel_rotation = 0  # 左車輪の回転角度 (rad)
        self.right_wheel_rotation = 0  # 右車輪の回転角度 (rad)

        self.wheel_radius = 0.072  # 車輪の半径 (50mmをmに変換)
        self.tread = 0.235  # トレッド (300mmをmに変換)
        self.size = 0.165

        self.delta_x = 0
        self.delta_y = 0
        self.delta_theta = 0


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

        # Roombaのワールド座標系での回転を更新
        self.world_orientation += self.delta_theta

    def plot(self):
        # Roombaの位置と姿勢をMatplotlibでプロット
        plt.clf()

        # 青い点でRoombaの中心を表現
        plt.plot(self.world_pos_position[0], self.world_pos_position[1], 'bo')

        # 半径0.165の円をプロット
        circle = plt.Circle((self.world_pos_position[0], self.world_pos_position[1]), 0.165, color='cyan', fill=False)
        plt.gca().add_patch(circle)

        # 赤い矢印で姿勢を表現
        line_length = 0.3
        line_dx = line_length * np.cos(self.world_orientation)
        line_dy = line_length * np.sin(self.world_orientation) #:.2f .format(self.world_pos_position[0])
        plt.arrow(self.world_pos_position[0], self.world_pos_position[1], line_dx, line_dy, color='red', width=0.02)


        # 台形を描画
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
        vertex1 = (self.world_pos_position[0] -  top_side_offset_Xcom + size_offset_Xcom,
                   self.world_pos_position[1] -  top_side_offset_Ycom + size_offset_Ycom)

        # 左上
        vertex4 = ((self.world_pos_position[0] -  bottom_side_offset_Xcom) + height_offset_Xcom,
                   (self.world_pos_position[1] -  bottom_side_offset_Ycom) + height_offset_Ycom)

        # 右端
        vertex2 = (self.world_pos_position[0] +  top_side_offset_Xcom + size_offset_Xcom,
                   self.world_pos_position[1] +  top_side_offset_Ycom + size_offset_Ycom)

        # 右上
        vertex3 = ((self.world_pos_position[0] +  bottom_side_offset_Xcom) + height_offset_Xcom,
                   (self.world_pos_position[1] +  bottom_side_offset_Ycom) + height_offset_Ycom)

        # 台形を描画
        trapezoid = plt.Polygon([vertex1, vertex2,vertex3,vertex4], fill=False, edgecolor='green')

        plt.gca().add_patch(trapezoid)

        print('{:.3f}'.format(self.world_pos_position[0]),
              ',','{:.3f}'.format(self.world_pos_position[1]),
              ',','{:.3f}'.format(self.world_orientation),
              ',','{:.3f}'.format(self.odometry_position[0]),
              ',','{:.3f}'.format(self.odometry_position[0]),
              ',','{:.3f}'.format(self.orientation))

        # グラフを正方形にし、目盛りを1ずつ増加
        plt.axis('equal')
        plt.xticks(np.arange(-2, 3, 0.5))
        plt.yticks(np.arange(-2, 3, 0.5))

        plt.title("Roomba Simulator")
        plt.grid(True)


# アニメーション用の関数
def animate(frame):
    # 左右の車輪の回転角度の差分を仮想的に生成
    left_wheel_rotation_delta = 1 * 1e-1 #0.1 * np.sin(frame * 0.1)
    right_wheel_rotation_delta = 1 * 1e-1 #0.1 * np.cos(frame * 0.1)

    roomba_simulator.odometry_update(left_wheel_rotation_delta, right_wheel_rotation_delta)
    roomba_simulator.world_pos_update()
    roomba_simulator.plot()

# RoombaSimulatorのインスタンス作成
roomba_simulator = RoombaSimulator()

# アニメーションの作成
animation = FuncAnimation(plt.figure(), animate, frames=range(200), interval=50)

# アニメーションの保存
animation.save('./python/movie/roomba_simulation.mp4', writer='ffmpeg', fps=20, dpi=300)

# アニメーションの表示
# plt.show()