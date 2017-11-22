#___path.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from point import *
from settings import*

class path:
    def __init__(self, n = 0, A = 1, B = 1, _start_point = point(), _end_point = point(-1, -1)):
        self.length = n
        self.points = [point(randint(0, A-1), randint(0, B-1)) for _ in range(self.length)]
        if 0 < _end_point.x < A or 0 < _end_point.y < B:
            self.end_point = point(_end_point.x, _end_point.y)
        else:
            self.end_point = point(A-1, B-1)
        if 0 < _start_point.x < A or 0 < _start_point.y < B:
            self.start_point(_start_point.x, _start_point.y)
        else:
            self.start_point = point(0, 0)
        self.cost = 0
        self.calcCost()

    def getPoint(self, i):
        if i >= self.length:
            return -1, -1
        else:
            x, y = self.points[i].getPoint()
            return x, y
    def calcCost(self):
        if self.length > 0:
            self.cost += math.sqrt(pow(self.points[0].x - self.start_point.x, 2) +\
            pow(self.points[0].y - self.start_point.y, 2))
            for i in range(1, len(self.points)):
                self.cost += math.sqrt(pow(self.points[i].x-self.points[i-1].x, 2) +\
                pow(self.points[i].y-self.points[i-1].y, 2))
            self.cost += math.sqrt(pow(self.points[len(self.points)-1].x - self.end_point.x, 2) +\
            pow(self.points[len(self.points)-1].y - self.end_point.y, 2))
        else:
            self.cost += math.sqrt(pow(self.end_point.x - self.start_point.x, 2) +\
            pow(self.end_point.y - self.start_point.y, 2))
