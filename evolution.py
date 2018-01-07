# -*- coding: cp1250 -*-
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
        self.best_specimens = [self.pop.paths[-1], self.pop.paths[-1], self.pop.paths[-1]]
        self.generation_counter = 0
        self.best_cost_history = [-1, -1, -1]

#___PATH CROSSING___#
    def pathMean(self, path_1 = None, path_2 = None):   #Kazdy i-ty punkt nowej sciezki jest w polowie drogi pomiedzy i-tymi punktami sciezki 1 i 2
        tmp_path = Path(self.path_length, calcCost = False)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        for i in range(path_1.length):
            tmp_path.points[i] = path_1.points[i].pointMean(path_2.points[i])
        tmp_path.calcCost()
        return tmp_path

    def pathHalfChanger(self, path_1 = None, path_2 = None):   #zamienia polowkami
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


    def pathExchange(self, path_1 = None, path_2 = None):
        tmp_path = Path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point

        mincost=1000000000
        tmp_bestPath=Path(self.path_length)
        tmp_bestPath.start_point = path_1.start_point
        tmp_bestPath.end_point = path_1.end_point

        for i in range(1,self.path_length-1):
            for j in range(self.path_length):
                if j < i:
                    tmp_path.points[j]=path_1.points[j]
                else:
                    tmp_path.points[j]=path_2.points[j]
            tmp_path.calcCost()
            if tmp_path.cost < mincost:
                mincost=tmp_path.cost
                tmp_bestPath=tmp_path
        tmp_path=tmp_bestPath
        tmp_path.calcCost()
        return tmp_path

    def pathTwoBetter(self, path_1 = None, path_2 = None):   #Analizuje �ciezk� wybieraj�c lepsze punkty
        tmp_path = Path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        temp_twos_1=Path(0)
        temp_twos_2=Path(0)
        temp_cost=1000000000

        for i in range(path_1.length-1):
            temp_twos_1.start_point=tmp_path.points[i]
            temp_twos_2.start_point=tmp_path.points[i]
            temp_twos_1.end_point=path_1.points[i+1]
            temp_twos_2.end_point=path_2.points[i+1]
            temp_twos_1.calcCost()      #JAK UWZGLEDNIC MAPE?????????????????
            temp_twos_2.calcCost()      #JAK UWZGLEDNIC MAPE?????????????????

            if temp_twos_1.cost < temp_twos_2.cost:
                tmp_path.points[i+1] = path_1.points[i+1]
            else:
                tmp_path.points[i+1] = path_2.points[i+1]

        tmp_path.calcCost()
        return tmp_path
    def pathThreeBetter(self, path_1 = None, path_2 = None):   #Analizuje �ciezk� wybieraj�c lepsze pary punkt�w
        tmp_path = Path(self.path_length)
        tmp_path.start_point = path_1.start_point
        tmp_path.end_point = path_1.end_point
        temp_three_1=Path(1, calcCost = False)
        temp_three_2=Path(1, calcCost = False)
        temp_cost=1000000000
        i = 0
        while i < path_1.length-2:
            temp_three_1.start_point=tmp_path.points[i]
            temp_three_2.start_point=tmp_path.points[i]

            temp_three_1.points[0]=tmp_path.points[i+1] #CZY INDEKS DOBRZE
            temp_three_2.points[0]=tmp_path.points[i+1] #CZY DOBRZE INDEKS


            temp_three_1.end_point=path_1.points[i+2]
            temp_three_2.end_point=path_2.points[i+2]

            temp_three_1.calcCost()      #JAK UWZGLEDNIC MAPE?????????????????
            temp_three_2.calcCost()      #JAK UWZGLEDNIC MAPE?????????????????

            if temp_three_1.cost < temp_three_2.cost:
                tmp_path.points[i+1] = path_1.points[i+1]
                tmp_path.points[i+2] = path_1.points[i+2]

            else:
                tmp_path.points[i+1] = path_2.points[i+1]
                tmp_path.points[i+2] = path_2.points[i+2]

            i=i+2

        tmp_path.calcCost()
        return tmp_path





#TODO: implement more crossing functions
    def list2dict(self, crossingF_list): #konwersja listy w dictionary
        self.crossingF_dict={}
        for i in range(len(crossingF_list)):
            if crossingF_list[i] == 'pathMean':
                self.crossingF_dict[i] = self.pathMean
            if crossingF_list[i] == 'pathHalfChanger':
                self.crossingF_dict[i] = self.pathHalfChanger
            if crossingF_list[i] == 'pathTwoBetter':
                self.crossingF_dict[i] = self.pathTwoBetter
            if crossingF_list[i] == 'pathThreeBetter':
                self.crossingF_dict[i] = self.pathThreeBetter
            if crossingF_list[i] == 'pathExchange':
                self.crossingF_dict[i] = self.pathExchange


    def crossing(self):  #tu krzyzuje randomowym operatorem z podanych w data.txt patrz list2dict
        self.pop_new = population()
        rndindx=randint(0, len(self.crossingF_dict)-1) #wybiera randomowo jeden ze wskazanych operatorów
        print self.crossingF_dict[rndindx]
        for i in range(len(self.pop_selected.paths)):
            self.pop_new.insert(self.pop_selected.paths[i])
        for i in range(len(self.pop_selected.paths) - 1):
            for j in range(i+1, len(self.pop_selected.paths)):
                tmp_path = self.crossingF_dict[rndindx](self.pop_selected.paths[i], self.pop_selected.paths[j])
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
        self.generation_counter += 1
        self.best_cost_history[1:] = self.best_cost_history[0:2]
        self.best_cost_history[0] = self.best_specimens[0].cost

    def updateBestSpecimens(self, pop_to_check = None): #Odswieza liste najlepszych osobnikow, najlepiej to robic po usunieciu duplikatow i wyrownaniu populacji pop_new
        if None == pop_to_check:
            print "No population passed to updateBestSpecimens()"
        else:
            for path in pop_to_check.paths: #Przydatna konstrukcja w pythonie, dziala praktycznie z kazda lista. Jesli cos jest postaci X = [x1, x2, x3...], mozna tak robic
                if path.cost < self.best_specimens[0].cost:
                    self.best_specimens[0] = copy.deepcopy(path)
                elif path.cost < self.best_specimens[1].cost and path.cost != self.best_specimens[0].cost:
                    self.best_specimens[1] = copy.deepcopy(path)
                elif path.cost < self.best_specimens[2].cost and path.cost != self.best_specimens[1].cost and path.cost != self.best_specimens[0].cost:
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
