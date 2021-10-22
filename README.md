# Extensions / Scripts for pyFPDF (fpdf2)

This repository provides you with [FPDF Scripts](http://fpdf.org/en/script/) ported from PHP to Python.

**Scripts**
* [Alpha / Transparency](https://github.com/digidigital/Transparency-for-pyFPDF-fpdf2/blob/main/README.md#alpha--transparency-for-pyfpdf-fpdf2) 
* [Transform & Circular Text](https://github.com/digidigital/Transparency-for-pyFPDF-fpdf2/blob/main/README.md#transform--circular-text-for-pyfpdf-fpdf2) 

# Alpha / Transparency for pyFPDF (fpdf2)
This script adds transparency support to pyFPDF. You can set the alpha channel from 0 (fully transparent) to 1 (fully opaque). It applies to all elements (text, drawings, images). 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Usage

Just put AlphaFPDF.py in your project directory

```python
#!/usr/bin/env python3
# Ported from PHP to Python / pyFPDF in 2021 by Björn Seipel
# License: MIT 
# Original Author: Martin Hall-May
# License: FPDF 
# http://www.fpdf.org/en/script/script74.php
from fpdf import FPDF

class AlphaFPDF (FPDF):

    _extgstates = {}

    # alpha: real value from 0 (transparent) to 1 (opaque)
    # bm:    blend mode, one of the following:
    #          Normal, Multiply, Screen, Overlay, Darken, Lighten, ColorDodge, ColorBurn,
    #          HardLight, SoftLight, Difference, Exclusion, Hue, Saturation, Color, Luminosity
    def set_alpha(self, alpha, bm='Normal'):
        if alpha < 0: alpha=0
        if alpha > 1: alpha=1
        # set alpha for stroking (CA) and non-stroking (ca) operations
        gs = self.add_ext_gs_state({'ca':alpha, 'CA':alpha, 'BM':'/' + bm})
        self.set_ext_gs_state(gs)

    def add_ext_gs_state(self, parms):
        n = len(self._extgstates)+1
        self._extgstates[n] = {'parms': parms}
        
        return n
    
    def set_ext_gs_state(self, gs):
        self._out("/GS%d gs" % gs)
    
    def _enddoc(self):
        if len(self._extgstates) > 0 and float(self.pdf_version) < float(1.4):
            self.pdf_version='1.4'
        FPDF._enddoc(self)
    
    def _putextgstates(self):
        for i in range (1, len(self._extgstates)+1):
            self._newobj()
            self._extgstates[i]['n'] = self.n
            self._out('<</Type /ExtGState')
            parms = self._extgstates[i]['parms']
            self._out("/ca %.3F" % parms['ca'])
            self._out("/CA %.3F" % parms['CA'])
            self._out('/BM ' + parms['BM'])
            self._out('>>')
            self._out('endobj')
    
    def _putresourcedict(self):
        FPDF._putresourcedict(self)
        self._out('/ExtGState <<')
        for k, extgstate in zip(self._extgstates.keys(), self._extgstates.values()):
            self._out('/GS' + str(k) + ' ' + str(extgstate['n']) + ' 0 R')
                    
        self._out('>>')
                
    def _putresources(self):
        self._putextgstates()
        FPDF._putresources(self)
```

Import the script and use pyFPDF as usual.

Use `set_alpha(X)` to set the transparency where
X is a value between 0 (transparent) and 1 (opaque)

```python
#!/usr/bin/env python3

from AlphaFPDF import AlphaFPDF as FPDF 

pdf = FPDF()

pdf.add_page()
pdf.set_line_width(1.5)

# draw opaque red square
pdf.set_fill_color(255,0,0)
pdf.rect(10,10,40,40,'DF')

# set alpha to semi-transparency
pdf.set_alpha(0.5)

# draw green square
pdf.set_fill_color(0,255,0)
pdf.rect(20,20,40,40,'DF')

# draw png image
pdf.image('./Image.png',30,30,40)

# restore full opacity
pdf.set_alpha(1)

# print name
pdf.set_font('Helvetica', 'B', 24)
pdf.text(46,68,'On top of Image')

pdf.output("demo.pdf")
```

Gives you:

![Transparent text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Transparency-for-pyFPDF-fpdf2/main/alpha/result.jpg)

The generated PDF is exported as PDF version 1.4. It may not comply with the PDF standard in all respects. 

### This script is the answer for:
* How to create a PDF with transparent text in Python?
* How to add images with alpha/transparency in pyFPDF?
* How to add dynamic transparent overlay / stamps to PDF documents?

# Transform & Circular Text for pyFPDF (fpdf2)

This script adds transfromation featurea ans support for circular text to pyFPDF. 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Usage

Just put PDFTransform.py in your project directory
```python
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
```

Import the script and use pyFPDF with added features as usual.

## Transform features

Performs the following 2D transformations: scaling, mirroring, translation, rotation and skewing.
Use `start_transform()` before, and `stop_transform()` after the transformations to restore the normal behavior.

`start_transform()`

Use this before calling any tranformation.

`scale_x(float s_x [, float x [, float y]])`

`scale_y(float s_y [, float x [, float y]])

`scale_xy(float s [, float x [, float y]])`

`scale(float s_x, float s_y [, float x [, float y]])`

s_x: scaling factor for width as percent. 0 is not allowed.
s_y: scaling factor for height as percent. 0 is not allowed.
s: scaling factor for width and height as percent. 0 is not allowed.
x: abscissa of the scaling center. Default is current x position
y: ordinate of the scaling center. Default is current y position

`mirror_h([float x])`

Alias for scaling -100% in x-direction
x: abscissa of the axis of reflection

`mirror_v([float y])`

Alias for scaling -100% in y-direction
y: ordinate of the axis of reflection

`mirror_p([float x, [float y]])`

Point reflection on point (x, y). (alias for scaling -100 in x- and y-direction)
x: abscissa of the point. Default is current x position
y: ordinate of the point. Default is current y position

`mirror_l([float angle [, float x [, float y]]])`

Reflection against a straight line through point (x, y) with the gradient angle (angle).
angle: gradient angle of the straight line. Default is 0 (horizontal line).
x: abscissa of the point. Default is current x position
y: ordinate of the point. Default is current y position

translate_x(float t_x)
translate_y(float t_y)
translate(float t_x, float t_y)

t_x: movement to the right
t_y: movement to the bottom

`t_rotate(float angle [, float x [, float y]])`

angle: angle in degrees for counter-clockwise rotation
x: abscissa of the rotation center. Default is current x position
y: ordinate of the rotation center. Default is current y position

`skew_x(float angle_x [, float x [, float y]])`

`skew_y(float angle_y [, float x [, float y]])`

`skew(float angle_x, float angle_y [, float x [, float y]])`

angle_x: angle in degrees between -90 (skew to the left) and 90 (skew to the right)
angle_y: angle in degrees between -90 (skew to the bottom) and 90 (skew to the top)
x: abscissa of the skewing center. default is current x position
y: ordinate of the skewing center. default is current y position

`stop_transform()`

Restores the normal painting and placing behavior as it was before calling StartTransform(). 

## Circular Text

Prints a circular text inside a given circle. It makes use of the Transformations features.

`circular_text(float x, float y, float r, string text [, string align [, float kerning [, float fontwidth]]])`

x: abscissa of center

y: ordinate of center

r: radius of circle

text: text to be printed

align: text alignment: top or bottom. Default value: top

kerning: spacing between letters in percentage. Default value: 120. Zero is not allowed.

fontwidth: width of letters in percentage. Default value: 100. Zero is not allowed. 

```python
# !/usr/bin/env python3

from PDFTransform import PDFTransform as FPDF 

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica','B',12)

#Scaling
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(25, 20, 40, 10, 'D')
pdf.text(25, 34, 'pdf.scale_xy(percent, center_x, center_y)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#pdf.scale_xy(150, 25, 30) by 150% centered by (50,30) which is the lower left corner of the rectangle
pdf.scale_xy(150, 25, 30)
pdf.rect(25, 20, 40, 10, 'D')
pdf.text(25, 19, 'pdf.scale_xy(150, 50, 30)')
#Stop Transformation
pdf.stop_transform()

#Translation
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 20, 40, 10, 'D')
pdf.text(125, 19, 'pdf.translate(horizontal, vertical)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#Translate 7 to the right, 5 to the bottom
pdf.translate(7, 5)
pdf.rect(125, 20, 40, 10, 'D')
pdf.text(125, 19, 'pdf.translate(7, 5)')
#Stop Transformation
pdf.stop_transform()

#Rotation
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(25, 50, 40, 10, 'D')
pdf.text(25, 64, 'pdf.t_rotate(degrees, center_x, center_y')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#t_rotate 20 degrees counter-clockwise centered by (50,60) which is the lower left corner of the rectangle
pdf.t_rotate(15, 25, 60)
pdf.rect(25, 50, 40, 10, 'D')
pdf.text(25, 49, 'pdf.t_rotate(20, 50, 60)')
#Stop Transformation
pdf.stop_transform()

#Skewing
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 50, 40, 10, 'D')
pdf.text(125, 64, 'pdf.skew_x(degrees,by_x, by_y)')
pdf.text(125, 69, 'pdf.skew_y(degrees,by_x, by_y)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#skew 30 degrees along the x-axis centered by (125,60) which is the lower left corner of the rectangle
pdf.skew_x(30, 125, 60)
pdf.rect(125, 50, 40, 10, 'D')
pdf.text(125, 49, 'pdf.skew_x(30, 125, 60)')
#Stop Transformation
pdf.stop_transform()

#Mirroring horizontally
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(50, 80, 40, 10, 'D')
pdf.text(50, 79, 'pdf.mirror_h(x_of_axis)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror horizontally with axis of reflection at x-position 50 (left side of the rectangle)
pdf.mirror_h(50)
pdf.rect(50, 80, 40, 10, 'D')
pdf.text(50, 79, 'pdf.mirror_h(50)')
#Stop Transformation
pdf.stop_transform()

#Mirroring vertically
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 80, 40, 10, 'D')
pdf.text(125, 79, 'pdf.mirror_v(y_of_axis)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror vertically with axis of reflection at y-position 90 (bottom side of the rectangle)
pdf.mirror_v(90)
pdf.rect(125, 80, 40, 10, 'D')
pdf.text(125, 79, 'pdf.mirror_v(90)')
#Stop Transformation
pdf.stop_transform()

#Point reflection
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(50, 110, 40, 10, 'D')
pdf.text(50, 109, 'pdf.mirror_p(x_of_point,y_of_point)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#point reflection at the lower left point of rectangle
pdf.mirror_p(50,120)
pdf.rect(50, 110, 40, 10, 'D')
pdf.text(50, 109, 'pdf.mirror_p(50,120)')
#Stop Transformation
pdf.stop_transform()

#Mirroring against a straigth line described by a point (120, 120) and an angle -20°
angle=-20
px=120
py=120

#just vor visualisation: the straight line to mirror against
pdf.set_draw_color(200)
pdf.line(px-1,py-1,px+1,py+1)
pdf.line(px-1,py+1,px+1,py-1)
pdf.start_transform()
pdf.t_rotate(angle, px, py)
pdf.line(px-5, py, px+60, py)
pdf.stop_transform()

pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 110, 40, 10, 'D')
pdf.text(125, 109, 'pdf.mirror_l(angle, px, py)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror against the straight line
pdf.mirror_l(angle, px, py)
pdf.rect(125, 110, 40, 10, 'D')
pdf.text(125, 109, 'pdf.mirror_l(-20, 120, 120)')
#Stop Transformation
pdf.stop_transform()

# circular text
pdf.add_page()
pdf.set_font('Helvetica','B',32)

text='Circular Text'
pdf.circular_text(105, 50, 35, text, 'top')
pdf.circular_text(105, 50, 35, text, 'bottom')

pdf.set_line_width(2)
pdf.set_draw_color(r=230, g=30, b=180)
pdf.set_fill_color(210)

pdf.ellipse(x=63, y=108, w=85, h=85, style="FD")
pdf.set_font(size=13)

pdf.circular_text(105, 150, 40, "pdf.circular_text(105, 50, 30, text, 'top')", 'top')
pdf.circular_text(105, 150, 40, "pdf.circular_text(105, 150, 30, text, 'bottom')", 'bottom')

pdf.text(15, 220, 'pdf.circular_text(float x, float y, float r, str text [, str align [, float kerning [, float fontwidth]]])')

pdf.output("./demo.pdf")
```

The result should look like this:

![Transform, rotate, shear, mirror text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Transparency-for-pyFPDF-fpdf2/main/transform/transform.jpg)

![circular round text in pyFPDF](https://raw.githubusercontent.com/digidigital/Transparency-for-pyFPDF-fpdf2/main/transform/circular_text.jpg)
