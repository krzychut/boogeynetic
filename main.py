# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
from random import randint
import math as math
import sys
from evolution import *
from population import *
from path import *
from point import *
from main_window import *
from settings import *

if __name__ == '__main__':
    param = Parameters('data.txt')  #zawiera podstawowe parametry (opisana w settings)
    if 1 < len(sys.argv):
        try:
            print "argv length:", len(sys.argv)
            print "argv[0]:", sys.argv[1]
            param.SetPack(int(str(sys.argv[1])))
        except ValueError:
            print "Argument passed must be an integer. Using default parameter set: 1"
            param.SetPack(1)
    else:
        print "No argument passed. Using default parameter set: 1"
        param.SetPack(1)

    window = mainWindow(param.map)   #Zawiera mape (3 kanaly, na razie wykorzystany 1, zajme sie jeszcze terenem i mapa kosztow - Chuti)
    n = param.n   #Liczba wierzcholkow lamanej
    pop_count = param.pop_count    #Liczba populacji
    # exp_beta=param.beta#beta rozk�adu wykladniczego
    evo = evolution(
    _exp_beta = param.beta,
    _top_percent = param.top_percent,
    _pop_count = param.pop_count,
    _n = param.n,
    _height = window.height,
    _width = window.width)  #To zawiera populacje stara, populacje po selekcji i populacje po krzyzowaniu + funkcje do tego
    evo.selection() #Tu selekcja wedlug rozkladu wykladniczego
    evo.crossing(evo.pathMean)  #Tu krzyzowanie. Jako parametr przyjmuje funkcje krzyzujaca, trzeba wiecej takich napisac
    evo.clearRepeatingSpecimens()   #Usuwa powtorzenia z populacji po krzyzowaniu
    evo.adjustPopulation(pop_count) #Dodaje losowe sciezki albo usuwa najgorsze z nowej populacji, zeby bylo ich tyle co przed selekcja
    evo.updateBestSpecimens(evo.pop_new)

    while(True):
        window.tmp_map = window.heightmap.copy()
        if(window.key == q_key):
            break
        if window.key == m_key:
            if DEBUG:
                print 'Showing old population'
            window.drawPop(evo.pop) #drawPop - Rysuje wybrana populacje na tmp_map, czyli tymczasowej kopii mapy, potrzebnej tylko do wyswietlania sciezek
        elif window.key == n_key:
            if DEBUG:
                print "Showing selected population"
            window.drawPop(evo.pop_selected)
        elif window.key == b_key:
            if DEBUG:
                print 'Showing crossed population'
            window.drawPop(evo.pop_new)
        elif window.key == v_key:
            evo.nextGeneration()    #Stara populacja jest nadpisana przez nowa, pozostale populacje sa czyszczone
            evo.selection()
            evo.crossing(evo.pathMean)
            evo.clearRepeatingSpecimens()
            evo.adjustPopulation(pop_count)
            # evo.pop_new.showPopStats()
            evo.updateBestSpecimens(evo.pop_new)    #Odswieza liste trzech najlepszych rozwiazan
            print "Best Path:", evo.pop_new.paths[0].printPath()    #printPath() Wypisuje kolejne punkty sciezki, tylko do debuggingu
            print "Worst Path:", evo.pop_new.paths[len(evo.pop_new.paths) - 1].printPath()
        print "Best Specimen Costs: ", evo.best_specimens[0].cost, evo.best_specimens[1].cost, evo.best_specimens[2].cost
        for spec in evo.best_specimens:
            print "Best specimen:"
            spec.printPath()
        cv.imshow(window.window_name, window.tmp_map) #Tutaj odswiezany jest wyswietlany obrazek, tzn. tmp_map z naniesionymi sciezkami pojawia sie na ekranie
        window.key = cv.waitKey(0) #To musi byc po kazdym imshow(), czeka na input z klawiatury. Parametr to czas czekania, 0 oznacza nieskonczonosc

    cv.destroyAllWindows()  #Po zakonczeniu programu (klawisz 'q') zamyka okienka zeby nie bylo segfaultow
