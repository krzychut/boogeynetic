##___point.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from settings import*

class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b
    def getPoint(self):
        return self.x, self.y
    def pointMean(self, point_2):
        tmp_point = Point()
        tmp_point.x = int((self.x + point_2.x) / 2 )
        tmp_point.y = int((self.y + point_2.y) / 2 )
        return tmp_point
    def isEqual(self, point = None):
        if None == point:
            print "No point given to Point.isEqual()"
        else:
            if self.x == point.x and self.y == point.y:
                return True
            else:
                return False
