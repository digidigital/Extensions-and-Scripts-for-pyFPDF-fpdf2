#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Author: Patrick Benny
# License: FPDF
# http://www.fpdf.org/en/script/script62.php

from fpdf import FPDF

class PDFCellFit(FPDF):

    #Cell with horizontal scaling if text is too wide
    def cell_fit(self,  w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', scale=False, force=True, center=False, markdown=False):

        #Get string width
        str_width=self.get_string_width(txt)
        #Calculate ratio to fit cell
        if w==0:
            w = self.w-self.r_margin-self.x
        ratio = (w-self.c_margin*2)/str_width

        fit = (ratio < 1 or (ratio > 1 and force))
        if fit:

            if scale:

                #Calculate horizontal scaling
                horiz_scale=ratio*100.0
                #Set horizontal scaling
                self._out('BT %.2F Tz ET' % (horiz_scale))

            else:

                #Calculate character spacing in points
                char_space=(w-self.c_margin*2-str_width)/max(len(txt)-1,1)*self.k
                #Set character spacing
                self._out('BT %.2F Tc ET' % (char_space))

            
          
        #Pass on to Cell method
        #Override user alignment (since text will fill up cell)
        align=''
        self.cell(w, h, txt, border, ln, align, fill, link, center, markdown)

        #Reset character spacing/horizontal scaling
        if fit:
            self._out('BT ' + ('100 Tz' if scale else '0 Tc') + ' ET')


    #Cell with horizontal scaling only if necessary
    def cell_fit_scale(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, True, False, center, markdown)


    #Cell with horizontal scaling always
    def cell_fit_scale_force(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, True, True, center, markdown)


    #Cell with character spacing only if necessary
    def cell_fit_space(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):

        self.cell_fit(w, h, txt, border, ln, align, fill, link, False, False, center, markdown)


    #Cell with character spacing always
    def cell_fit_space_force(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link='', center=False, markdown=False):
        #Same as calling cell_fit directly
        self.cell_fit(w, h, txt, border, ln, align, fill, link, False, True, center, markdown)