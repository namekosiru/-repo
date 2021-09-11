import cv2
import numpy as np
import os

machine_name_index = int(input("color:0, gray:1 "))
date_name    = input("Please input date :")
file_name    = input("Please input file_name :")

current_path = os.getcwd()
machine_list = ["color", "gray"]
machine_name = machine_list[machine_name_index]



read_movie_path   = os.path.join(current_path, "data",  machine_name, date_name, file_name)
save_dir_path     = os.path.join(current_path, "data",  machine_name, date_name, file_name.split(".")[0])

try:
    os.makedirs(save_dir_path)
    print("create ", save_dir_path)
except:
    pass

cap = cv2.VideoCapture(read_movie_path)
i = 0
while (True):
    print(i)
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("frame", gray)
        save_name = f"{i:05}.jpg"
        save_path = os.path.join(save_dir_path, save_name)
        cv2.imwrite(save_path, gray)
        cv2.waitKey(5)
        i += 1
        # 最初の数枚だけ保存
        if i >= 100:
            exit(f"crop {i-1} images")
    else:
        print("finished")
        exit()