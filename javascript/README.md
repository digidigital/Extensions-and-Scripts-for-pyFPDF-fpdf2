# Embed Javascript in PDF for pyFPDF (fpdf2)
This script allows to embed JavaScript inside the PDF. The code is executed when the document is opened.

The Acrobat JavaScript reference is available [here](https://opensource.adobe.com/dc-acrobat-sdk-docs/acrobatsdk/).

**Note: Support depends on the PDF viewer and security settings.** 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/javascript/demo.pdf)

## Usage

Just put PDFJavascript.py in your project directory

```python
#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Johannes Güntert
# License: FPDF 
# http://www.fpdf.org/en/script/script36.php

from fpdf import FPDF, util

class PDFJavascript(FPDF):

    _javascript=''

    def include_js(self, script, isUTF8=False): 
        self._javascript=str(script)
    
    def _outjavascript(self): 
        self._newobj()
        self._n_js=self.n
        self._out('<<')
        self._out('/Names [(EmbeddedJS) ' + str((self.n+1)) + ' 0 R]')
        self._out('>>')
        self._out('endobj')
        self._newobj()
        self._out('<<')
        self._out('/S /JavaScript')
        self._out('/JS (' + util.escape_parens(self.normalize_text(self._javascript)) + ')' )
        self._out('>>')
        self._out('endobj')

    def _putresources(self): 
        super()._putresources()
        if len(self._javascript)>0: 
            self._outjavascript()

    def _putcatalog(self): 
        super()._putcatalog()
        if len(self._javascript)>0: 
            self._out('/Names <</JavaScript ' + str(self._n_js) + ' 0 R>>')
```

Import the script and use pyFPDF as usual.

Use `include_js(str x)` to add yout Javascript code to your PDF.

This example shows how to open the print dialog when the document has loaded (**doesn't work with all viewers!**). 
```python
#!/usr/bin/python3

from PDFJavascript import PDFJavascript as FPDF

# This example shows how to open the print dialog when the document has loaded.

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', '', 20)
pdf.text(90, 50, 'Print me!')
pdf.include_js('print(true);')
pdf.output('demo.pdf')
```

