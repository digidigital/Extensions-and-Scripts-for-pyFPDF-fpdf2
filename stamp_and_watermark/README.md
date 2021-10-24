# Stamp and Watermark PDF (fpdf2)
This script adds support for stamps (overlay) and watermarks (underlay) to PDF files by modifying the 'header()' and 'footer()' functions. 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Mass stamping or watermarking PDF files](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/stamp_and_watermark/stamp_and_watermark.png)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/stamp_and_watermark/demo.pdf)

## Usage

Just put PDFMark.py and AlphaFPDF.py in your project directory

```python
##!/usr/bin/env python3
# Author: Björn Seipel
# License: MIT

from AlphaFPDF import AlphaFPDF

class PDFMark(AlphaFPDF):

    _watermark_data=[]
    _stamp_data=[]

    def watermark(self, text, x=None, y=None, angle=45, alpha=1, text_color=[200,200,200], font='Helvetica', font_size=50, font_style=''):        
        self._watermark_data = [text, x, y, angle, alpha, text_color, font, font_size, font_style]

    def stamp(self, text, x=None, y=None, angle=45, alpha=1, text_color=[255,0,0], font='Helvetica', font_size=50, font_style=''):
        self._stamp_data     = [text, x, y, angle, alpha, text_color, font, font_size, font_style]
    
    def _mark(self, text_data):
        if len(text_data)!=0:
            #store current x, y coordinates
            old_X, old_y = self.get_x(), self.get_y()
            
            self.set_font(text_data[6], text_data[8] , text_data[7])
            r,g,b = text_data[5]
            self.set_text_color(r, g, b)
            self.set_alpha(text_data[4])
            
            text=text_data[0]
            stringWidth=self.get_string_width(text)/2
            x, y =text_data[1], text_data[2] 
            
            if x==None:
                x=self.w/2-stringWidth
            if y==None:
                y=self.h/2
            
            #rotate and print text
            with self.rotation(text_data[3], x+stringWidth, y):
                self.text(x,y, text)                                 
            
            #set alpha back to opaque
            self.set_alpha(1)
            #store old coordinates
            self.set_xy(old_X,old_y)
            
    def header(self):
        try: 
            super().header()
        except:
            pass
        self._mark(self._watermark_data)

    def footer(self):
        try: 
            super().footer()
        except:
            pass
        self._mark(self._stamp_data)
```

Import the script and use pyFPDF as usual.

Use
`watermark(str text, float x=None, float y=None, int angle=45, float alpha=1, list text_color=\[200,200,200], str font='Helvetica', int font_size=50, str font_style='')`
to add an underlay text to all pages that are added ***after*** watermark was set.

Use
`stamp(str text, float x=None, float y=None, int angle=45, float alpha=1, list text_color=\[200,200,200], str font='Helvetica', int font_size=50, str font_style='')`
to add an overlay to all pages ***including*** the current one.

* txt: The textstring that you want to use as stamp / watermark
* x: x-coordinate
* y: y-coordinate
* angle: The angle used to rotate the text
* alpha: A float defining the transparency of a stamp. A value between 0 and 1 (0=transparent, 1=opaque) 
* text_color: A list with three values between 0 and 255 \[red,green,blue])
* font: String with one of the installed fonts
* font_size: The font size
* font_style: A string containing one or more of the letters B, I, U (bold, italic, underline)  

All values except 'text' are optional

```python
#!/usr/bin/env python3

from PDFMark import PDFMark as FPDF 
from random import randint

#some random text to fill the pages 
def textlines(pdf, lines):
    loremIpsum='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.'
    for x in range (0, lines):
        pdf.cell(180, 5, loremIpsum)
        pdf.ln() 

pdf = FPDF()

#set stamp prior to calling add_page()
pdf.stamp( 'APPROVED', y=50, angle=10, font_size=60, font_style='BIU')
#set watermark prior to calling add_page()
pdf.watermark('DRAFT CONTRACT', font_style='BI')

pdf.add_page()
pdf.set_font('Helvetica', 'B', 12)
textlines(pdf, 50)

pdf.add_page()
pdf.set_text_color(0, 0, 255)
pdf.set_font('Helvetica', 'I', 12)
textlines(pdf, 30)
#change watermark for all pages that follow (pass empty string to stop printing watermarks)  
pdf.watermark('New Watermark', angle=0, text_color=[255,255,50], font='Courier', font_style='BI')

pdf.add_page()
#change stamp for this page and all that follow (pass empty string to stop printing stamps)
pdf.stamp('NOT APPROVED!', alpha=0.5, angle=10, font_size=60, font_style='BIU')
pdf.set_text_color(0, 255, 255)
pdf.set_font('Times', 'B', 12)
textlines(pdf, 50)

pdf.output('demo.pdf')
```

### This script is the answer for:
* How to batch stamp PDF files with fpdf?
* How to add stamps with alpha/transparency in pyFPDF?

