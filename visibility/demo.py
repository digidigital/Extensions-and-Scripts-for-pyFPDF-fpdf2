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