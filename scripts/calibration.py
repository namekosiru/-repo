import os
import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

a = 6
b = 9
objp = np.zeros((b*a,3), np.float32) 
objp[:,:2] = np.mgrid[0:a,0:b].T.reshape(-1,2) .T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


current_path = os.getcwd()
machine_name_index = int(input("color:0, gray:1, gopro:2, muson:3 "))
machine_list = ["color", "gray", "gopro", "muson"]
machine_name = machine_list[machine_name_index]
date_name    = input("Please input date :")
folder_name    = input("Please input folder_name :")

save_dir_path  = os.path.join(current_path, "data", machine_name, date_name, folder_name)


images = glob.glob(os.path.join(save_dir_path, '*.jpg'))
if not images:
    exit("invalid folder_name")

for fname in images:
    img = cv2.imread(fname)
    print(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (a,b),None)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(0)

cv2.destroyAllWindows()