#!/usr/bin/python3

from PDFImageMask import PDFImageMask as FPDF

pdf = FPDF()

pdf.add_page()
pdf.set_font('Helvetica', 'B', 12)
pdf.image('./Background.png', 0, 0)

# Import mask image and define as mask
pdf.image('./Mask.png', is_mask=True)

# Import image and apply mask
# Note: If you use the image more than once it will be masked 
# every time even if you do not set mask_image  
pdf.image('./Portrait1.png', 25, 25, 50, mask_image='./Mask.png')
pdf.text(75, 70, 'Photo by yecayeca at Morguefile.com')
pdf.image('./Portrait2.png', 25, 75, 50, mask_image='./Mask.png')
pdf.text(75, 120, 'Photo by steveneder999 at Morguefile.com')

pdf.output('demo.pdf')