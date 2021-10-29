# 360 Degree Text
This script adds 360 degree text. `B`, `U` and `I` are supported. 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![360 Degree Text](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/text_360/demo.png)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/text_360/demo.pdf)

## Usage

Just put PDFText360.py in your project directory

```python
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
 
        for non_printable in ('\n', '\t', '\r'):    
            text=text.replace(non_printable,'')

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
```

Import the script.

Use `text_360(x, y, text, width)` to write your 360 degree text on the page.

* x: x-coordinate of the center of the text
* y: y-coordinate of the center of the text
* text: The text to be printed
* width: The width of the circle 

All parameters except for `text` are optional. `pdf.text_360(text='Lorem ipsum dolor sit amet.')` puts the text in the center of your page and the width is set to 1/2 of the text width (when printed horizontally).

```python
#!/usr/bin/python3

from PDFText360 import PDFText360 as FPDF

pdf = FPDF()
pdf.add_page()

txt1 = 'The Quick Brown Fox Jumps Over The Lazy Dog.'
txt2 = '---------------------------------------------------------------------------------------------------'

pdf.set_font("helvetica", "B", 20)
pdf.set_text_color(250, 0, 0)

pdf.text_360(105, 100, txt1, 80)
pdf.text_360(105, 100, txt2, 100)

pdf.set_font("times", "IU", 10)
pdf.set_text_color(0, 0, 250)

pdf.text_360(105, 100, txt1, 60)

pdf.output('demo.pdf')
```
