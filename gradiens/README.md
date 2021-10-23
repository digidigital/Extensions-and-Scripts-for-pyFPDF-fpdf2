# Linear, radial and multi-color gradients for pyFPDF (fpdf2)
Paints linear and radial gradients as well as multi-color gradients (coons patch meshes) inside a rectangle.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Linear and radial gradients in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/gradiens/demo_page_1.png)
![Multi-color gradients in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/gradiens/demo_page_2.png)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/gradiens/demo.pdf)

## Usage

Just put PDFGradients.py in your project directory

```python
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
```

Import the script and use pyFPDF as usual.

**linear_gradient(float x, float y, float w, float h, list col1, list col2 \[, list coords])**
* x: abscissa of the top left corner of the rectangle.
* y: ordinate of the top left corner of the rectangle.
* w: width of the rectangle.
* h: height of the rectangle.
* col1: first color (RGB components). Can be a list with one or three values between 0 and 255
* col2: second color (RGB components). Can be a list with one or three values between 0 and 255
* coords: list of the form (x1, y1, x2, y2) which defines the gradient vector (see linear_gradient_coords.jpg). The default value is from left to right (x1=0, y1=0, x2=1, y2=0).

![Linear gradient coords](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/gradiens/linear_gradient_coords.jpg)



**radial_gradient(float x, float y, float w, float h, list col1, list col2 \[, list coords])**
* x: abscissa of the top left corner of the rectangle.
* y: ordinate of the top left corner of the rectangle.
* w: width of the rectangle.
* h: height of the rectangle.
* col1: first color (RGB components). Can be a list with one or three values between 0 and 255
* col2: second color (RGB components). Can be a list with one or three values between 0 and 255
* coords: list of the form (fx, fy, cx, cy, r) where (fx, fy) is the starting point of the gradient with color1, (cx, cy) is the center of the circle with color2, and r is the radius of the circle (see radial_gradient_coords.jpg). (fx, fy) should be inside the circle, otherwise some areas will not be defined.

![radial gradient coords](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/gradiens/radial_gradient_coords.jpg)



**coons_patch_mesh(float x, float y, float w, float h, list col1, list col2, list col3, list col4 \[, list coords \[, float coords_min \[, float coords_max]]])**
* x: abscissa of the top left corner of the rectangle.
* y: ordinate of the top left corner of the rectangle.
* w: width of the rectangle.
* h: height of the rectangle.
* col1: first color (lower left corner) (RGB components). Can be a list with one or three values between 0 and 255
* col2: second color (lower right corner) (RGB components). Can be a list with one or three values between 0 and 255
* col3: third color (upper right corner) (RGB components). Can be a list with one or three values between 0 and 255
* col4: fourth color (upper left corner) (RGB components). Can be a list with one or three values between 0 and 255
*coords:

![coons patch mesh coords](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/gradiens/coons_patch_mesh_coords.jpg)

### for one patch mesh

* **list\[float x1, float y1, .... float x12, float y12])**: 12 pairs of coordinates (normally from 0 to 1) which specify the Bézier control points that define the patch. First pair is the lower left edge point, next is its right control point (control point 2). Then the other points are defined in the order: control point 1, edge point, control point 2 going counter-clockwise around the patch. Last (x12, y12) is the first edge point's left control point (control point 1).

### or two or more patch meshes

* **dict{int patchnumber:dict patch , ... }**
 where "dict patch" is a dict with the following keys / values for each patch:
* **dict{'f':int , 'points':list, 'colors':list}**
* f: where to put that patch (0 = first patch, 1, 2, 3 = right, top and left of precedent patch - I didn't figure this out completely - just trial and error ;-)
* points: 12 pairs of coordinates of the Bézier control points as above for the first patch, 8 pairs of coordinates for the following patches, ignoring the coordinates already defined by the precedent patch (I also didn't figure out the order of these - also: try and see what's happening)
* colors: must be a list of 4 colors for the first patch, 2 colors for the following patches where each color is defined in a **dict{'r':int,'g':int,'b':int}**

* coords_min: minimum value used by the coordinates. If a coordinate's value is smaller than this it will be cut to coords_min. default: 0
* coords_max: maximum value used by the coordinates. If a coordinate's value is greater than this it will be cut to coords_max. default: 1 

```python
# !/usr/bin/env python3

from PDFGradients import PDFGradients as FPDF 

pdf = FPDF()

#first page
pdf.add_page()
pdf.set_font('Helvetica','',14)
pdf.cell(0,5,'Page 1',0,1,'C')
pdf.ln()

#set colors for gradients (r,g,b) or (grey 0-255)
red=[255,0,0]
blue=[0,0,200]
yellow=[255,255,0]
green=[0,255,0]
white=[255]
black=[0]

#set the coordinates x1,y1,x2,y2 of the gradient (see linear_gradient_coords.jpg)
coords=[0,0,1,0]

#paint a linear gradient
pdf.linear_gradient(20,25,80,80,blue,red,coords)

#set the coordinates fx,fy,cx,cy,r of the gradient (see radial_gradient_coords.jpg)
coords=[0.5,0.5,1,1,1.2]

#paint a radial gradient
pdf.radial_gradient(110,25,80,80,white,black,coords)

#paint a coons patch mesh with default coordinates
pdf.coons_patch_mesh(20,115,80,80,yellow,blue,green,red)

#set the coordinates for the cubic Bézier points x1,y1 ... x12, y12 of the patch (see coons_patch_mesh_coords.jpg)
coords=[0.00,0.00, 0.33,0.20,             #lower left
        0.67,0.00, 1.00,0.00, 0.80,0.33,  #lower right
        0.80,0.67, 1.00,1.00, 0.67,0.80,  #upper right
        0.33,1.00, 0.00,1.00, 0.20,0.67,  #upper left
        0.00,0.33]                        #lower left
coords_min=0   #minimum value of the coordinates
coords_max=1   #maximum value of the coordinates

#paint a coons patch gradient with the above coordinates 
pdf.coons_patch_mesh(110,115,80,80,yellow,blue,green,red,coords,coords_min,coords_max)

#second page
pdf.add_page()
pdf.cell(0,5,'Page 2',0,1,'C')
pdf.ln()

#first patch: f = 0
patch_list={}
patch_list[0]={}
patch_list[0]['f']=0
patch_list[0]['points']=[0.00,0.00, 0.33,0.00,
                        0.67,0.00, 1.00,0.00, 1.00,0.33,
                        0.8,0.67, 1.00,1.00, 0.67,0.8,
                        0.33,1.80, 0.00,1.00, 0.00,0.67,
                        0.00,0.33]
patch_list[0]['colors']=({'r':255,'g':255,'b':0},
                         {'r':0,'g':0,'b':255},
                         {'r':0,'g':255,'b':0},
                         {'r':255,'g':0,'b':0})

#second patch - above the other: f = 2
patch_list[1]={}
patch_list[1]['f']=2
patch_list[1]['points']=[0.00,1.33,
                        0.00,1.67, 0.00,2.00, 0.33,2.00,
                        0.67,2.00, 1.00,2.00, 1.00,1.67,
                        1.5,1.33]
patch_list[1]['colors']=({'r':0,'g':0,'b':0},
                         {'r':255,'g':0,'b':255})

#third patch - right of the above: f = 3
patch_list[2]={}
patch_list[2]['f']=3
patch_list[2]['points']=[1.33,0.80,
                        1.67,1.50, 2.00,1.00, 2.00,1.33,
                        2.00,1.67, 2.00,2.00, 1.67,2.00,
                        1.33,2.00]
patch_list[2]['colors']=({'r':0,'g':255,'b':255},
                         {'r':0,'g':0,'b':0})

#fourth patch - below the above, which means left(?) of the above: f = 1
patch_list[3]={}
patch_list[3]['f']=1
patch_list[3]['points']=[2.00,0.67,
                        2.00,0.33, 2.00,0.00, 1.67,0.00,
                        1.33,0.00, 1.00,0.00, 1.00,0.33,
                        0.8,0.67]
patch_list[3]['colors']=({'r':0,'g':0,'b':0},
                         {'r':0,'g':0,'b':255})

coords_min=0
coords_max=2

pdf.coons_patch_mesh(10,25,190,200,[],[],[],[],patch_list,coords_min,coords_max)

pdf.output('demo.pdf')
```
