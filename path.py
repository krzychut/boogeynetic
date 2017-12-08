#___path.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from point import *
from settings import*

class Path:
    def __init__(self, n = 0, A = 1, B = 1, _start_point = Point(), _end_point = Point(-1, -1)):
        self.length = n
        self.points = [Point(randint(0, A-1), randint(0, B-1)) for _ in range(self.length)]
        if 0 < _end_point.x < A and 0 < _end_point.y < B:
            self.end_point = Point(_end_point.x, _end_point.y)
        else:
            self.end_point = Point(A-1, B-1)
        if 0 < _start_point.x < A and 0 < _start_point.y < B:
            self.start_point(_start_point.x, _start_point.y)
        else:
            self.start_point = Point(0, 0)
        self.cost = 0
        self.calcCost()

    def getPoint(self, i = 0):
        if i >= self.length:
            return -1, -1
        else:
            x, y = self.points[i].getPoint()
            return x, y

#TODO: Implement variance calculation
    def calcCost(self, height_map = None,terrain_map = None):
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

    def isEqual(self, path = None):
        if None == path:
            print "No path given to path.isEqual()"
            return False
        else:
            for i in range(0, len(self.points)):
                if not self.points[i].isEqual(path.points[i]):
                    return False
            return True

    def printPath(self):
        txt = ''
        txt += "Start: " + str(self.start_point.getPoint()) + "| "
        for i in range(0, len(self.points)):
            txt += "Point " + str(i) + ": " + str(self.points[i].getPoint()) + "| "
        txt += "End: " + str(self.end_point.getPoint())
        print txt
