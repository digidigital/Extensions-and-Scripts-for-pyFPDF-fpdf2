#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Olivier
# License: FPDF 
# http:#www.fpdf.org/en/script/script75.php

from fpdf import FPDF

class PDFVisibility(FPDF):
    
    _visibility = None

    def set_visibility(self, v):
        if self._visibility!='all':
            self._out('EMC')
        if v=='print':
            self._out('/OC /OC1 BDC')
        elif v=='screen':
            self._out('/OC /OC2 BDC')
        elif v!='all':
            raise ValueError(
                'Incorrect visibility: ' +  v
            )
        self._visibility = v
    
    def _endpage(self): 
        self.set_visibility('all')
        super()._endpage()
    
    def _enddoc(self):
        if float(self.pdf_version)<1.5:
            self.pdf_version = '1.5'
        super()._enddoc()
    
    def _putocg(self):  
        self._newobj()
        self.n_ocg_print = self.n
        self._out('<</Type /OCG /Name ' + self._escape('(print)'))
        self._out('/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>')
        self._out('endobj')
        self._newobj()
        self.n_ocg_view = self.n
        self._out('<</Type /OCG /Name ' + self._escape('(view)'))
        self._out('/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>')
        self._out('endobj')
    
    def _putresources(self):
        self._putocg()
        super()._putresources()
    
    def _putresourcedict(self):
        super()._putresourcedict()
        self._out('/Properties <</OC1 ' + str(self.n_ocg_print) +' 0 R /OC2 ' + str(self.n_ocg_view) + ' 0 R>>')
    
    def _putcatalog(self):
        super()._putcatalog()
        p = str(self.n_ocg_print) + ' 0 R'
        v = str(self.n_ocg_view) + ' 0 R'
        a_s = "<</Event /Print /OCGs [" + p + " " + v +"] /Category [/Print]>> <</Event /View /OCGs [" + p + " " + v +"] /Category [/View]>>"
        self._out("/OCProperties <</OCGs [" + p + " " + v +"] /D <</ON [" + p + "] /OFF [" + v + "] /AS [" + a_s + "]>>>>")

    def _escape(self, string):
        # Escape special characters
        string=string.replace('\\','\\\\')
        string=string.replace('(','\\(')
        string=string.replace(')','\\)')
        string=string.replace('\r','\\r')
        return string