# Adjust text to cell width
This method is an extension of cell() allowing to output text with either character spacing or horizontal scaling.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Fill cell() with text](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/cell_fit/cell_fit.png)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/cell_fit/demo.pdf)

## Usage

Just put PDFCellFit.py in your project directory

```python
#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Author: Patrick Benny
# License: FPDF
# http://www.fpdf.org/en/script/script62.php

from fpdf import FPDF

class PDFCellFit(FPDF):

    #Cell with horizontal scaling if text is too wide
    def cell_fit(self,  w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', scale=False, force=True, center=False, markdown=False):

        #Get string width
        str_width=self.get_string_width(txt)
        #Calculate ratio to fit cell
        if w==0:
            w = self.w-self.r_margin-self.x
        ratio = (w-self.c_margin*2)/str_width

        fit = (ratio < 1 or (ratio > 1 and force))
        if fit:

            if scale:

                #Calculate horizontal scaling
                horiz_scale=ratio*100.0
                #Set horizontal scaling
                self._out('BT %.2F Tz ET' % (horiz_scale))

            else:

                #Calculate character spacing in points
                char_space=(w-self.c_margin*2-str_width)/max(len(txt)-1,1)*self.k
                #Set character spacing
                self._out('BT %.2F Tc ET' % (char_space))

            
          
        #Pass on to Cell method
        #Override user alignment (since text will fill up cell)
        align=''
        self.cell(w, h, txt, border, ln, align, fill, link, center, markdown)

        #Reset character spacing/horizontal scaling
        if fit:
            self._out('BT ' + ('100 Tz' if scale else '0 Tc') + ' ET')


    #Cell with horizontal scaling only if necessary
    def cell_fit_scale(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, True, False, center, markdown)


    #Cell with horizontal scaling always
    def cell_fit_scale_force(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, True, True, center, markdown)


    #Cell with character spacing only if necessary
    def cell_fit_space(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, False, False, center, markdown)


    #Cell with character spacing always
    def cell_fit_space_force(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):
        #Same as calling cell_fit directly
        self.cell_fit(w, h, txt, border, ln, align, fill, link, False, True, center, markdown)
```

Import the script and use pyFPDF as usual.

`cell_fit(float w [, float h [, string txt [, mixed border [, int ln [, string align [, boolean fill [, mixed link [, boolean scale [, boolean force]]]]]]]]])`

The first 8 parameters are the same as cell(). The additional parameters are:

scale
-> False: character spacing
-> True: horizontal scaling

force
-> False: only space/scale if necessary (not when text is short enough to fit)
-> True: always space/scale

The following four methods are also provided for convenience, allowing all combinations of scale/force, and using only the 8 parameters of cell():

* `cell_fit_scale()`
* `cell_fit_scale_force()`
* `cell_fit_space()`
* `cell_fit_space_force()`

```python
#!/usr/bin/python3

from PDFCellFit import PDFCellFit as FPDF

# Script does not work well with markdown enabled
# Styles B,I,U work fine
 
txt_short = 'This text is short enough.'
txt_long = 'This text is way too long.'
for i in range(2):
    txt_long+=' ' + txt_long

pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(255,255,255)

pdf.set_font('Helvetica','B',16)
pdf.write(10,'Cell')
pdf.set_font('')
pdf.ln()
pdf.cell(0,10,txt_short,1,1)
pdf.cell(0,10,txt_long,1,1)
pdf.ln(20)

pdf.set_font('','B')
pdf.write(10,'cell_fit_scale')
pdf.set_font('')
pdf.write(10,' (horizontal scaling only if necessary)')
pdf.ln()
pdf.cell_fit_scale(0,10,txt_short,1,1)
pdf.cell_fit_scale(0,10,txt_long,1,1,'',1)
pdf.ln()

pdf.set_font('','B')
pdf.write(10,'cell_fit_scale_force')
pdf.set_font('')
pdf.write(10,' (horizontal scaling always)')
pdf.ln()
pdf.cell_fit_scale_force(0,10,txt_short,1,1,'',1)
pdf.cell_fit_scale_force(0,10,txt_long,1,1,'',1)
pdf.ln(20)

pdf.set_font('','B')
pdf.write(10,'cell_fit_space')
pdf.set_font('')
pdf.write(10,' (character spacing only if necessary)')
pdf.ln()
pdf.cell_fit_space(0,10,txt_short,1,1)
pdf.cell_fit_space(0,10,txt_long,1,1,'',1)
pdf.ln()

pdf.set_font('','B')
pdf.write(10,'cell_fit_space_force')
pdf.set_font('')
pdf.write(10,' (character spacing always)')
pdf.ln()
pdf.cell_fit_space_force(0,10,txt_short,1,1,'',1)
pdf.cell_fit_space_force(0,10,txt_long,1,1,'',1)

pdf.output('demo.pdf')
```

