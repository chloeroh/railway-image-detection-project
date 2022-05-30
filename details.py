'''
augment : .Mat
return : tuple
'''

import numpy as np
import pandas as pd
import cv2
import math
import statistics

class Details:
    def __init__(self, file_name):
        self.pic_array = sio.loadmat(file_name)
    
    def findLocation(self):
        # x1, y1
        y1_list, x1_list = np.where(self.pic_array == 0)[0], np.where(self.pic_array == 0)[1]
        y1_list_median = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][x1_list[0]]!=255]
        x1 = x1_list[0]
        y1 = round((y1_list_median[0] + y1_list_median[-1])/2)
                
        # x2, y2
        flip_y = np.flip(self.pic_array, axis = 1)
        starting_point = round(np.shape(flip_y)[1]/6)
        x2_flip = 0
            
        for j in list(range(starting_point, flip_y.shape[1]-starting_point)):
            for i in range(flip_y.shape[0]):
                list_flip_y = list(flip_y[i][j-starting_point:j+starting_point])
                if flip_y[i][j]==0 and list_flip_y.count(0)==starting_point*2:
                    x2_flip = j-starting_point
                    break
                else : continue
            if x2_flip != 0 : break
            else : continue

        x2 = flip_y.shape[1] - x2_flip - 15
        y2_list = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][x2]!=255]
        y2 = int(statistics.median(y2_list))
        
        # x3, y3
        y3_list = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][0]!=255]
        if len(y3_list) == 0:
            j = -1
            while len(y3_list) == 0 :
                j+=1
                y3_list = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][j]!=255]
        y3 = int(statistics.median(y3_list))
        x3 = 0

        # x4, y4
        y4_list = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][-1]!=255]
        j = 0
        if len(y4_list) == 0:
            while len(y4_list) == 0:
                j = j-1
                y4_list = [i for i in range(self.pic_array.shape[0]) if self.pic_array[i][j]!=255]
        y4 = int(statistics.median(y4_list)) + 5
        x4 = self.pic_array.shape[1]
        
#         location_dic = {'x1y1': [x1,y1], 'x2y2': [x2,y2], 'x3y3': [x3,y3], 'x4y4':[x4,y4]}
        location_tuple = ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
        return location_tuple
    
    def findLength_pixel(self, location_tuple):
        self.location_tuple = location_tuple
        # (x1, y1) - (x3, y3)
        a = math.dist(location_tuple[0], location_tuple[2])

        # (x1, y1) - (x2, y2)
        b = math.dist(location_tuple[0], location_tuple[1])
    
        # (x2, y2) - (x4, y4)
        c = math.dist(location_tuple[1], location_tuple[3])

        # extra (x3, y3) - (x2, y2) for left angle
        d = math.dist(location_tuple[2], location_tuple[1])

        # extra (x1, y1) - (x4, y4) for right angle
        e = math.dist(location_tuple[0], location_tuple[3])

        
        # total length (x3, y3) - (x4, y4)
        total = math.dist(location_tuple[2], location_tuple[3])

        
        length_pixel_tuple = (a,b,c,d,e,total)
        return length_pixel_tuple
    
    def findAngle(self, length_pixel_dic):
        #find triangle size with Heron Formula
        self.length_pixel_dic = length_pixel_dic
        a,b,c = self.length_pixel_tuple[0], self.length_pixel_tuple[1], self.length_pixel_tuple[2]
        d,e = self.length_pixel_tuple[3], self.length_pixel_tuple[4]
        
        # triangle size formula function
        def heron_formula(len_1, len_2, len_3):
            s = (len_1 + len_2 + len_3)/2
            triangle_size = math.sqrt(s*(s-len_1)*(s-len_2)*(s-len_3))
            return triangle_size

        # angle function
        def subtract_angle(triangle_size, len_1, len_2):
            sin_radian = (2*triangle_size)/(len_1*len_2) #  angle > 90
            angle_360 = ((math.asin(sin_radian))/math.pi)*180
            if angle_360 < 90 : angle_final = 180-angle_360
            else : angle_final = angle_360
            return angle_final
        
        # Left angle
        left_triangle = heron_formula(a,b,d)
        left_angle = subtract_angle(left_triangle, a, b)
        
        # Right angle
        right_triangle = heron_formula(b,c,e)
        right_angle = subtract_angle(right_triangle, b, c)
        
#         angle_dic = {'left_angle' : left_angle, 'right_angle': right_angle}
        angle_tuple = (left_angle, right_angle) 
        return angle_tuple