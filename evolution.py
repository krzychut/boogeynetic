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
#___CONSTRUCTORS___#
    def __init__(self,_exp_beta=3, _top_percent = 1, _pop_count = 0, _n = 0, _height = 0, _width = 0, _start_point = Point(), _end_point = Point(-1, -1)):
        self.pop = population(_pop_count, _n, _height, _width)  #Populacja przed selekcja w danympokoleniu
        self.pop_selected = population(0, _n)   #Populacja po selekcji w danym pokoleniu
        self.pop_new = population(0, _n)    #Populacja po krzyzowaniu, na niej wykonane jest usuwanie duplikatow i wyrownanie rozmiaru populacji
        self.pop_count = _pop_count #Zadana liczebnosc populacji
        self.path_length = _n   #Dlugosc sciezki, podawana bedzie w settings.py, wczytana z pliku txt
        self.height = _height   #Wymiary mapy, zapewnia dopuszczalnosc generowanych rozwiazan
        self.width = _width
        self.exp_beta = _exp_beta   #Wspolczynnik ksztaltu rozkladu wykladniczego do selekcji. Dla 1000 osobnikow dziala calkiem dobrze. Do konfiguraji w settings.py - SKONFIGUROWANO
        self.top_percent = 1    #Tyle procent najlepszych sciezek zawsze przechodzi selekcje, bedzie pewnie zmienna globalna w settings.py
        self.best_specimens = [self.pop.paths[0], self.pop.paths[1], self.pop.paths[2]]

#___PATH CROSSING___#
    def pathMean(self, path_1 = Path(), path_2 = Path()):   #Kazdy i-ty punkt nowej sciezki jest w polowie drogi pomiedzy i-tymi punktami sciezki 1 i 2
        tmp_path = Path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        for i in range(path_1.length):
            tmp_path.points[i] = path_1.points[i].pointMean(path_2.points[i])
        tmp_path.calcCost()
        return tmp_path
    
    def pathHalfChanger(self, path_1 = Path(), path_2 = Path()):   #zamienia polowkami
        k = randint(0,1)
        tmp_path = Path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        
        for i in range(int(k*0.5*path_1.length),int((k+1)*0.5*path_1.length)):
            tmp_path.points[i] = path_1.points[i].pointMean(path_2.points[i])

        for i in range(int((1-k)*0.5*path_1.length),int((2-k)*0.5*path_1.length)):
            tmp_path.points[i] = path_1.points[i].pointMean(path_2.points[i])
            
        tmp_path.calcCost()
        return tmp_path






#TODO: implement more crossing functions


    def crossing(self, crossing_function):  #Tu jako argument podajemy funkcje krzyzujaca, np. pathMean(), wykonuje jedno krzyzowanie kazdej sciezki z kazda
        self.pop_new = population()
        for i in range(len(self.pop_selected.paths)):
            self.pop_new.insert(self.pop_selected.paths[i])
        for i in range(len(self.pop_selected.paths) - 1):
            for j in range(i+1, len(self.pop_selected.paths)):
                tmp_path = self.pathMean(self.pop_selected.paths[i], self.pop_selected.paths[j])
                self.pop_new.insert(tmp_path)
        if DEBUG:
            print 'Population after crossing:', len(self.pop_new.paths)

#___PATH SELECTION___#
    def selection(self):    #Najpierw wybiera top_percent procent najlepszych sciezek, a potem uzupelnia wedlug rozkladu wykladniczego (najwiecej najlepszych)
        idx = 0
        while len(self.pop_selected.paths) < int(0.5 * math.sqrt(8 * len(self.pop.paths) + 1) + 0.5) \
        and len(self.pop_selected.paths) < len(self.pop.paths) * self.top_percent * 0.01:
            self.pop_selected.insert(self.pop.paths[idx])
            # if DEBUG:
            #     print 'Path', idx, 'added as top percentile.'
            idx += 1
        if DEBUG:
            print idx, 'paths added as top percentile.'
        while len(self.pop_selected.paths) < int(0.5 * math.sqrt(8 * len(self.pop.paths) + 1) + 0.5):
            idx = int(np.random.exponential(self.exp_beta) * 100)
            if idx < self.pop_count:
                self.pop_selected.insert(self.pop.paths[idx])
        if DEBUG:
            print 'Old population: ', self.pop_count,'New Population:', len(self.pop_selected.paths)

#___UTILITY FUNCTIONS___#
    def clearPopulation(self, pop_to_clear = None): #Czysci cala wybrana populacje, w zasadzie niepotrzebne, mozna napisac np.: evo.pop_new = []
        if None == pop_to_clear:
            pass
        else:
            pop_to_clear = []

    def nextGeneration(self):   #Przygotowuje obiekt do nastepnej iteracji algorytmu, tj. stara populacja jest nadpisana przez nowa, pozostale sa czyszczone
        self.pop = copy.deepcopy(self.pop_new)
        self.pop_new.paths = []
        self.pop_selected.paths = []
        self.pop_count = len(self.pop.paths)

    def updateBestSpecimens(self, pop_to_check = None): #Odswieza liste najlepszych osobnikow, najlepiej to robic po usunieciu duplikatow i wyrownaniu populacji pop_new
        if None == pop_to_check:
            print "No population passed to updateBestSpecimens()"
        else:
            for path in pop_to_check.paths: #Przydatna konstrukcja w pythonie, dziala praktycznie z kazda lista. Jesli cos jest postaci X = [x1, x2, x3...], mozna tak robic
                if path.cost < self.best_specimens[0].cost:
                    self.best_specimens[0] = copy.deepcopy(path)
                elif path.cost < self.best_specimens[1].cost:
                    self.best_specimens[1] = copy.deepcopy(path)
                elif path.cost < self.best_specimens[2].cost:
                    self.best_specimens[2] = copy.deepcopy(path)
                else:
                    break

    def clearRepeatingSpecimens(self):  #Czysci duplikaty w pop_new
        i = 0
        deleted = 0
        # tmp_pop = population()
        while(i < len(self.pop_new.paths)-1):
            if self.pop_new.paths[i].isEqual(self.pop_new.paths[i+1]):
                # print "Deleting path", i+1
                # print self.pop_new.paths[i].getPoint(), self.pop_new.paths[i+1].getPoint()
                self.pop_new.delete(i+1)
                deleted += 1
            else:
                i += 1
        if DEBUG:
            print "Path duplicates deleted after crossing:", deleted

    def refillPopulation(self, pop_count = None):   #Uzupelnia populacje pop_new do zadanej liczebnosci. Jesli podasz mniejsza niz obecna, nic nie robi
        if None == pop_count:
            return
        while len(self.pop_new.paths) < pop_count:
            path = Path(self.path_length, self.height, self.width)
            self.pop_new.insert(path)
        self.pop_count = len(self.pop_new.paths)

    def cropPopulation(self, pop_count = None): #Obcina najgrsze osobniki populacji pop_new do zadanej liczebnosci. Jesli podasz wieksza niz obecna, nic nie robi
        if None == pop_count:
            return
        while(len(self.pop_new.paths) > pop_count):
            self.pop_new.delete(len(self.pop_new.paths) - 1)

    def adjustPopulation(self, pop_count = None):   #Wywoluje refill, potem crop, w rezultacie ustala populacje na zadanej ilosci
        if None == pop_count:
            return
        self.refillPopulation(pop_count)
        self.cropPopulation(pop_count)
        if DEBUG:
            print "Adjusted pop_new size to:", len(self.pop_new.paths)
