# !/usr/bin/env python3

from PDFTransform import PDFTransform as FPDF 

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica','B',12)

#Scaling
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(25, 20, 40, 10, 'D')
pdf.text(25, 34, 'pdf.scale_xy(percent, center_x, center_y)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#pdf.scale_xy(150, 25, 30) by 150% centered by (50,30) which is the lower left corner of the rectangle
pdf.scale_xy(150, 25, 30)
pdf.rect(25, 20, 40, 10, 'D')
pdf.text(25, 19, 'pdf.scale_xy(150, 50, 30)')
#Stop Transformation
pdf.stop_transform()

#Translation
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 20, 40, 10, 'D')
pdf.text(125, 19, 'pdf.translate(horizontal, vertical)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#Translate 7 to the right, 5 to the bottom
pdf.translate(7, 5)
pdf.rect(125, 20, 40, 10, 'D')
pdf.text(125, 19, 'pdf.translate(7, 5)')
#Stop Transformation
pdf.stop_transform()

#Rotation
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(25, 50, 40, 10, 'D')
pdf.text(25, 64, 'pdf.t_rotate(degrees, center_x, center_y')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#t_rotate 20 degrees counter-clockwise centered by (50,60) which is the lower left corner of the rectangle
pdf.t_rotate(15, 25, 60)
pdf.rect(25, 50, 40, 10, 'D')
pdf.text(25, 49, 'pdf.t_rotate(20, 50, 60)')
#Stop Transformation
pdf.stop_transform()

#Skewing
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 50, 40, 10, 'D')
pdf.text(125, 64, 'pdf.skew_x(degrees,by_x, by_y)')
pdf.text(125, 69, 'pdf.skew_y(degrees,by_x, by_y)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#skew 30 degrees along the x-axis centered by (125,60) which is the lower left corner of the rectangle
pdf.skew_x(30, 125, 60)
pdf.rect(125, 50, 40, 10, 'D')
pdf.text(125, 49, 'pdf.skew_x(30, 125, 60)')
#Stop Transformation
pdf.stop_transform()

#Mirroring horizontally
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(50, 80, 40, 10, 'D')
pdf.text(50, 79, 'pdf.mirror_h(x_of_axis)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror horizontally with axis of reflection at x-position 50 (left side of the rectangle)
pdf.mirror_h(50)
pdf.rect(50, 80, 40, 10, 'D')
pdf.text(50, 79, 'pdf.mirror_h(50)')
#Stop Transformation
pdf.stop_transform()

#Mirroring vertically
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 80, 40, 10, 'D')
pdf.text(125, 79, 'pdf.mirror_v(y_of_axis)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror vertically with axis of reflection at y-position 90 (bottom side of the rectangle)
pdf.mirror_v(90)
pdf.rect(125, 80, 40, 10, 'D')
pdf.text(125, 79, 'pdf.mirror_v(90)')
#Stop Transformation
pdf.stop_transform()

#Point reflection
pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(50, 110, 40, 10, 'D')
pdf.text(50, 109, 'pdf.mirror_p(x_of_point,y_of_point)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#point reflection at the lower left point of rectangle
pdf.mirror_p(50,120)
pdf.rect(50, 110, 40, 10, 'D')
pdf.text(50, 109, 'pdf.mirror_p(50,120)')
#Stop Transformation
pdf.stop_transform()

#Mirroring against a straigth line described by a point (120, 120) and an angle -20°
angle=-20
px=120
py=120

#just vor visualisation: the straight line to mirror against
pdf.set_draw_color(200)
pdf.line(px-1,py-1,px+1,py+1)
pdf.line(px-1,py+1,px+1,py-1)
pdf.start_transform()
pdf.t_rotate(angle, px, py)
pdf.line(px-5, py, px+60, py)
pdf.stop_transform()

pdf.set_draw_color(200)
pdf.set_text_color(200)
pdf.rect(125, 110, 40, 10, 'D')
pdf.text(125, 109, 'pdf.mirror_l(angle, px, py)')
pdf.set_draw_color(0)
pdf.set_text_color(0)
#Start Transformation
pdf.start_transform()
#mirror against the straight line
pdf.mirror_l(angle, px, py)
pdf.rect(125, 110, 40, 10, 'D')
pdf.text(125, 109, 'pdf.mirror_l(-20, 120, 120)')
#Stop Transformation
pdf.stop_transform()

# circular text
pdf.add_page()
pdf.set_font('Helvetica','B',32)

text='Circular Text'
pdf.circular_text(105, 50, 35, text, 'top')
pdf.circular_text(105, 50, 35, text, 'bottom')

pdf.set_line_width(2)
pdf.set_draw_color(r=230, g=30, b=180)
pdf.set_fill_color(210)

pdf.ellipse(x=63, y=108, w=85, h=85, style="FD")
pdf.set_font(size=13)

pdf.circular_text(105, 150, 40, "pdf.circular_text(105, 50, 30, text, 'top')", 'top')
pdf.circular_text(105, 150, 40, "pdf.circular_text(105, 150, 30, text, 'bottom')", 'bottom')

pdf.text(15, 220, 'pdf.circular_text(float x, float y, float r, str text [, str align [, float kerning [, float fontwidth]]])')

pdf.output("./demo.pdf")

