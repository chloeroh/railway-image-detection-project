import numpy as np
import pandas as pd
import cv2

class Filter:
    def __init__(self, img):
        self.img = img

    def decide_colourbound(self):        
#         img = cv2.imread(self.pic_name)
        img_HSV = (cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)).reshape(self.img.shape[0]*self.img.shape[1],3)
        row0_H = np.average([row[0] for row in img_HSV])
        row1_S = np.average([row[1] for row in img_HSV])
        row2_V = np.average([row[2] for row in img_HSV])
        
        if row2_V > 30:
            if row0_H < 30:
                lowerbound = (0, 100, 0)
                upperbound = (255, 255, 20)
            else:
                lowerbound = (0, 200, 0)
                upperbound = (255, 255, 255)
        elif row2_V <= 30:
            lowerbound = (0, 40, 0)
            upperbound = (255, 255, 255)
        return lowerbound, upperbound
        
    def filter_image(self, lowerbound, upperbound):
        img = cv2.resize(self.img, dsize=(200*2, 140*2), interpolation=cv2.INTER_CUBIC)
        self.lowerbound = lowerbound
        self.upperbound = upperbound
        filtering = cv2.inRange(img, self.lowerbound, self.upperbound)
        _, binary_img = cv2.threshold(filtering, 10, 255, cv2.THRESH_BINARY_INV)
        return img, binary_img