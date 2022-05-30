import math

def realLength_cm(location_dic, findLength_pixels_dic):
    straightline_pixels = math.dist((location_dic['x1y1'][0], location_dic['x1y1'][1]), 
                                    (location_dic['x2y2'][0],location_dic['x1y1'][1]))
    rail_middle_cm = round(18.4-13, 4)
    cm_pixels = straightline_pixels/rail_middle_cm
    part1 = round(findLength_pixels_dic['a']/cm_pixels,4)
    part2 = round(findLength_pixels_dic['b']/cm_pixels,4)
    part3 = round(findLength_pixels_dic['c']/cm_pixels,4)
    total = round(findLength_pixels_dic['total']/cm_pixels,4)
    
    length_cm_dic = {'part1': part1, 'part2': part2, 'part3': part3, 'total' : total}
    return length_cm_dic