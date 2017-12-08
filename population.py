#___population.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from path import *
from point import *
from settings import*

class population:
    def __init__(self, _pop_count = 0, _n = 0, _height = 0, _width = 0, _start_point = Point(), _end_point = Point(-1, -1)):
        self.paths = []
        self.path_length = _n
        #self.paths = [Path(_n, _height, _width) for _ in range(_pop_count)]
        for i in range(0, _pop_count):
            self.insert(Path(_n, _height, _width))
        if DEBUG:
            self.showPopStats()

    def insert(self, _path):
        if len(self.paths) == 0:
            self.paths.append(_path)
        else:
            for i in range(0, len(self.paths)):
                if self.paths[i].cost > _path.cost:
                    self.paths.insert(i, _path)
                    return
                else:
                    pass
            self.paths.append(_path)
        # self.path_length = len(self.paths)

    def delete(self, _index = -1):
        tmp_path = self.paths.pop(_index)
        # self.path_length = len(self.paths)
        return tmp_path

    def showPopStats(self):
        i = 0
        for path in self.paths:
            print 'Path', i, 'cost:', path.cost
            i += 1
