# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import json
import os
import copy
import math


def main():
    QieMian = ["心尖四腔心切面"]
    cur_path = "./zq50+(1)"
    cur_path_json = os.path.join(cur_path, "annotations.json")
    f = open(cur_path_json, encoding='utf-8')
    frame = json.load(f)
    annotations = frame["annotations"]
    for x in annotations:
        pic_path = os.path.join(cur_path, str(x))
        if not os.path.exists(pic_path):
            continue
        img = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), 1)
        sp = img.shape  # [高|宽|像素值由三种原色构成]
        print("图片尺寸：  ",sp)
        if annotations[x]['bodyPart'] not in QieMian:
            continue
        for y in annotations[x]["annotations"]:
            if y["name"] in ["胸腔面积","心脏面积"]:
                cur_vertex = copy.deepcopy(y["vertex"])
                print(x,"的",y["name"],":")
                #print(cur_vertex)
                list_cur_vertex = cur_vertex.split(";")
                points = []
                for vertex in list_cur_vertex:
                    cur_x = (float(vertex.split(",")[0]))
                    cur_y = (float(vertex.split(",")[1]))
                    points.append([cur_x,cur_y])
                print("points:",points)
                polygon = np.array([points], dtype=np.int32)
                #直接用opencv的函数进行计算
                g_dsrcArea = cv2.contourArea(polygon,True)
                # 利用像素填充进行计算
                # im 的求解必须放在for循环内部  放在外部第二次会被覆盖
                im = np.zeros(img.shape[:2], dtype="uint8")
                polygon_mask = cv2.fillPoly(im, polygon, 255)
                area = np.sum(np.greater(polygon_mask, 0))
                print(area)
                print(math.ceil(area))
                print(abs(g_dsrcArea))
                #assert math.ceil(area)==1

if __name__ == '__main__':
    main()
    print("OK")