#!/usr/bin/env python3
# Ported from PHP to Python / pyFPDF2 in 2021 by Björn Seipel
# Original Author: Martin Hall-May
# License: FPDF 
# http://www.fpdf.org/en/script/script74.php

from AlphaFPDF import AlphaFPDF

class PDFMark(AlphaFPDF):

    _watermark_data=[]
    _stamp_data=[]

    def watermark(self, text, x=None, y=None, angle=45, alpha=1, text_color=[200,200,200], font='Helvetica', font_size=50, font_style=''):        
        self._watermark_data = [text, x, y, angle, alpha, text_color, font, font_size, font_style]

    def stamp(self, text, x=None, y=None, angle=45, alpha=1, text_color=[255,0,0], font='Helvetica', font_size=50, font_style=''):
        self._stamp_data     = [text, x, y, angle, alpha, text_color, font, font_size, font_style]
    
    def _mark(self, text_data):
        if len(text_data)!=0:
            #store current x, y coordinates
            old_X, old_y = self.get_x(), self.get_y()
            
            self.set_font(text_data[6], text_data[8] , text_data[7])
            r,g,b = text_data[5]
            self.set_text_color(r, g, b)
            self.set_alpha(text_data[4])
            
            text=text_data[0]
            stringWidth=self.get_string_width(text)/2
            x, y =text_data[1], text_data[2] 
            
            if x==None:
                x=self.w/2-stringWidth
            if y==None:
                y=self.h/2
            
            #rotate and print text
            with self.rotation(text_data[3], x+stringWidth, y):
                self.text(x,y, text)                                 
            
            #set alpha back to opaque
            self.set_alpha(1)
            #store old coordinates
            self.set_xy(old_X,old_y)
            

    def header(self):
        try: 
            super().header()
        except:
            pass
        self._mark(self._watermark_data)

    def footer(self):
        try: 
            super().footer()
        except:
            pass
        self._mark(self._stamp_data)





