#!/usr/bin/python3

from PDFSector import PDFSector as FPDF

pdf = FPDF()
pdf.add_page()
xc=105
yc=60
r=40
pdf.set_fill_color(120,120,255)
pdf.sector(xc,yc,r,20,120)
pdf.set_fill_color(120,255,120)
pdf.sector(xc,yc,r,120,250)
pdf.set_fill_color(255,120,120)
pdf.sector(xc,yc,r,250,20)
pdf.output('demo.pdf')