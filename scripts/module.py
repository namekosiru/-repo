import os
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

def otsu(img):
    #otsuの二値化
    ret, frame = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    cv2.imshow("origin", img)
    cv2.imshow("Otsu", frame)
    cv2.waitKey(0)

def calc_keypoints(img, type_name):
    #特徴点の計算
    if type_name == "sift":
        sift = cv2.xfeatures2d.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(img, None)
        return keypoints, descriptors
    elif type_name == "orb":
        orb = cv2.ORB_create()
        #keypoints = orb.detect(img,None)
        #keypoints, descriptors = orb.compute(img, keypoints)
        #上の二行はdetectAndComputeと等しい
        #descriptors:(特徴点の数, 特徴量記述子の次元数)
        keypoints, descriptors = orb.detectAndCompute(img, None)
        return keypoints, descriptors

def draw_keypoints(img, keypoints, name="test"):
    #特徴点の描画
    img_keypoints = cv2.drawKeypoints(img,keypoints, outImage=None)
    cv2.imshow("origin", img)
    cv2.imshow("keypoints", img_keypoints)
    # cv2.imwrite(f"{name}.jpg", img_keypoints)
    cv2.waitKey(0)


if __name__ == "__main__":
    current_path = os.getcwd()
    load_path = input("please input load_folder_path: ")
    images = glob.glob(os.path.join(load_path, '*.jpg'))

    # for image in images:
    img1 = cv2.imread("C:\\Users\\kazulab07\\Desktop\\daitei\\data\\color\\0603\\15m_s_1_trim\\00001.jpg",0)
    img2 = cv2.imread("C:\\Users\\kazulab07\\Desktop\\daitei\\data\\gray\\0603\\15m_s_1_trim\\00000.jpg",0)


    keypoints1, descriptors1 = calc_keypoints(img1, "orb")
    keypoints2, descriptors2 = calc_keypoints(img2, "orb")
    draw_keypoints(img1, keypoints1, "key1")
    draw_keypoints(img2, keypoints2, "key2")
    
    #総当たりマッチング orb
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    # Draw first 10 matches.
    img3 = cv2.drawMatches(img1,keypoints1,img2,keypoints2,matches[:10],outImg=None, flags=2)
    cv2.imwrite("img3.jpg", img3)
    cv2.imshow("img3", img3)
    cv2.waitKey(0)
    # m = matches[0]
    # query_pt, train_pt = keypoints1[m.queryIdx], keypoints2[m.trainIdx]
    # query_desc, train_desc = descriptors1[m.queryIdx], descriptors2[m.trainIdx]
    # dst = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None)
    # cv2.imshow("img", dst)
    # cv2.waitKey(0)



    # cv2.imshow("img", img_sift)
    # cv2.waitKey(0)
    # for image in images:
    #     img  = cv2.imread(image, 0)
    #     canny_img = cv2.Canny(img, 50, 110)
    #     hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    #     plt.hist(hist)
    #     plt.show()
    #     cv2.imshow("canny", canny_img)
    #     cv2.waitKey(0)