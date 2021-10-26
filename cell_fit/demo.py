#!/usr/bin/python3

from PDFCellFit import PDFCellFit as FPDF

# Script does not work well with markdown enabled
# Styles B,I,U work fine
 
txt_short = 'This text is short enough.'
txt_long = 'This text is way too long.'
for i in range(2):
    txt_long+=' ' + txt_long

pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(255,255,255)

pdf.set_font('Helvetica','B',16)
pdf.write(10,'Cell')
pdf.set_font('')
pdf.ln()
pdf.cell(0,10,txt_short,1,1)
pdf.cell(0,10,txt_long,1,1)
pdf.ln(20)

pdf.set_font('','B')
pdf.write(10,'cell_fit_scale')
pdf.set_font('')
pdf.write(10,' (horizontal scaling only if necessary)')
pdf.ln()
pdf.cell_fit_scale(0,10,txt_short,1,1)
pdf.cell_fit_scale(0,10,txt_long,1,1,'',1)
pdf.ln()

pdf.set_font('','B')
pdf.write(10,'cell_fit_scale_force')
pdf.set_font('')
pdf.write(10,' (horizontal scaling always)')
pdf.ln()
pdf.cell_fit_scale_force(0,10,txt_short,1,1,'',1)
pdf.cell_fit_scale_force(0,10,txt_long,1,1,'',1)
pdf.ln(20)

pdf.set_font('','B')
pdf.write(10,'cell_fit_space')
pdf.set_font('')
pdf.write(10,' (character spacing only if necessary)')
pdf.ln()
pdf.cell_fit_space(0,10,txt_short,1,1)
pdf.cell_fit_space(0,10,txt_long,1,1,'',1)
pdf.ln()

pdf.set_font('','B')
pdf.write(10,'cell_fit_space_force')
pdf.set_font('')
pdf.write(10,' (character spacing always)')
pdf.ln()
pdf.cell_fit_space_force(0,10,txt_short,1,1,'',1)
pdf.cell_fit_space_force(0,10,txt_long,1,1,'',1)

pdf.output('demo.pdf')