#!/usr/bin/python3
# Ported from PHP to Python by Björn Seipel in 2021
# License: MIT
# Original Author: Andreas Würmser
# License: FPDF 
# http://fpdf.org/en/script/script72.php

from fpdf import FPDF
from math import floor

class PDFGradients(FPDF):

    _gradients = {}

    def linear_gradient(self, x, y, w, h, col1=[], col2=[], coords=[0,0,1,0]):
        self.clip(x,y,w,h)
        self.gradient(2,col1,col2,coords)
    
    def radial_gradient(self, x, y, w, h, col1=[], col2=[], coords=[0.5,0.5,0.5,0.5,1]):
        self.clip(x,y,w,h)
        self.gradient(3,col1,col2,coords)
    
    def coons_patch_mesh(self, x, y, w, h, col1=[], col2=[], col3=[], col4=[], coords=[0.00,0.0,0.33,0.00,0.67,0.00,1.00,0.00,1.00,0.33,1.00,0.67,1.00,1.00,0.67,1.00,0.33,1.00,0.00,1.00,0.00,0.67,0.00,0.33], coords_min=0, coords_max=1):
        self.clip(x,y,w,h)        
        n = len(self._gradients)+1
        self._gradients[n]={}
        self._gradients[n]['type']=6 #coons patch mesh
        #check the coords array if it is the simple array or the multi patch array
        
        if isinstance(coords[0], (int, float)):
            col1=self._check_color_triplet(col1)
            col2=self._check_color_triplet(col2)
            col3=self._check_color_triplet(col3)
            col4=self._check_color_triplet(col4)
            patch_list={}
            patch_list[0]={}
            patch_list[0]['f']=0
            patch_list[0]['points']=coords
            patch_list[0]['colors']=({'r':col1[0],'g':col1[1],'b':col1[2]},
                                     {'r':col2[0],'g':col2[1],'b':col2[2]},
                                     {'r':col3[0],'g':col3[1],'b':col3[2]},
                                     {'r':col4[0],'g':col4[1],'b':col4[2]})
        else:
            #multi patch array
            patch_list=coords
        
        bpcd=65535 #16 BitsPerCoordinate
        #build the data stream
        self._gradients[n]['stream']=''
        for i in range(0,len(patch_list)):
            self._gradients[n]['stream']+=chr(patch_list[i]['f']) #start with the edge flag as 8 bit
            for j in range (0, len(patch_list[i]['points'])):
                #each point as 16 bit
                patch_list[i]['points'][j]=((patch_list[i]['points'][j]-coords_min)/(coords_max-coords_min))*bpcd
                if patch_list[i]['points'][j]<0: patch_list[i]['points'][j]=0
                if patch_list[i]['points'][j]>bpcd: patch_list[i]['points'][j]=bpcd
                self._gradients[n]['stream']+=chr(floor(patch_list[i]['points'][j]/256))
                self._gradients[n]['stream']+=chr(floor(patch_list[i]['points'][j]%256))
            
            for j in range(0,len(patch_list[i]['colors'])):
                #each color component as 8 bit
                self._gradients[n]['stream']+=chr(patch_list[i]['colors'][j]['r'])
                self._gradients[n]['stream']+=chr(patch_list[i]['colors'][j]['g'])
                self._gradients[n]['stream']+=chr(patch_list[i]['colors'][j]['b'])
            
        #paint the gradient
        self._out('/Sh' + str(n) + ' sh')
        #restore previous Graphic State
        self._out('Q')
    
    def clip(self, x,y,w,h):
        #save current Graphic State
        s='q'
        #set clipping area
        s= s + ' %.2F %.2F %.2F %.2F re W n' % (x*self.k, (self.h-y)*self.k, w*self.k, -h*self.k)
        #set up transformation matrix for gradient
        s= s + ' %.3F 0 0 %.3F %.3F %.3F cm' % (w*self.k, h*self.k, x*self.k, (self.h-(y+h))*self.k)
        self._out(s)
    
    def _check_color_triplet(self,col):
        # if only one value for color is submitted as single value or list
        # make color grayscale by seeting this value for r, g and b
        if isinstance (col, (int, float)):
            col = int(col)
            col = [col,col,col]
        elif len(col)==1:
            col = int(col[0])
            col = [col,col,col]
        return col
    
    def gradient(self, grad_type, col1, col2, coords):
        
        n = len(self._gradients)+1
        self._gradients[n]={}
        self._gradients[n]['type']=grad_type
        col1=self._check_color_triplet(col1)
        col2=self._check_color_triplet(col2)
        self._gradients[n]['col1']='%.3F %.3F %.3F' % ((col1[0]/255),(col1[1]/255),(col1[2]/255))
        self._gradients[n]['col2']='%.3F %.3F %.3F' % ((col2[0]/255),(col2[1]/255),(col2[2]/255))
        self._gradients[n]['coords']=coords
        #paint the gradient
        self._out('/Sh' + str(n) + ' sh')
        #restore previous Graphic State
        self._out('Q')
    
    def _putshaders(self):
        #foreach(self._gradients as id:grad)
        for gradNo, grad in zip(self._gradients.keys(), self._gradients.values()):  
            if grad['type']==2 or grad['type']==3:
                self._newobj()
                self._out('<<')
                self._out('/FunctionType 2')
                self._out('/Domain [0.0 1.0]')
                self._out('/C0 [' + str(grad['col1']) + ']')
                self._out('/C1 [' + str(grad['col2']) + ']')
                self._out('/N 1')
                self._out('>>')
                self._out('endobj')
                f1=self.n

            self._newobj()
            self._out('<<')
            self._out('/ShadingType ' + str(grad['type']))
            self._out('/ColorSpace /DeviceRGB')
            if grad['type']==2:
                self._out('/Coords [%.3F %.3F %.3F %.3F]' % (grad['coords'][0],grad['coords'][1],grad['coords'][2],grad['coords'][3]))
                self._out('/Function ' + str(f1) + ' 0 R')
                self._out('/Extend [true true] ')
                self._out('>>')
            
            elif grad['type']==3:
                #x0, y0, r0, x1, y1, r1
                #at this time radius of inner circle is 0
                self._out('/Coords [%.3F %.3F 0 %.3F %.3F %.3F]' % (grad['coords'][0],grad['coords'][1],grad['coords'][2],grad['coords'][3],grad['coords'][4]))
                self._out('/Function ' + str(f1) + ' 0 R')
                self._out('/Extend [true true] ')
                self._out('>>')
            
            elif grad['type']==6:
                self._out('/BitsPerCoordinate 16')
                self._out('/BitsPerComponent 8')
                self._out('/Decode[0 1 0 1 0 1 0 1 0 1]')
                self._out('/BitsPerFlag 8')
                self._out('/Length ' + str(len(grad['stream'])))
                self._out('>>')
                self._putstream(grad['stream'])
            self._out('endobj')
            self._gradients[gradNo]['id']=self.n
        
    def _putstream(self, data):
        self._out('stream')
        self._out(data)
        self._out('endstream')

    def _putresourcedict(self):
        super()._putresourcedict()
        self._out('/Shading <<')
        for gradNo, grad in zip(self._gradients.keys(), self._gradients.values()):
             self._out('/Sh' + str(gradNo) + ' ' + str(grad['id']) + ' 0 R')
        self._out('>>')
    

    def _putresources(self):
        self._putshaders()
        super()._putresources()
 