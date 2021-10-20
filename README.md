# Transparency for pyFPDF (fpdf2)
This script adds transparency support to pyFPDF. You can set the alpha channel from 0 (fully transparent) to 1 (fully opaque). It applies to all elements (text, drawings, images). 

Tested with fpdf2 2.4.5, Pillow 8.3.1 & Python 3.8.10

## Usage

Just put AlphaFPDF.py in your project directory

```
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

Use pdf.set_alpha(X) to set the transparency where
X is a value between 0 (transparent) and 1 (opaque)

```
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

![Transparent text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Transparency-for-pyFPDF-fpdf2/main/result.jpg)

### The script is the answer for:
* How to create a PDF with transparent text in Python?
* How to add images with alpha/transparency in pyFPDF?
* How to add dynamic transparent overlay / stamps to PDF documents?
