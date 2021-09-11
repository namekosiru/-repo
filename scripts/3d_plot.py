from calc_matrix import *
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
import cv2

class Plot_Utils():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xy = [[i, j] for i, j in zip(self.x, self.y)]
        self.hull = ConvexHull(self.xy)

    def plot_3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title("3D plot")
        ax.set_xlabel("x [cm]")
        ax.set_ylabel("y [cm]")
        ax.set_zlabel("z [cm]")
        ax.scatter(self.x, self.y, self.z, marker="^")

    def plot_2d(self):
        points = self.hull.points
        hull_points = points[self.hull.vertices]
        hp = np.vstack((hull_points, hull_points[0]))
        print(f"area : {self._polygon_area(hp[:,0], hp[:,1])} [cm]")       

        fig = plt.figure()
        plt.scatter(self.x, self.y, label="key points")
        plt.xlabel("X [cm]")
        plt.ylabel("Y [cm]")
        plt.title("area")
        plt.plot(hp[:,0], hp[:,1], c="green", label="outline")
        plt.legend()     

    def _polygon_area(self, x, y):
        return abs(sum(x[i]*y[i-1] - y[i]*x[i-1] for i in range(len(x)))) / 2

def get_u_v(x, y, z, L):
    u = (x * L[0] + y * L[1] + z * L[2] + L[3]) / (x * L[8] + y * L[9] + z * L[10] + 1)
    v = (x * L[4] + y * L[5] + z * L[6] + L[7]) / (x * L[8] + y * L[9] + z * L[10] + 1)



if __name__ == "__main__":
    X_color_M, uv_color = get_X_matrix_and_uv_list("color")
    X_gray_M,  uv_gray  = get_X_matrix_and_uv_list("gray")
    L1 = get_dlt_parameter(X_color_M, uv_color)
    L2 = get_dlt_parameter(X_gray_M, uv_gray)

    xyz3s = np.load('./data/np_xyz.npy')
    x_kin, y_kin, z_kin = xyz3s[:,0] * 100 , xyz3s[:,1] * 100, xyz3s[:,2] * 100 # kinectから読み込み cm→m単位

    data = pd.read_csv("./data/pair_plot_position/all_keypoints.txt", header=None)
    X_dlt, Y_dlt, Z_dlt = [], [], []
    for _, content in data.iterrows(): #dltから読み込み　cm単位
        position = list(map(int, content[0].split(" ")))
        x, y, z = get_3d_points(L1, L2, position[:2], position[2:4])
        X_dlt.append(x)
        Y_dlt.append(y)
        Z_dlt.append(-z)

    kinect = Plot_Utils(x_kin, y_kin, z_kin)
    kinect.plot_3d()
    kinect.plot_2d()
    # dlt = Plot_Utils(X_dlt, Y_dlt, Z_dlt)

    plt.show()
