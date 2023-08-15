##!/usr/bin/env python3
# Author: Björn Seipel
# License: MIT
# Tested with fpdf 2.7.5, Pillow 9.1.0, Python 3.8.10

from fpdf import FPDF

class PDFMark(FPDF):

    _watermark_data=[]
    _stamp_data=[]

    def watermark(self, text, x=None, y=None, angle=45, alpha=1, text_color=[200,200,200], font='Helvetica', font_size=50, font_style=''):        
        self._watermark_data = [text, x, y, angle, alpha, text_color, font, font_size, font_style]

    def stamp(self, text, x=None, y=None, angle=45, alpha=1, text_color=[255,0,0], font='Helvetica', font_size=50, font_style=''):
        self._stamp_data     = [text, x, y, angle, alpha, text_color, font, font_size, font_style]
    
    def _mark(self, text_data):
       
        if len(text_data)!=0 and len(text_data[0])!=0:
            
            with pdf.local_context(fill_opacity=text_data[4], text_color=text_data[5], font_family=text_data[6],font_style=text_data[8], font_size=text_data[7]):                
                text=text_data[0]
                stringWidth=self.get_string_width(text)/2
                x, y=text_data[1], text_data[2] 
                
                if x==None:
                    x=self.w/2-stringWidth
                if y==None:
                    y=self.h/2
                
                #rotate and print text
                with self.rotation(text_data[3], x+stringWidth, y):
                    self.text(x,y, text)                             
            
    def header(self): 
        super().header()
        self._mark(self._watermark_data)

    def footer(self):
        super().footer()
        self._mark(self._stamp_data)
