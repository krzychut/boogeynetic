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
    n = 5
    pop_count = 1000
    evo = evolution(pop_count, n, window.height, window.width)
    evo.selection()
    tmp_pop = evo.crossing()

    while(True):
        window.tmp_map = window.heightmap.copy()
        if window.key == m_key:
            if DEBUG:
                print 'Showing old population'
            window.drawPop(evo.pop)
        elif window.key == n_key:
            if DEBUG:
                print "Showing new population"
            window.drawPop(evo.pop_new)
        elif window.key == b_key:
            if DEBUG:
                print 'Showing crossed population'
            window.drawPop(tmp_pop)
        cv.imshow(window.window_name, window.tmp_map)
        window.key = cv.waitKey(0)
        if(window.key == esc):
            break
    cv.destroyAllWindows()
