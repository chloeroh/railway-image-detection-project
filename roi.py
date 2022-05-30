import numpy as np
import pandas as pd
import cv2

def roi(target_img, original_image):
    w,h = target_img.shape[:2]
    image_original = cv2.imread(original_image)
    img_gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)
    
    noise = cv2.randn(np.zeros(img_gray.shape, np.int32),50,10)
    src = cv2.add(img_gray, noise, dtype=cv2.CV_8UC3)
    
    res = cv2.matchTemplate(src, target_img, cv2.TM_CCOEFF_NORMED)
    _, maxv, _, maxloc = cv2.minMaxLoc(res)
    
    cropped_img = image_original[maxloc[1]+100:maxloc[1]+h-250, maxloc[0]+5:maxloc[0]+w+40]
#     cropped_interpolation_img = cv2.resize(cropped_gray_img, dsize=(200*2, 140*2), interpolation=cv2.INTER_CUBIC)

    return cropped_img #np.average(cropped_gray_img) > 100 : Fail crop