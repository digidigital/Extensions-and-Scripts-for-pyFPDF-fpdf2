#!/usr/bin/python3

from PDFJavascript import PDFJavascript as FPDF

# This example shows how to open the print dialog when the document has loaded (doesn't work with Chrome).

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', '', 20)
pdf.text(90, 50, 'Print me!')
pdf.include_js('print(true);')
pdf.output('demo.pdf')