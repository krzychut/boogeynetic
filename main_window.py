import cv2 as cv
import numpy as np
from random import randint
import math as math
from population import *
from path import *
from point import *
from settings import *
import time

                         
class mainWindow:

    def __init__(self,_map='terrain.png', _rover_radius = 5):
        self.heightmap = cv.imread(_map)
        self.height, self.width = self.heightmap.shape[:2]
        self.tmp_map = self.heightmap.copy()
        self.heightmap[:,:,1] = 0
        self.heightmap[:,:,2] = 1
        self.calcVariance(_rover_radius)
        self.window_name = 'Evolution'
        self.mWindow = cv.namedWindow(self.window_name)
        self.maphandle = cv.imshow(self.window_name, self.tmp_map)
        self.key = -1
        esc = 27
        self.path_colour = [0, 0, 255]
        self.path_thickness = 2

    def drawPath(self, path, colour = None):   #Rysuje podana sciezke na tmp_map, bedziemy tez tego uzywac do maskowania obrazow i wyliczania funkcji kosztu
        if None == colour:
            colour = self.path_colour
        if path.length > 0:
            cv.line(self.tmp_map, path.start_point.getPoint(), path.getPoint(0), colour, self.path_thickness)
            for i in range(1, path.length):
                cv.line(self.tmp_map, path.getPoint(i-1), path.getPoint(i), colour, self.path_thickness)
            cv.line(self.tmp_map, path.end_point.getPoint(), path.getPoint(path.length-1), colour, self.path_thickness)
        else:
            cv.line(self.tmp_map, path.start_point.getPoint(), path.end_point.getPoint(), colour, self.path_thickness)

    def drawPop(self, _population): #Rysuje podana populacje na tmp_map
        # for i in range(0, len(_population.paths)):
        for path in _population.paths:
            self.drawPath(path)

    def calcVariance(self, radius = 5):
        var_window = cv.namedWindow("Variance")
        b, g, r = cv.split(self.heightmap)
        # mask_img = np.zeros(self.heightmap.shape[:2], np.uint8)
        for i in range(0, self.height):
            loop1 = time.time()
            for j in range(0, self.width):
                y1, x1 = np.ogrid[max(0, i-radius):min(self.height-1, i+radius), max(0, j-radius):min(self.width-1, j+radius)]
                mask1 = (x1-j)*(x1-j) + (y1-i)*(y1-i) < radius*radius
                mask_img = np.zeros((len(y1), len(x1[0])), np.uint8)
                mask_img[mask1] = 1
                tmp = b[y1, x1]
                mean, stddev = cv.meanStdDev(src = tmp, mask = mask_img)
                self.heightmap[i, j, 1] = stddev
            cv.imshow("Variance", self.heightmap[:,:,1])
            cv.waitKey(1)
