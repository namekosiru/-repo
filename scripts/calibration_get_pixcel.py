import cv2

def onClick(event, u, v, flags, param):
    global file_name, u_v_list
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (u, v), 5, (255, 0, 0), -1)
        print(f"pixcel is {(u, v)}")
        u_v_list.append(str(u))
        u_v_list.append(str(v))
        try:
            cordinate_3d = list(input("input x, y, z as x y z : ").split(" "))
            list_u = create_line_u(cordinate_3d, u)
            list_v = create_line_v(cordinate_3d, v)
        except Exception as e:
            print("please retry")
            cordinate_3d = list(input("input x, y, z as x y z : ").split(" "))
            list_u = create_line_u(cordinate_3d, u)
            list_v = create_line_v(cordinate_3d, v)

        with open (f"./data/calibration_txt/{file_name}.txt", "a") as f:
            f.writelines(" ".join(list_u))
            f.write("\n")
            f.writelines(" ".join(list_v))
            f.write("\n")
        print("finished write")
        print("terminate operation please enter esc")

def create_line_u(cordinate_3d, u):
    x, y, z = cordinate_3d[0], cordinate_3d[1], cordinate_3d[2]
    ux = str(- u * int(x))
    uy = str(- u * int(y))
    uz = str(- u * int(z))
    return [x, y, z, "1", "0", "0", "0", "0", ux, uy, uz]

def create_line_v(cordinate_3d, v):
    x, y, z = cordinate_3d[0], cordinate_3d[1], cordinate_3d[2]
    vx = str(- v * int(x))
    vy = str(- v * int(y))
    vz = str(- v * int(z))
    return ["0", "0", "0", "0", x, y, z, "1", vx, vy, vz]

if __name__ == "__main__":
    u_v_list = []
    file_name = input("please output filename : ")
    image_window = "img"
    img = cv2.imread("./data/color/0603/Calibration_Down+/00000.jpg")
    cv2.namedWindow("img")
    cv2.setMouseCallback(image_window, onClick)
    print(f"image shape : {img.shape}")
    while True:
        cv2.imshow(image_window, img)
        if cv2.waitKey(10) == 27:
            with open (f"./data/calibration_txt/{file_name}_uv.txt", "w") as f:
                f.writelines(" ".join(u_v_list))
            cv2.imwrite(f"./data/calibration_txt/{file_name}.jpg", img)
            break
    cv2.destroyAllWindows()