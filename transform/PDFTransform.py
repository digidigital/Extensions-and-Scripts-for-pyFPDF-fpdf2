#!/usr/bin/python3
# Ported from PHP to Python / pyFPDF2 in 2021 by Björn Seipel
# License: MIT
# ***Transform Script***
# Original Authors: Moritz Wagner & Andreas Würmser
# License: FPDF 
# http:#fpdf.org/en/script/script79.php
# ***Circular Text***
# Original Author: Andreas Würmser
# License: FPDF 
# http://fpdf.org/en/script/script82.php

from fpdf import FPDF
from math import pi, tan, sin, cos, radians
class PDFTransform (FPDF):

    def start_transform(self):
        #save the current graphic state
        self._out('q')
    
    def scale_x(self, s_x, x='', y=''):
        self.scale(s_x, 100, x, y)
    
    def scale_y(self, s_y, x='', y=''):
        self.scale(100, s_y, x, y)
    
    def scale_xy(self, s, x='', y=''):
        self.scale(s, s, x, y)
    
    def scale(self, s_x, s_y, x='', y=''):
        if(x == ''): x=self.x
        if(y == ''): y=self.y
        if(s_x == 0 or s_y == 0):
            raise ValueError(
                'Please use values unequal to zero for Scaling'
            )
        y=(self.h-y)*self.k
        x*=self.k
        #calculate elements of transformation matrix
        s_x/=100
        s_y/=100
        tm = [s_x, 0, 0, s_y, x*(1-s_x), y*(1-s_y)]

        #scale the coordinate system
        self.transform(tm)
    
    def mirror_h(self, x=''):
        self.scale(-100, 100, x)
    
    def mirror_v(self, y=''):
        self.scale(100, -100, '', y)
    
    def mirror_p(self, x='',y=''):
        self.scale(-100, -100, x, y)
    
    def mirror_l(self, angle=0, x='',y=''):
        self.scale(-100, 100, x, y)
        self.t_rotate(-2*(angle-90),x,y)
    
    def translate_x(self, t_x):
        self.translate(t_x, 0)
    
    def translate_y(self, t_y):
        self.translate(0, t_y)

    def translate(self, t_x, t_y):
        #calculate elements of transformation matrix
        tm = [1,0,0,1,t_x*self.k,-t_y*self.k]
        #translate the coordinate system
        self.transform(tm)
    
    def t_rotate(self, angle, x='', y=''):
        if(x == ''): x=self.x
        if(y == ''): y=self.y
        y=(self.h-y)*self.k
        x*=self.k
        #calculate elements of transformation matrix
        tm = []
        tm.append(cos(radians(angle)))
        tm.append(sin(radians(angle)))
        tm.append(-tm[1])
        tm.append(tm[0])
        tm.append(x+tm[1]*y-tm[0]*x)
        tm.append(y-tm[0]*y-tm[1]*x)
        #t_rotate the coordinate system around (x,y)
        self.transform(tm)
    
    def skew_x(self, angle_x, x='', y=''):
        self.skew(angle_x, 0, x, y)
    
    def skew_y(self, angle_y, x='', y=''):
        self.skew(0, angle_y, x, y)
    
    def skew(self, angle_x, angle_y, x='', y=''):
        if(x == ''): x=self.x
        if(y == ''): y=self.y
        if(angle_x <= -90 or angle_x >= 90 or angle_y <= -90 or angle_y >= 90):
            raise ValueError(
                'Please use values between -90° and 90° for skewing'
            )
        x*=self.k
        y=(self.h-y)*self.k
        #calculate elements of transformation matrix
        tm = []
        tm.append(1) 
        tm.append(tan(radians(angle_y)))
        tm.append(tan(radians(angle_x)))
        tm.append(1)
        tm.append(-tm[2]*y)
        tm.append(-tm[1]*x)
        #skew the coordinate system
        self.transform(tm)
    
    def transform(self, tm):
        self._out("%.3F %.3F %.3F %.3F %.3F %.3F cm" % (tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]))
    
    def stop_transform(self):
        #restore previous graphic state
        self._out('Q')

    def circular_text(self, x, y, r, text, align='top', kerning=120, fontwidth=100):
    
        kerning/=100
        fontwidth/=100        
        if(kerning==0): 
            raise ValueError(
                'Please use values unequal to zero for kerning'
            )
        if(fontwidth==0): 
            raise ValueError(
                'Please use values unequal to zero for font width'        
            )
        #get width of every letter
        t=0
        #for(i=0 i<strlen(text) i++):
        w=[]
        for i in range(0,len(text)):
            w.append(self.get_string_width(text[i]))
            w[i]*=kerning*fontwidth
            #total width of string
            t+=w[i]
        
        #circumference
        u=(r*2)*pi
        #total width of string in degrees
        d=(t/u)*360
        self.start_transform()
        # rotate matrix for the first letter to center the text
        # (half of total degrees)
        if(align=='top'):
            self.t_rotate(d/2, x, y)
        
        else:
            self.t_rotate(-d/2, x, y)
        
        #run through the string
        #for(i=0 i<strlen(text) i++):
        for i in range(0,len(text)):    
            if(align=='top'):
                #rotate matrix half of the width of current letter + half of the width of preceding letter
                if(i==0):
                    self.t_rotate(-((w[i]/2)/u)*360, x, y)
                
                else:
                    self.t_rotate(-((w[i]/2+w[i-1]/2)/u)*360, x, y)
                
                if(fontwidth!=1):
                    self.start_transform()
                    self.scale_X(fontwidth*100, x, y)
                
                self.set_xy(x-w[i]/2, y-r)
            
            else:
                #rotate matrix half of the width of current letter + half of the width of preceding letter
                if(i==0):
                    self.t_rotate(((w[i]/2)/u)*360, x, y)
                
                else:
                    self.t_rotate(((w[i]/2+w[i-1]/2)/u)*360, x, y)
                
                if(fontwidth!=1):
                    self.start_transform()
                    self.scale_X(fontwidth*100, x, y)
                
                self.set_xy(x-w[i]/2, y+r-(self.font_size))
            
            self.cell(w[i],self.font_size,text[i],0,0,'C') 
            if(fontwidth!=1):
                 self.stop_transform()
                   
        self.stop_transform()
