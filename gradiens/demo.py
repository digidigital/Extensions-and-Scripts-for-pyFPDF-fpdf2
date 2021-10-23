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


