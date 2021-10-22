#!/usr/bin/python3

from PDFRounded import PDFRounded as FPDF

pdf=FPDF()
pdf.add_page()
pdf.set_fill_color(192)
pdf.rounded_rect(60, 30, 68, 46, 5, 'DF', '13')

pdf.rounded_rect(60, 95, 68, 46, 5, 'D', '24')

pdf.rounded_rect(60, 160, 68, 46, 5, 'F', '1234')

pdf.output('demo.pdf')