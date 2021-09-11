from calc_matrix import *
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
import cv2

def get_u_v(x, y, z, L):
    u = (x * L[0] + y * L[1] + z * L[2] + L[3]) / (x * L[8] + y * L[9] + z * L[10] + 1)
    v = (x * L[4] + y * L[5] + z * L[6] + L[7]) / (x * L[8] + y * L[9] + z * L[10] + 1)

def polygon_area(x, y):
    return abs(sum(x[i]*y[i-1] - y[i]*x[i-1] for i in range(len(x)))) / 2.

# def calc_area(x, y):
#     area = 0
#     for i in range(len(x)):
#         area += abs(x[i] * y[i-1] - x[i-1] * y[i])
#     return 0.5 * area

def create_convex_map(X, Y):
    array = []
    for x, y in zip(X, Y):
        array.append([x,y])
    array = np.array(array)
    hull = ConvexHull(array)
    plt.scatter(X, Y, label="key points")
    plt.xlabel("X [cm]")
    plt.ylabel("Y [cm]")
    plt.title("area ")
    #外周部分の座標配列
    x, y = [], []
    # simplex:array配列の結合部分のindex番号
    for simplex, vertice in zip(hull.simplices, hull.vertices):
        x.append(array[vertice][0])
        y.append(array[vertice][1])
        plt.plot(array[simplex, 0], array[simplex, 1], c="green")
    print(f"area : {polygon_area(x, y)} [cm]")

    plt.legend()
    # plt.show()

if __name__ == "__main__":
    X_color_M, uv_color = get_X_matrix_and_uv_list("color")
    X_gray_M,  uv_gray  = get_X_matrix_and_uv_list("gray")
    L1 = get_dlt_parameter(X_color_M, uv_color)
    L2 = get_dlt_parameter(X_gray_M, uv_gray)

    data = pd.read_csv("./data/pair_plot_position/all_keypoints.txt", header=None)
    xyz3s = np.load('./data/np_xyz.npy')
    x, y, z = xyz3s[:,0] , xyz3s[:,1], xyz3s[:,2] # kinectから読み込み m単位

    X, Y, Z = [], [], []
    for _, content in data.iterrows(): #dltから読み込み　cm単位
        position = list(map(int, content[0].split(" ")))
        x, y, z = get_3d_points(L1, L2, position[:2], position[2:4])
        X.append(x)
        Y.append(y)
        Z.append(-z)

    # create_convex_map(X, Y)#DLTから算出したもの
    create_convex_map(x, y)#Kinectから

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title("3D plot")
    ax.set_xlabel("x [cm]")
    ax.set_ylabel("y [cm]")
    ax.set_zlabel("z [cm]")

    # ax.scatter(X, Y, Z, marker="^")#DLT
    ax.scatter(x, y, z, marker="^")#Kinect
    plt.show()
