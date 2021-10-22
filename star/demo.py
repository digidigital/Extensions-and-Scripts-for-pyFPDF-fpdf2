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