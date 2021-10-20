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
