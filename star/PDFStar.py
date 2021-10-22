#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Luciano Salvino
# License: FPDF
# http://www.fpdf.org/en/script/script71.php

from fpdf import FPDF
from math import pi, sin, cos

class PDFStar(FPDF):

    def star(self, x, y, rin, rout, points, style='D'):

        if style== 'F':
            op = 'f'
        elif style=='FD' or style=='DF':
            op = 'B'
        else:
            op = 'S'
        dth = pi/points
        th = 0
        k = self.k
        h = self.h
        points_string = ''
        for i in range (0,(points*2)+1): 
        
            th += dth
            cx = x + (rin if i%2==0 else rout) * cos(th)
            cy = y + (rin if i%2==0 else rout) * sin(th)
            points_string += '%.2F %.2F' % (cx*k, (h-cy)*k)
            if(i==0):
                points_string += ' m '
            else:
                points_string += ' l '
        
        self._out(points_string + op)