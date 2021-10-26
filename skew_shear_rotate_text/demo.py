#!/usr/bin/python3

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