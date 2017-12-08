import cv2 as cv
import numpy as np
from random import randint
import math as math
from evolution import *
from population import *
from path import *
from point import *
from main_window import *
from settings import *

if __name__ == '__main__':
    window = mainWindow()
    n = 1
    pop_count = 1000
    evo = evolution(pop_count, n, window.height, window.width)
    evo.selection()
    evo.crossing(evo.pathMean)
    evo.clearRepeatingSpecimens()
    evo.refillPopulation(pop_count)

    while(True):
        window.tmp_map = window.heightmap.copy()
        if(window.key == q_key):
            break
        if window.key == m_key:
            if DEBUG:
                print 'Showing old population'
            window.drawPop(evo.pop)
        elif window.key == n_key:
            if DEBUG:
                print "Showing selected population"
            window.drawPop(evo.pop_selected)
        elif window.key == b_key:
            if DEBUG:
                print 'Showing crossed population'
            window.drawPop(evo.pop_new)
        elif window.key == v_key:
            evo.nextGeneration()
            evo.selection()
            evo.crossing(evo.pathMean)
            evo.clearRepeatingSpecimens()
            evo.adjustPopulation(pop_count)
            # evo.pop_new.showPopStats()
            evo.updateBestSpecimens(evo.pop)
            print "Best Path:", evo.pop_new.paths[0].getPoint()
            print "Worst Path:", evo.pop_new.paths[len(evo.pop_new.paths) - 1].getPoint()
        print "Best Specimen Costs: ", evo.best_specimens[0].cost, evo.best_specimens[1].cost, evo.best_specimens[2].cost
        for spec in evo.best_specimens:
            print "Best specimen:"
            spec.printPath()
        cv.imshow(window.window_name, window.tmp_map)
        window.key = cv.waitKey(0)
    cv.destroyAllWindows()
