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
    return abs(sum(x[i]*y[i-1] - y[i]*x[i-1] for i in range(len(x)))) / 2

# def calc_area(x, y):
#     area = 0
#     for i in range(len(x)):
#         area += abs(x[i] * y[i-1] - x[i-1] * y[i])
#     return 0.5 * area

def create_convex_map(X, Y):
    xy_lis = []
    for x, y in zip(X, Y):
        xy_lis.append([x,y])
    xy_lis = np.array(xy_lis)
    hull = ConvexHull(xy_lis)

    #外周部分の座標配列
    # x, y = [], []
    # simplex:array配列の結合部分のindex番号
    # for simplex, vertice in zip(hull.simplices, hull.vertices):
    #     x.append(xy_lis[vertice][0])
    #     y.append(xy_lis[vertice][1])
    #     plt.plot(xy_lis[simplex, 0], xy_lis[simplex, 1], c="green")


    return hull.simplices, hull.vertices

def plot_3d(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("3D plot")
    ax.set_xlabel("x [cm]")
    ax.set_ylabel("y [cm]")
    ax.set_zlabel("z [cm]")
    ax.scatter(x, y, z, marker="^")

def plot_2d(x, y, simplices=None, vertices=None):
    fig = plt.figure()
    plt.scatter(x, y, label="key points")
    plt.xlabel("X [cm]")
    plt.ylabel("Y [cm]")
    plt.title("area ")
    for simplex, vertice in zip(simplices, vertices):
        plt.plot(x[simplex], y[simplex], c="green")
    print(f"area : {polygon_area(x, y)} [cm]")

if __name__ == "__main__":
    X_color_M, uv_color = get_X_matrix_and_uv_list("color")
    X_gray_M,  uv_gray  = get_X_matrix_and_uv_list("gray")
    L1 = get_dlt_parameter(X_color_M, uv_color)
    L2 = get_dlt_parameter(X_gray_M, uv_gray)

    data = pd.read_csv("./data/pair_plot_position/all_keypoints.txt", header=None)
    xyz3s = np.load('./data/np_xyz.npy')
    x_kin, y_kin, z_kin = xyz3s[:,0] * 100 , xyz3s[:,1] * 100, xyz3s[:,2] * 100 # kinectから読み込み cm→m単位

    X_dlt, Y_dlt, Z_dlt = [], [], []
    for _, content in data.iterrows(): #dltから読み込み　cm単位
        position = list(map(int, content[0].split(" ")))
        x, y, z = get_3d_points(L1, L2, position[:2], position[2:4])
        X_dlt.append(x)
        Y_dlt.append(y)
        Z_dlt.append(-z)

    # plot_3d(X_dlt, Y_dlt, Z_dlt)
    plot_3d(x_kin, y_kin, z_kin)
    sim, con = create_convex_map(x_kin, y_kin)
    # create_convex_map(X_dlt, Y_dlt)#DLTから算出したもの
    plot_2d(x_kin, y_kin, sim, con)#Kinectから

    plt.show()
