#!/usr/bin/env python3
# Ported from PHP to Python / pyFPDF2 in 2021 by Björn Seipel
# Original Author: Martin Hall-May
# License: FPDF 
# http://www.fpdf.org/en/script/script74.php
from fpdf import FPDF

class AlphaFPDF (FPDF):

    _extgstates = {}

    # alpha: real value from 0 (transparent) to 1 (opaque)
    # bm:    blend mode, one of the following:
    #          Normal, Multiply, Screen, Overlay, Darken, Lighten, ColorDodge, ColorBurn,
    #          HardLight, SoftLight, Difference, Exclusion, Hue, Saturation, Color, Luminosity
    def set_alpha(self, alpha, bm='Normal'):
        if alpha < 0: alpha=0
        if alpha > 1: alpha=1
        # set alpha for stroking (CA) and non-stroking (ca) operations
        gs = self.add_ext_gs_state({'ca':alpha, 'CA':alpha, 'BM':'/' + bm})
        self.set_ext_gs_state(gs)

    def add_ext_gs_state(self, parms):
        n = len(self._extgstates)+1
        self._extgstates[n] = {'parms': parms}
        
        return n
    
    def set_ext_gs_state(self, gs):
        self._out("/GS%d gs" % gs)
    
    def _enddoc(self):
        if len(self._extgstates) > 0 and float(self.pdf_version) < float(1.4):
            self.pdf_version='1.4'
        super()._enddoc()
    
    def _putextgstates(self):
        for i in range (1, len(self._extgstates)+1):
            self._newobj()
            self._extgstates[i]['n'] = self.n
            self._out('<</Type /ExtGState')
            parms = self._extgstates[i]['parms']
            self._out("/ca %.3F" % parms['ca'])
            self._out("/CA %.3F" % parms['CA'])
            self._out('/BM ' + parms['BM'])
            self._out('>>')
            self._out('endobj')
    
    def _putresourcedict(self):
        super()._putresourcedict(self)
        self._out('/ExtGState <<')
        for k, extgstate in zip(self._extgstates.keys(), self._extgstates.values()):
            self._out('/GS' + str(k) + ' ' + str(extgstate['n']) + ' 0 R')
                    
        self._out('>>')
                
    def _putresources(self):
        self._putextgstates()
        super()._putresources(self)
