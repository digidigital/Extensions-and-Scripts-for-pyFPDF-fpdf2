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
