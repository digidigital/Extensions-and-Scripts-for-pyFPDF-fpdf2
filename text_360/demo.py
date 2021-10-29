#!/usr/bin/python3

from PDFText360 import PDFText360 as FPDF

pdf = FPDF()
pdf.add_page()

txt1 = 'The Quick Brown Fox Jumps Over The Lazy Dog.'
txt2 = '---------------------------------------------------------------------------------------------------'

pdf.set_font("helvetica", "B", 20)
pdf.set_text_color(250, 0, 0)

pdf.text_360(105, 100, txt1, 80)
pdf.text_360(105, 100, txt2, 100)

pdf.set_font("times", "IU", 10)
pdf.set_text_color(0, 0, 250)

pdf.text_360(105, 100, txt1, 60)

pdf.output('demo.pdf')