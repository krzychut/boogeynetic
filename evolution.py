import copy
import cv2 as cv
import numpy as np
from random import randint
import math as math
from population import *
from path import *
from point import *
from settings import*

class evolution:
    def __init__(self, _pop_count = 0, _n = 0, _height = 0, _width = 0):
        self.pop = population(_pop_count, _n, _height, _width)
        self.pop_new = population()
        self.pop_count = _pop_count
        self.exp_beta = 3
        self.top_percent = 1
        self.path_length = _n
        self.best_specimens = [self.pop.paths[0], self.pop.paths[1], self.pop.paths[2]]

    def pathMean(self, path_1 = path(), path_2 = path()):
        tmp_path = path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        for i in range(path_1.length):
            tmp_path.points[i] = path_1.points[i].pointMean(path_2.points[i])
        return tmp_path

    def selection(self):
        idx = 0
        while len(self.pop_new.paths) < int(0.5 * math.sqrt(8 * len(self.pop.paths) + 1) + 0.5) \
        and len(self.pop_new.paths) < len(self.pop.paths) * self.top_percent * 0.01:
            self.pop_new.insert(self.pop.paths[idx])
            if DEBUG:
                print 'Path', idx, 'added as top percentile.'
            idx += 1

        if DEBUG:
            print idx, 'paths added as top percentile.'

        while len(self.pop_new.paths) < int(0.5 * math.sqrt(8 * len(self.pop.paths) + 1) + 0.5):
            idx = int(np.random.exponential(self.exp_beta) * 100)
            if idx < self.pop_count:
                self.pop_new.insert(self.pop.paths[idx])
        if DEBUG:
            print 'Old population: ', self.pop_count,'New Population:', len(self.pop_new.paths)

    def crossing(self):
        tmp_pop = population()
        for i in range(len(self.pop_new.paths)):
            tmp_pop.insert(self.pop_new.paths[i])
        for i in range(len(self.pop_new.paths) - 1):
            for j in range(i+1, len(self.pop_new.paths)):
                tmp_path = self.pathMean(self.pop_new.paths[i], self.pop_new.paths[j])
                tmp_pop.insert(tmp_path)
        if DEBUG:
            print 'Population after crossing:', len(tmp_pop.paths)
        return tmp_pop

    def clearPopulation(self):
        pass
