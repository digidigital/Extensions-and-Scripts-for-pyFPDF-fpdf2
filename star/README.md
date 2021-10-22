# Star shape for pyFPDF (fpdf2)
This script draws a star.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Usage

Just put PDFStar.py in your project directory ans import it.

```python
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
```

Import the script and use pyFPDF as usual.

star(float x, float y, float rin, float rout, int points [, string style])

x: abscissa of center.

y: ordinate of center.

rin: internal radius.

rout: external radius.

points: number of points that the star is composed of.

style: style of rendering, the same as for rect(): D, F or FD.

Note: if rin=rout, the star will appear as a circle. 

```python
#!/usr/bin/python3

from PDFStar import PDFStar as FPDF

#Example
pdf = FPDF()
pdf.add_page()

pdf.set_draw_color(0,0,0)
pdf.set_fill_color(255,0,0)
pdf.set_line_width(0.5)
pdf.star(100,60,40,30,36,'DF')

pdf.set_draw_color(0,0,150)
pdf.set_line_width(1)
pdf.star(100,150,40,30,10,'D')

pdf.set_fill_color(200,200,200)
pdf.set_line_width(1)
pdf.star(100,240,40,15,5,'F')

pdf.output('demo.pdf')
```

Gives you:

![Transparent text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/star/demo.jpg)

