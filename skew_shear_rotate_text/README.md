# Skew, shear and rotate text
This extension allows to print rotated and sheared (i.e. distorted like in italic) text.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Skew, shear and rotate text in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/skew_shear_rotate_text/demo.png)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/skew_shear_rotate_text/demo.pdf)

## Usage

Just put PDFTextR.py in your project directory

```python
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
```

Import the script and use pyFPDF as usual.

`tex_with_direction(float x, float y, string txt [, string direction])`

x: abscissa
y: ordinate
txt: text string
direction: one of the following values (R by default):

    R (Right): Left to Right
    U (Up): Bottom to Top
    D (Down): Top To Bottom
    L (Left): Right to Left

`text_with_rotation(float x, float y, string txt, float txt_angle [, float font_angle])`

x: abscissa
y: ordinate
txt: text string
txt_angle: angle of the text
font_angle: shear angle (0 by default)

```python
from PDFTextR import PDFTextR as FPDF

# Example
# Underline is not supported since underline is not a 
# property of a font. Instead FPDF draws a line.

pdf=FPDF()
pdf.add_page()
pdf.set_font('Helvetica','B',40)
pdf.text_with_rotation(50,65,'Hello',45,-45)
pdf.set_font_size(30)
pdf.text_with_direction(110,50,'World!','L')
pdf.set_text_color(255,0,0)
pdf.text_with_direction(110,50,'World!','U')
pdf.set_text_color(0,255,0)
pdf.set_font(style='I')
pdf.text_with_direction(110,50,'World!','R')
pdf.set_text_color(0,0,255)
pdf.text_with_direction(110,50,'World!','D')
pdf.output('demo.pdf')
```
