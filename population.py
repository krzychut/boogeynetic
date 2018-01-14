#___population.py___
import cv2 as cv
import numpy as np
from random import randint
import math as math
from path import *
from point import *
from settings import*
import copy

class population:
    def __init__(self, _pop_count = 0, _n = 0, _height = 0, _width = 0, _start_point = Point(), _end_point = Point(-1, -1)):
        self.paths = [] #Zbior wszystkich sciezek w danej populacji
        self.path_length = _n   #Zadana liczba wierzcholkow lamanej
        for i in range(0, _pop_count):
            self.insert(Path(_n, _height, _width))
        # self.makeStairs()
        if DEBUG:
            pass
            # self.showPopStats()

    def insert(self, _path):    #Wstawia podana sciezke do populacji tak, sciezki byly posortowane od najlepszej do najgorszej. Sciezki wstawiamy TYLKO z uzyciem tej funkcji, inaczej bedzie syf.
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

    def delete(self, _index = -1):  #Usuwa sciezke o podanym indeksie ([] to domyslnie lista, wiec sama sie potem naprawia)
        tmp_path = copy.deepcopy(self.paths.pop(_index))
        # self.path_length = len(self.paths)
        return tmp_path

    def showPopStats(self): #Wyswietla koszty wszystkich sciezek
        i = 0
        for path in self.paths:
            print 'Path', i, 'cost:', path.cost
            i += 1

    def makeStairs(self):
        for i in range(len(self.paths)/4):
            pass
            for j in range(self.path_length):
                pass
