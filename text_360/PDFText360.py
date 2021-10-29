#!/usr/bin/python3
# Ported from PHP to Python (and extended) by Björn Seipel in 2021
# License: MIT
# Original Author: CIX88
# License: „[…]Alle dargestellten Quelltexte sind frei verfügbar.[…]“ -> "[...]All source code presented is freely available.[...]"
# http://www.cix88.de/cix_pdf/pdf_fpdf_allgemein/cix_tut_042.php

from fpdf import FPDF, util
from math import pi, cos, sin

class PDFText360(FPDF):

    def _circle_text_transform(self, x, y, txt, tx = 0, fy = 0, tw = 0, fw = 0):

        fw += 90 + float(tw)
        tw *= pi/180
        fw *= pi/180

        if tx == '': tx = cos(float(tw))
        ty = sin(float(tw))
        fx = cos(float(fw))
        if fy == '': fy = sin(float(fw))

        s = 'BT %.2f %.2f %.2f %.2f %.2f %.2f Tm (%s) Tj ET' % (
            tx,
            ty,
            fx,
            fy,
            x * self.k,
            (self.h-y) * self.k,
            util.escape_parens(txt)
            )
        s = 'q ' + self.text_color + ' ' + s + ' Q'      
            
        self._out(s)

    def text_360(self, x = None , y = None, text = None, width = None):

        # set x, y to center of page if not set        
        if x==None:
            x=self.w/2
        if y==None:
            y=self.h/2

        if text==None: 
            return

        print (len(text))        
        for non_printable in ('\n', '\t', '\r'):    
            text=text.replace(non_printable,'')
        print (len(text))

        if len(text)==0:
            return

        # set width to 1/2 width of text if not set
        if width==None:
            width=self.get_string_width(text)/2

        value_degrees = 360 / len(text)

        cc = 1
        buffer = 1
        for temp in text:
            cc+=1
            st_x = cos( ( buffer * pi ) / 180 )
            st_target_x = x + ( -st_x * width / 2 )
            st_y = sin( ( buffer * pi ) / 180 )
            st_target_y = y + ( -st_y * width / 2 )

            self._circle_text_transform( st_target_x, st_target_y, temp, '', '', 90-buffer)
            buffer += value_degrees
       
        if self.underline and text!='': 
            # store line width
            line_width=self.line_width

            draw_color=self.text_color.upper()
            self._out(draw_color)

            lw=self.current_font["ut"]/1000*self.font_size_pt
            self.set_line_width(lw/2)
            
            # draw circle
            circle_x=x-width/2+lw
            circle_y=y-width/2+lw
            circle_w=width-2*lw
            self.ellipse(circle_x, circle_y, circle_w, circle_w, style="D")
           
            # restore previous values
            self.set_line_width(line_width)
            self._out(self.draw_color)



