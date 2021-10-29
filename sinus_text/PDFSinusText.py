# #!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: CIX88
# License: „[…]Alle dargestellten Quelltexte sind frei verfügbar.[…]“ -> "[...]All source code presented is freely available.[...]"
# http:#www.cix88.de/cix_pdf/pdf_fpdf_allgemein/cix_tut_039.php

from fpdf import FPDF, util
from math import pi, cos, sin

class PDFSinusText(FPDF):

    def sinus_text_transform(self, x, y, txt, vs = 1, hs = 1, rota = 0, kipp = 0):

        if vs >= 0 and vs <= 1: vs = cos( rota ) + 0.45
        if hs >= 0 and hs <= 1: hs = cos( kipp ) + 0.45
                
        rota *= pi/180
        rota = sin(rota)
        kipp *= pi/180
        kipp = sin(kipp)

        s = 'BT %.2f %.2f %.2f %.2f %.2f %.2f Tm (%s) Tj ET' % (
            vs,
            rota,
            kipp,
            hs,
            x * self.k,
            (self.h-y) * self.k,
            util.escape_parens(txt)
             )

        if self.underline and txt!='': s += ' ' + self._do_underline(x,y,txt)
        s = 'q ' + self.text_color + ' ' + s + ' Q'
        self._out(s)

    def sinus_text(self,  x , y, text, amplitude = 20, phase_shift = 1, width_strech = 1.5):
        start_x = x
        start_y = y
        bb = self.get_string_width(text)
        step = '%.2f' % (bb/len(text))

        for i in range (0,len(text)):
            if i <= len(text):
                val = text[i]
                y = sin( start_x * phase_shift * (pi/180) ) * amplitude
                self.sinus_text_transform(start_x, y + start_y, val )
                start_x = start_x + ( self.get_string_width(val) * width_strech)