#!/usr/bin/python3

from PDFDiagrams import PDFDiagrams as FPDF

pdf = FPDF()
pdf.add_page()

data = {'Men':1510, 'Women':1610, 'Children':1400}

#Pie chart
pdf.set_font('Helvetica', 'BIU', 12)
pdf.cell(0, 5, '1 - Pie chart', 0, 1)
pdf.ln(8)

pdf.set_font('Helvetica', '', 10)
valX = pdf.get_x()
valY = pdf.get_y()

pdf.cell(30, 5, 'Number of men:')
pdf.cell(15, 5, str(data['Men']), 0, 0, 'R')
pdf.ln()
pdf.cell(30, 5, 'Number of women:')
pdf.cell(15, 5, str(data['Women']), 0, 0, 'R')
pdf.ln()
pdf.cell(30, 5, 'Number of children:')
pdf.cell(15, 5, str(data['Children']), 0, 0, 'R')
pdf.ln()
pdf.ln(8)

pdf.set_xy(90, valY)
col1=(100,100,255)
col2=(255,100,100)
col3=(255,255,100)
pdf.pie_chart(100, 35, data, '%l (%p)', (col1,col2,col3))
pdf.set_xy(valX, valY + 40)

#Bar diagram
pdf.set_font('Helvetica', 'BIU', 12)
pdf.cell(0, 5, '2 - Bar diagram', 0, 1)
pdf.ln(8)
valX = pdf.get_x()
valY = pdf.get_y()
pdf.bar_diagram(190, 70, data, '%l : %v (%p)', (255,175,100))
pdf.set_xy(valX, valY + 80)

pdf.output('demo.pdf')