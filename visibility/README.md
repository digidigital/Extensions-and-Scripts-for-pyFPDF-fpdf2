# Visibility feature for pyFPDF (fpdf2)
This script allows to restrict the rendering of some elements to screen or printout. This can be useful, for instance, to put a background image or color that will show on screen but won't print.

**Note: this feature is not supported by all PDF viewers.** 

Some Test on Ubuntu 20.04: 
- Chromium 94.0.4606.81 (Works as intended)
- Google Chrome 94.0.4606.81 (Works as intended)
- Evince 3.36.10 (Does not display content marked for screen display, but displays content marked for printing)   
- Okular 21.08.2 (Same result as for Evince)
- Firefox 93.0 (Ignores restrictions and displays all content)

Script was tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Usage

Just put PDFVisibility.py in your project directory and import it.

```python
#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Olivier
# License: FPDF 
# http:#www.fpdf.org/en/script/script75.php

from fpdf import FPDF

class PDFVisibility(FPDF):
    
    _visibility = None

    def set_visibility(self, v):
        if self._visibility!='all':
            self._out('EMC')
        if v=='print':
            self._out('/OC /OC1 BDC')
        elif v=='screen':
            self._out('/OC /OC2 BDC')
        elif v!='all':
            raise ValueError(
                'Incorrect visibility: ' +  v
            )
        self._visibility = v
    
    def _endpage(self): 
        self.set_visibility('all')
        super()._endpage()
    
    def _enddoc(self):
        if float(self.pdf_version)<1.5:
            self.pdf_version = '1.5'
        super()._enddoc()
    
    def _putocg(self):  
        self._newobj()
        self.n_ocg_print = self.n
        self._out('<</Type /OCG /Name ' + self._escape('(print)'))
        self._out('/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>')
        self._out('endobj')
        self._newobj()
        self.n_ocg_view = self.n
        self._out('<</Type /OCG /Name ' + self._escape('(view)'))
        self._out('/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>')
        self._out('endobj')
    
    def _putresources(self):
        self._putocg()
        super()._putresources()
    
    def _putresourcedict(self):
        super()._putresourcedict()
        self._out('/Properties <</OC1 ' + str(self.n_ocg_print) +' 0 R /OC2 ' + str(self.n_ocg_view) + ' 0 R>>')
    
    def _putcatalog(self):
        super()._putcatalog()
        p = str(self.n_ocg_print) + ' 0 R'
        v = str(self.n_ocg_view) + ' 0 R'
        a_s = "<</Event /Print /OCGs [" + p + " " + v +"] /Category [/Print]>> <</Event /View /OCGs [" + p + " " + v +"] /Category [/View]>>"
        self._out("/OCProperties <</OCGs [" + p + " " + v +"] /D <</ON [" + p + "] /OFF [" + v + "] /AS [" + a_s + "]>>>>")

    def _escape(self, string):
        # Escape special characters
        string=string.replace('\\','\\\\')
        string=string.replace('(','\\(')
        string=string.replace(')','\\)')
        string=string.replace('\r','\\r')
        return string
```

Import the script and use pyFPDF as usual.

set_visibility(string v)

v can take one of the following values:
* all: always visible
* print: visible only when printed
* screen: visible only when displayed on screen

```python
#!/usr/bin/env python3

from PDFVisibility import PDFVisibility as FPDF 

pdf = FPDF()    
pdf.add_page()
pdf.set_font('Helvetica', '', 14)
pdf.write(6, "This line is always displayed. Support of this feature depends on your reader.\n")
pdf.set_visibility('screen')
pdf.write(6, "This line is displayed on screen.\n")
pdf.set_visibility('print')
pdf.write(6, "This line is printed.\n")
pdf.set_visibility('all')
pdf.output('demo.pdf')
```
