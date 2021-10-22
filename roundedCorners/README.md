# Rectangle with rounded corners for pyFPDF (fpdf2)
Draw rectangles with rounded corners

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example
![Draw a rectangle with rounded corners in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/roundedCorners/demo.jpg)

[PDF file](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/roundedCorners/demo.pdf)

## Usage

Just put PDFRounded.py in your project directory and import it.

```python
#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Maxime Delorme
# License: FPDF 
# http://www.fpdf.org/en/script/script7.php
# Original Author: Christophe Prugnaud
# License: FPDF 
# http://www.fpdf.org/en/script/script35.php

from fpdf import FPDF
from math import sqrt

class PDFRounded (FPDF):

    def rounded_rect(self, x, y, w, h, r, style = '', corners = '1234'):
    
        k = self.k
        hp = self.h
        if(style=='F'):
            op='f'
        elif(style=='FD' or style=='DF'):
            op='B'
        else:
            op='S'
        myArc = 4/3 * (sqrt(2) - 1)
        self._out('%.2F %.2F m' % ((x+r)*k,(hp-y)*k))

        xc = x+w-r
        yc = y+r
        self._out('%.2F %.2F l' % (xc*k,(hp-y)*k))
        if '2' not in corners:
            self._out('%.2F %.2F l' % ((x+w)*k,(hp-y)*k))
        else:
            self._arc(xc + r*myArc, yc - r, xc + r, yc - r*myArc, xc + r, yc)

        xc = x+w-r
        yc = y+h-r
        self._out('%.2F %.2F l' % ((x+w)*k,(hp-yc)*k))
        if '3' not in corners:
            self._out('%.2F %.2F l' % ((x+w)*k,(hp-(y+h))*k))
        else:
            self._arc(xc + r, yc + r*myArc, xc + r*myArc, yc + r, xc, yc + r)

        xc = x+r
        yc = y+h-r
        self._out('%.2F %.2F l' % (xc*k,(hp-(y+h))*k))
        if '4' not in corners:
            self._out('%.2F %.2F l' % (x*k,(hp-(y+h))*k))
        else:
            self._arc(xc - r*myArc, yc + r, xc - r, yc + r*myArc, xc - r, yc)

        xc = x+r 
        yc = y+r
        self._out('%.2F %.2F l' % (x*k,(hp-yc)*k))
        if '1' not in corners:
            self._out('%.2F %.2F l' % (x*k,(hp-y)*k))
            self._out('%.2F %.2F l' % ((x+r)*k,(hp-y)*k))
        else:
            self._arc(xc - r, yc - r*myArc, xc - r*myArc, yc - r, xc, yc - r)
        self._out(op)
    

    def _arc(self, x1, y1, x2, y2, x3, y3):
    
        h = self.h
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c ' % (x1*self.k, (h-y1)*self.k,
            x2*self.k, (h-y2)*self.k, x3*self.k, (h-y3)*self.k))
```

Import the script and use pyFPDF as usual.

rounded_rect(x, y, w, h, r, style = '', corners = '')
* x, y: top left corner of the rectangle.
* w, h: width and height.
* r: radius of the rounded corners.
* corners: numbers of the corners to be rounded: 1, 2, 3, 4 or any combination (1=top left, 2=top right, 3=bottom right, 4=bottom left).
* style: same as Rect(): F, D (default), FD or DF. 

```python
#!/usr/bin/python3

from PDFRounded import PDFRounded as FPDF

pdf=FPDF()
pdf.add_page()
pdf.set_fill_color(192)
pdf.rounded_rect(60, 30, 68, 46, 5, 'DF', '13')

pdf.rounded_rect(60, 95, 68, 46, 5, 'D', '24')

pdf.rounded_rect(60, 160, 68, 46, 5, 'F', '1234')

pdf.output('demo.pdf')
```

