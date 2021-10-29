#!/usr/bin/python3

from PDFSinusText import PDFSinusText as FPDF

pdf=FPDF()
pdf.add_page()

pdf.set_font('helvetica', 'B', 10)
pdf.set_text_color(250, 0, 0)

txt1 = 'The Quick Brown Fox Jumps Over The Lazy Dogs.'
txt2 = '+++++++++++++++++++++++++++++++++++++++'

pdf.sinus_text(20, 30, txt1, 10, 3)
pdf.sinus_text(20, 60, txt1, 10, -3)

pdf.sinus_text(20, 100, txt1, 50, 1)
pdf.sinus_text(20, 170, txt1, 50, -1)

pdf.set_text_color(0, 0, 250)

pdf.sinus_text(20, 200, txt2, 10, -10,1)

pdf.sinus_text(20, 250, '! Just a test !', 0,0,5)

pdf.output('demo.pdf')