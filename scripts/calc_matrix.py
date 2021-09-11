import numpy as np
def get_X_matrix_and_uv_list(color):
    # calib1 = np.loadtxt(f"./data/calibration_txt/calibration_down_{color}.txt", delimiter=" ", dtype="int64") #mm
    # calib2 = np.loadtxt(f"./data/calibration_txt/calibration_down+_{color}.txt", delimiter=" ", dtype="int64")
    # uv_list1 = np.loadtxt(f"./data/calibration_txt/calibration_down_{color}_uv.txt", delimiter=" ", dtype="int64")
    # uv_list2 = np.loadtxt(f"./data/calibration_txt/calibration_down+_{color}_uv.txt", delimiter=" ", dtype="int64")
    calib1 = np.loadtxt(f"./data/calibration_txt/{color}_down.txt", delimiter=" ", dtype="int64") #cm
    calib2 = np.loadtxt(f"./data/calibration_txt/{color}_down+.txt", delimiter=" ", dtype="int64")
    uv_list1 = np.loadtxt(f"./data/calibration_txt/{color}_down_uv.txt", delimiter=" ", dtype="int64")
    uv_list2 = np.loadtxt(f"./data/calibration_txt/{color}_down+_uv.txt", delimiter=" ", dtype="int64")
    X_matrix = np.concatenate([calib1, calib2])
    uv_list = np.concatenate([uv_list1, uv_list2])
    return X_matrix, uv_list

def get_dlt_parameter(X_matrix, uv_matrix):
    X_inv = np.linalg.inv(np.dot(X_matrix.T, X_matrix))
    return X_inv @ X_matrix.T @ uv_matrix

def get_3d_points(L1, L2, uv1, uv2):
    x1, y1 = uv1[0], uv1[1]
    x2, y2 = uv2[0], uv2[1]
    A_matrix = np.array([
                        [L1[0] - L1[8] * x1, L1[1] - L1[9] * x1, L1[2] - L1[10] * x1],
                        [L1[4] - L1[8] * y1, L1[5] - L1[9] * y1, L1[6] - L1[10] * y1],
                        [L2[0] - L2[8] * x2, L2[1] - L2[9] * x2, L2[2] - L2[10] * x2],
                        [L2[4] - L2[8] * y2, L2[5] - L2[9] * y2, L2[6] - L2[10] * y2],
                        ])
    B_matrix = np.array([x1 - L1[3], y1 - L1[7], x2 - L2[3], y2 - L2[7]])
    x, y, z = get_dlt_parameter(A_matrix, B_matrix)
    return x, y, z



if __name__ == "__main__":
    X_color_M, uv_color = get_X_matrix_and_uv_list("color")
    X_gray_M,  uv_gray  = get_X_matrix_and_uv_list("gray")
    L1 = get_dlt_parameter(X_color_M, uv_color)
    L2 = get_dlt_parameter(X_gray_M, uv_gray)
    x, y, z = get_3d_points(L1, L2, uv_color[:2], uv_gray[:2])
    print(f"L1 : {L1}")
    print(f"L2 : {L2}")
