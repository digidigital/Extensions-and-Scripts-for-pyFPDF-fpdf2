#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Pivkin Vladimir
# License: FPDF
# http://www.fpdf.org/en/script/script31.php
#
# Only Bold and Italics are available as style.
# Underline is not supported since underline is not a 
# property of a font. Instead FPDF draws a line.

from fpdf import FPDF, util 
from math import pi, cos, sin

class PDFTextR(FPDF):

    def text_with_direction(self, x, y, txt, direction='R'):

        if direction=='R':
            s='BT %.2F %.2F %.2F %.2F %.2F %.2F Tm (%s) Tj ET' % (1,0,0,1,x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        elif direction=='L':
            s='BT %.2F %.2F %.2F %.2F %.2F %.2F Tm (%s) Tj ET' % (-1,0,0,-1,x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        elif direction=='U':
            s='BT %.2F %.2F %.2F %.2F %.2F %.2F Tm (%s) Tj ET' % (0,1,-1,0,x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        elif direction=='D':
            s='BT %.2F %.2F %.2F %.2F %.2F %.2F Tm (%s) Tj ET' % (0,-1,1,0,x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        else:
            s='BT %.2F %.2F Td (%s) Tj ET' % (x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        if self.fill_color != self.text_color:
            s = f"q {self.text_color} {s} Q"
        self._out(s)


    def text_with_rotation(self, x, y, txt, txt_angle, font_angle=0):

        font_angle+=90+txt_angle
        txt_angle*=pi/180
        font_angle*=pi/180

        txt_dx=cos(txt_angle)
        txt_dy=sin(txt_angle)
        font_dx=cos(font_angle)
        font_dy=sin(font_angle)

        s='BT %.2F %.2F %.2F %.2F %.2F %.2F Tm (%s) Tj ET' % (txt_dx,txt_dy,font_dx,font_dy,x*self.k,(self.h-y)*self.k,util.escape_parens(txt))
        if self.fill_color != self.text_color:
            s = f"q {self.text_color} {s} Q"
        self._out(s)