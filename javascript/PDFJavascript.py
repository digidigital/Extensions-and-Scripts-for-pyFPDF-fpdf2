#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Johannes Güntert
# License: FPDF 
# http://www.fpdf.org/en/script/script36.php

from fpdf import FPDF

class PDFJavascript(FPDF):

    _javascript=''
    #_n_js=0

    def include_js(self, script, isUTF8=False): 
        self._javascript=str(script)
    
    def _outjavascript(self): 
        self._newobj()
        self._n_js=self.n
        self._out('<<')
        self._out('/Names [(EmbeddedJS) ' + str((self.n+1)) + ' 0 R]')
        self._out('>>')
        self._out('endobj')
        self._newobj()
        self._out('<<')
        self._out('/S /JavaScript')
        self._out('/JS (' + self._escape(self.normalize_text(self._javascript)) + ')' )
        self._out('>>')
        self._out('endobj')

    def _putresources(self): 
        super()._putresources()
        if len(self._javascript)>0: 
            self._outjavascript()

    def _putcatalog(self): 
        super()._putcatalog()
        if len(self._javascript)>0: 
            self._out('/Names <</JavaScript ' + str((self._n_js)) + ' 0 R>>')

    def _escape(self, string):
        # Escape special characters
        string=string.replace('\\','\\\\')
        string=string.replace('(','\\(')
        string=string.replace(')','\\)')
        string=string.replace('\r','\\r')
        return string