# Extensions / Scripts for pyFPDF (fpdf2)

This repository contains some of the original [FPDF PHP Scripts](http://fpdf.org/en/script/) scripts that were ported to Python to be used in conjunction with fpdf2.

**Scripts**
* [Alpha / Transparency](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/blob/main/README.md#alpha--transparency-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/alpha)
* [Transform & Circular Text](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/blob/main/README.md#transform--circular-text-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/transform) 
* [Diagrams](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#diagrams-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/diagrams)
* [Javascript support](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#embed-javascript-in-pdf-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/javascript)
* [Rectangles with rounded corners](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#rectangle-with-rounded-corners-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/roundedCorners)
* [Draw segments of circles](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#sectors-of-circle-shapes-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/sector)
* [Draw star shapes](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#star-shape-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/star)
* [Restrict elements to be displayed on screen / printed only](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2#visibility-feature-for-pyfpdf-fpdf2) -> [Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/visibility)

# Alpha / Transparency for pyFPDF (fpdf2)
This script adds transparency support to pyFPDF. You can set the alpha channel from 0 (fully transparent) to 1 (fully opaque). It applies to all elements (text, drawings, images). 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example
![Transparent text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/alpha/result.jpg)

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/alpha/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/alpha)

# Transform & Circular Text for pyFPDF (fpdf2)
This script adds transfromation featurea ans support for circular text to pyFPDF. 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example
![Transform, rotate, shear, mirror text, images and drawings in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/transform/transform.jpg)

![Circular round text in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/transform/circular_text.jpg)

[PDF file](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/transform/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/transform) 

# Diagrams for pyFPDF (fpdf2)
Draw pie charts and bar diagrams with this script. 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Pie charts and bar diagrams with pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/diagrams/demo.jpg)

[PDF file](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/diagrams/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/diagrams)

# Embed Javascript in PDF for pyFPDF (fpdf2)
This script allows to embed JavaScript inside the PDF. The code is executed when the document is opened.

The Acrobat JavaScript reference is available [here](https://opensource.adobe.com/dc-acrobat-sdk-docs/acrobatsdk/).

**Note: Support depends on the PDF viewer and security settings.** 

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![PDF File](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/javascript/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/javascript)

# Rectangle with rounded corners for pyFPDF (fpdf2)
Draw rectangles with rounded corners

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example
![Draw a rectangle with rounded corners in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/roundedCorners/demo.jpg)

[PDF file](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/roundedCorners/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/roundedCorners)

# Sectors of circle shapes for pyFPDF (fpdf2)
This script allows to draw segments of a circle. It can be used to render a pie chart.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example

![Pie charts in pyFPDF](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/sector/demo.jpg)

[PDF file](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/sector/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/sector)

# Star shape for pyFPDF (fpdf2)
This script draws a star.

Tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Example
![Star shapes](https://raw.githubusercontent.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/main/star/demo.jpg)

[PDF file](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/raw/main/star/demo.pdf)

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/star)

# Visibility feature for pyFPDF (fpdf2)
This script allows to restrict the rendering of some elements to screen or printout. This can be useful, for instance, to put a background image or color that will show on screen but won't print.

**Note: this feature is not supported by all PDF viewers.** 

Some Test on Ubuntu 20.04: 
- Chromium 94.0.4606.81 (Works as intended)
- Google Chrome 94.0.4606.81 (Works as intended)
- Evince 3.36.10 (Does not display content marked for screen display, but displays content marked for printing)   
- Okular 21.08.2 (Same result as for Evince)
- Firefox 93.0 (Ignores restrictions and displays all content)

Script was tested with fpdf2 2.4.5, Pillow 8.3.1, Python 3.8.10

## Get the code
[Code](https://github.com/digidigital/Extensions-and-Scripts-for-pyFPDF-fpdf2/tree/main/visibility)
