#___population.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from path import *
from point import *
from settings import*

class population:
    def __init__(self, _pop_count = 0, _n = 0, _height = 0, _width = 0):
        self.paths = []
        self.path_length = _n
        #self.paths = [path(_n, _height, _width) for _ in range(_pop_count)]
        for i in range(0, _pop_count):
            self.insert(path(_n, _height, _width))
        if DEBUG:
            for i in range(0, _pop_count):
                print 'Path', i, 'cost:', self.paths[i].cost
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
    def delete(self, _index = -1):
        return self.paths.pop(_index)
