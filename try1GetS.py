
import math
import os
import json
import copy
import cv2
import numpy as np
class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
def GetAreaOfPolyGon(points):
    # 计算多边形面积
    area = 0
    if(len(points)<3):
         raise Exception("error")
    p1 = points[0]
    for i in range(1,len(points)-1):
        p2 = points[i]
        p3 = points[i + 1]
        #计算向量
        vecp1p2 = Point(p2.x-p1.x,p2.y-p1.y)
        vecp2p3 = Point(p3.x-p2.x,p3.y-p2.y)
        #判断顺时针还是逆时针，顺时针面积为正，逆时针面积为负
        vecMult = vecp1p2.x*vecp2p3.y - vecp1p2.y*vecp2p3.x   #判断正负方向比较有意思
        sign = 0
        if(vecMult>0):
            sign = 1
        elif(vecMult<0):
            sign = -1
        triArea = GetAreaOfTriangle(p1,p2,p3)*sign
        #print(triArea)
        area += triArea
    return abs(area)

def GetAreaOfTriangle(p1,p2,p3):
    '''计算三角形面积   海伦公式'''
    area = 0
    p1p2 = GetLineLength(p1,p2)
    p2p3 = GetLineLength(p2,p3)
    p3p1 = GetLineLength(p3,p1)
    s = (p1p2 + p2p3 + p3p1)/2
    area = s*(s-p1p2)*(s-p2p3)*(s-p3p1)   #海伦公式
    area = math.sqrt(area)
    return area

def GetLineLength(p1,p2):
    '''计算边长'''
    length = math.pow((p1.x-p2.x),2) + math.pow((p1.y-p2.y),2)  #pow  次方
    length = math.sqrt(length)
    return length

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
                # print(cur_vertex)
                list_cur_vertex = cur_vertex.split(";")
                points = []
                cur_x = []
                cur_y = []
                for vertex in list_cur_vertex:
                    cur_x.append(float(vertex.split(",")[0]))
                    cur_y.append(float(vertex.split(",")[1]))
                # print("x:  ",x)
                # print("y:  ",y)
                for index in range(len(cur_x)):
                    points.append(Point(cur_x[index],cur_y[index]))
                area = GetAreaOfPolyGon(points)
                print(area)
                print(math.ceil(area))
                #assert math.ceil(area)==1

if __name__ == '__main__':
    main()
    print("OK")