#___path.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from point import *
from settings import*
import glob

class Path:
    def __init__(self, n = 0, A = 1, B = 1, _start_point = Point(), _end_point = Point(-1, -1), calcCost = True):
        self.length = n #Ilosc wierzcholkow lamanej (nie liczymy punkto poczatkowego i startowego)
        self.points = [Point(randint(0, B-1), randint(0, A-1)) for _ in range(self.length)]
        if 0 < _end_point.x < B and 0 < _end_point.y < A:
            self.end_point = Point(_end_point.x, _end_point.y)
        else:
            self.end_point = Point(B-1, A-1)
        if 0 < _start_point.x < B and 0 < _start_point.y < A:
            self.start_point(_start_point.x, _start_point.y)
        else:
            self.start_point = Point(0, 0)
        self.cost = 0
        if calcCost:
            self.calcCost()

    def getPoint(self, i = 0):  #Zwraca wspolrzedne wierzcholka jako tuple. Syntax: x, y = path.getPoint(index)
        if i >= self.length:
            return -1, -1
        else:
            x, y = self.points[i].getPoint()
            return x, y

#TODO: Implement variance calculation
    def calcCost(self, terrain = None, display = False):   #Oblicza funkcje kosztu. Dopisze jeszcze liczenie wariancji - Chuti
        #Length
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
        #Variance
        mask = np.zeros(glob.variance_map.shape, dtype = glob.variance_map.dtype)
        if self.length > 0:
            cv.line(mask, self.start_point.getPoint(), self.getPoint(0), 1, glob.rover_radius)
            for i in range(1, self.length):
                cv.line(mask, self.getPoint(i-1), self.getPoint(i), 1, glob.rover_radius)
            cv.line(mask, self.end_point.getPoint(), self.getPoint(self.length-1), 1, glob.rover_radius)
        else:
            cv.line(mask, self.start_point.getPoint(), self.end_point.getPoint(), 1, glob.rover_radius)
        self.cost *= np.sum(cv.multiply(glob.variance_map, mask))
        if display:
            print 'Cost:', np.sum(masked), np.sum(mask), np.sum(glob.variance_map)
            if np.sum(mask) < 20:
                self.printPath()
            cv.imshow("Masked", masked)
            cv.waitKey(16)

    def isEqual(self, path = None): #Zwraca True, jesli sciezki sa identyczne (tzn. identyczne wspolrzedne kolejnych wierzcholkow), w przeciwnym razie False
        if None == path:
            print "No path given to path.isEqual()"
            return False
        else:
            for i in range(0, len(self.points)):
                if not self.points[i].isEqual(path.points[i]):
                    return False
            return True

    def printPath(self):    #Wypisuje kolejne punkty w konsoli
        txt = ''
        txt += "Start: " + str(self.start_point.getPoint()) + "| "
        for i in range(0, len(self.points)):
            txt += "Point " + str(i) + ": " + str(self.points[i].getPoint()) + "| "
        txt += "End: " + str(self.end_point.getPoint())
        print txt
