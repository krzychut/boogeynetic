# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
from random import randint
import math as math
import sys
from evolution import evolution
from population import population
from path import Path
from main_window import *
from settings import *
import glob
import time
import csv

if __name__ == '__main__':
#___READING PARAMETERS___#
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

#___DATA INITIALIZATION___#
    window = mainWindow(param.map)   #Zawiera mape (3 kanaly, na razie wykorzystany 1, zajme sie jeszcze terenem i mapa kosztow - Chuti)
    # glob.variance_map = window.heightmap[:,:,1]

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
    evo.list2dict(param.parameters_list)  #tu zmienia liste operatorów krzyzowania na dictionary

    csv_file=open("output_data.csv",'wb')# Plik w ktorym beda dane z testu
    wr=csv.writer(csv_file)     #PROSTY ZAPIS DO PLIKU CSV
    wr.writerow(["_exp_beta","_top_percent","pop_count","_n","_height","_width"])
    wr.writerow([param.beta,param.top_percent,param.pop_count,param.n,window.height,window.width])
    wr.writerow(["Generation","Best Specimen 0","Best Specimen 1","Best Specimen 2", "Gen Time"])

    gen_time_elapsed = time.time()
    evo.selection() #Tu selekcja wedlug rozkladu wykladniczego
    evo.crossing()  #Tu krzyzowanie. operatory dobiera na podstawie crossingF_dict z list2dict
    evo.clearRepeatingSpecimens()   #Usuwa powtorzenia z populacji po krzyzowaniu
    evo.adjustPopulation(pop_count) #Dodaje losowe sciezki albo usuwa najgorsze z nowej populacji, zeby bylo ich tyle co przed selekcja
    evo.updateBestSpecimens(evo.pop_new)
    gen_time_elapsed = time.time() - gen_time_elapsed

#___MAIN LOOP___#
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
            gen_time_elapsed = time.time()
            # evo.nextGeneration()    #Stara populacja jest nadpisana przez nowa, pozostale populacje sa czyszczone
            # evo.selection()
            # evo.crossing()   # korzysta z crossingF_dict utworzonego w list2dict
            # evo.clearRepeatingSpecimens()
            # evo.adjustPopulation(pop_count)
            # evo.updateBestSpecimens(evo.pop_new)    #Odswieza liste trzech najlepszych rozwiazan
            evo.evoSpin(mutation = True)
            gen_time_elapsed = time.time() - gen_time_elapsed
            # print "Best Path:", evo.pop_new.paths[0].printPath()    #printPath() Wypisuje kolejne punkty sciezki, tylko do debuggingu
            # print "Worst Path:", evo.pop_new.paths[-1].printPath()
        print "Best Specimen Costs: ", evo.best_specimens[0].cost, evo.best_specimens[1].cost, evo.best_specimens[2].cost
        # for spec in evo.best_specimens:
        #     print "Best specimen:"
        #     spec.printPath()
        for path in evo.best_specimens:
            window.drawPath(path, [0, 255, 0])
        print 'Generation:', evo.generation_counter, ' | Elapsed time:', gen_time_elapsed, 'seconds'
        print 'Best cost history:', evo.best_cost_history, '\n========================================================='
        l=[evo.generation_counter, evo.best_specimens[0].cost, evo.best_specimens[1].cost, evo.best_specimens[2].cost,
        gen_time_elapsed]# ELEMENTY DO ZAPISU DO PLIKU
        wr.writerow(l)
        cv.imshow(window.window_name, window.tmp_map) #Tutaj odswiezany jest wyswietlany obrazek, tzn. tmp_map z naniesionymi sciezkami pojawia sie na ekranie
        if window.key == v_key:
            key = cv.waitKey(1) #To musi byc po kazdym imshow(), czeka na input z klawiatury. Parametr to czas czekania, 0 oznacza nieskonczonosc
            if key in [q_key, m_key, n_key, b_key, v_key]:
                window.key = key
        else:
            window.key = cv.waitKey(0)
    csv_file.close()
    cv.destroyAllWindows()  #Po zakonczeniu programu (klawisz 'q') zamyka okienka zeby nie bylo segfaultow
