import cv2 as cv
import numpy as np
from random import randint
import math as math
from population import *
from path import *
from point import *
from settings import *


class mainWindow:
    def __init__(self):
        self.heightmap = cv.imread('terrain.png')
        self.tmp_map = self.heightmap.copy()
        self.height, self.width = self.tmp_map.shape[:2]
        self.window_name = 'Evolution'
        self.mWindow = cv.namedWindow(self.window_name, cv.WINDOW_GUI_NORMAL)
        self.maphandle = cv.imshow(self.window_name, self.tmp_map)
        self.key = -1
        esc = 27
        self.path_colour = [0, 0, 255]
        self.path_thickness = 2

    def __init__(self,_map):
        self.heightmap = cv.imread(_map)
        self.tmp_map = self.heightmap.copy()
        self.height, self.width = self.tmp_map.shape[:2]
        self.window_name = 'Evolution'
        self.mWindow = cv.namedWindow(self.window_name, cv.WINDOW_GUI_NORMAL)
        self.maphandle = cv.imshow(self.window_name, self.tmp_map)
        self.key = -1
        esc = 27
        self.path_colour = [0, 0, 255]
        self.path_thickness = 2

    def drawPath(self, path):   #Rysuje podana sciezke na tmp_map, bedziemy tez tego uzywac do maskowania obrazow i wyliczania funkcji kosztu
        cv.line(self.tmp_map, path.start_point.getPoint(), path.getPoint(0), self.path_colour, self.path_thickness)
        for i in range(1, path.length):
            cv.line(self.tmp_map, path.getPoint(i-1), path.getPoint(i), self.path_colour, self.path_thickness)
        cv.line(self.tmp_map, path.end_point.getPoint(), path.getPoint(path.length-1), self.path_colour, self.path_thickness)

    def drawPop(self, _population): #Rysuje podana populacje na tmp_map
        # for i in range(0, len(_population.paths)):
        for path in _population.paths:
            self.drawPath(path)
