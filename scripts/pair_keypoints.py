import cv2
import numpy as np

def onClick_gray(event, u, v, flags, param):
    global file_name, color
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img_gray, (u, v), 5, color, -1)
        print(f"gray pixcel is {(u, v)}")
        with open (f"./data/pair_plot_position/{file_name}.txt", "a") as f:
            f.writelines(f"{u} {v} ")

def onClick_color(event, u, v, flags, param):
    global file_name, color
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img_color, (u, v), 5, color, -1)
        print(f"color pixcel is {(u, v)}")
        with open (f"./data/pair_plot_position/{file_name}.txt", "a") as f:
            f.writelines(f"{u} {v}")
            f.write("\n")

if __name__ == "__main__":
    file_name = input("input filename : ")
    image_window_gray = "img_gray"
    cv2.namedWindow("img_gray")
    cv2.setMouseCallback(image_window_gray, onClick_gray)
    img_gray = cv2.imread("./data/gray/0603/15m_s_1_trim/00000.jpg")

    image_window_color = "img_color"
    cv2.namedWindow("img_color")
    cv2.setMouseCallback(image_window_color, onClick_color)
    img_color = cv2.imread("./data/color/0603/15m_s_1_trim/00001.jpg")
    print(f"img gray : {img_gray.shape}")
    print(f"img color : {img_color.shape}")
    while True:
        color = tuple(np.random.randint(0, 256, 3, dtype="int"))
        color = (int(color[0]), int(color[1]), int(color[2]))
        cv2.imshow(image_window_gray, img_gray)
        cv2.imshow(image_window_color, img_color)
        cv2.waitKey(0)

        flag = input("stop is 0 ")
        if flag == "0":
            img = cv2.hconcat([img_gray, img_color])
            cv2.imwrite(f"./data/pair_plot_position/{file_name}.jpg", img)
            break
    # cv2.waitKey(0)
    # img_concat_horizontal = cv2.hconcat([img_gray, img_color])
    # cv2.imshow(image_window, img)