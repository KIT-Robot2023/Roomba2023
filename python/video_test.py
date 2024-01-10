import numpy as np
import matplotlib.pyplot as plt
import cv2

# OpenCVの設定
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('out.mp4', fourcc, 20.0, (1000, 1000))

theta = np.linspace(0, 2*np.pi, 201)
delta_theta = np.linspace(0, 2*np.pi, 201)
b = 1.0
muki = True

for i in delta_theta:
    x = np.cos(theta)
    y1 = np.sin(theta + i)
    y2 = np.sin(b*theta)
    y3 = np.sin(2*theta + i)

    # 描画
    fig = plt.figure(figsize=(10,10))
    plt.plot(x, y1, 'b')
    plt.plot(x, y2, 'g')
    plt.plot(x, y3, 'r')
    fig.canvas.draw()

    # VideoWriterへ書き込み
    image_array = np.array(fig.canvas.renderer.buffer_rgba())
    im = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
    video.write(im)
    plt.close()

    if muki is True:
        b = b + 0.05
        if b > 6:
            muki = False
    else:
        b = b - 0.05

video.release