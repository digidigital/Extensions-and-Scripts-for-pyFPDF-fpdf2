#!/usr/bin/python3
# Ported from PHP to Python and adapted for fpdf2 by Björn Seipel in 2021
# License:  LGPL v3.0+  
# based on the idea of
# http://www.fpdf.org/en/script/script83.php
# Author: Valentin Schmidt
# License: FPDF 


from fpdf import FPDF
from image_parsing import get_img_info, load_image, SUPPORTED_IMAGE_FILTERS

class PDFImageMask(FPDF):

    def image(
        self,
        name,
        x=None,
        y=None,
        w=0,
        h=0,
        type="",
        link="",
        title=None,
        alt_text=None,
        is_mask=False,
        mask_image=None
    ):
        """
        Put an image on the page.
        The size of the image on the page can be specified in different ways:
        * explicit width and height (expressed in user units)
        * one explicit dimension, the other being calculated automatically
          in order to keep the original proportions
        * no explicit dimension, in which case the image is put at 72 dpi.
        **Remarks**:
        * if an image is used several times, only one copy is embedded in the file.
        * when using an animated GIF, only the first frame is used.
        Args:
            name: either a string representing a file path to an #!/usr/bin/python3inate is used.
                After the call, the current ordinate is moved to the bottom of the image
            w (int): optional width of the image. If not specified or equal to zero,
                it is automatically calculated from the image size.
                Pass `pdf.epw` to scale horizontally to the full page width.
            h (int): optional height of the image. If not specified or equal to zero,
                it is automatically calculated from the image size.
                Pass `pdf.eph` to scale horizontally to the full page height.
            type (str): [**DEPRECATED**] unused, will be removed in a later version.
            link (str): optional link to add on the image, internal
                (identifier returned by `add_link`) or external URL.
            title (str): optional. Currently, never seem rendered by PDF readers.
            alt_text (str): optional alternative text describing the image,
                for accessibility purposes. Displayed by some PDF readers on hover.
                          
        """
        if type:
            warnings.warn(
                '"type" is unused and will soon be deprecated',
                PendingDeprecationWarning,
            )
        if isinstance(name, str):
            img = None
        elif isinstance(name, Image.Image):
            name, img = hashlib.md5(name.tobytes()).hexdigest(), name
        elif isinstance(name, io.BytesIO):
            name, img = hashlib.md5(name.getvalue()).hexdigest(), name
        else:
            name, img = str(name), name
        info = self.images.get(name)
        if info:
            info["usages"] += 1
        else:
            if not img:
                img = load_image(name)
            info = get_img_info(img, self.image_filter)
            info["i"] = len(self.images) + 1
            info["usages"] = 1
            self.images[name] = info

        if mask_image!=None:
            info['smask'] = self.images.get(mask_image)['data']
        # Set PDF Version to at least 1.4 to enable transparency
        if is_mask:
            if float(self.pdf_version) < 1.4:
                self.pdf_version='1.4'

        # Automatic width and height calculation if needed
        if w == 0 and h == 0:  # Put image at 72 dpi
            w = info["w"] / self.k
            h = info["h"] / self.k
        elif w == 0:
            w = h * info["w"] / info["h"]
        elif h == 0:
            h = w * info["h"] / info["w"]

        # workarount fpdf 2.4.5 in pip seems to be different from git version ???
        try:
            if self.oversized_images and info["usages"] == 1:
                info = self._downscale_image(name, img, info, w, h)
        except:
            pass

        # Flowing mode
        if y is None:
            self._perform_page_break_if_need_be(h)
            y = self.y
            self.y += h

        if x is None:
            x = self.x

        stream_content = (
            f"q {w * self.k:.2f} 0 0 {h * self.k:.2f} {x * self.k:.2f} "
            f"{(self.h - y - h) * self.k:.2f} cm /I{info['i']} Do Q"
        )
        
        if not is_mask:
            if title or alt_text:
                with self._marked_sequence(title=title, alt_text=alt_text):
                    self._out(stream_content)
            else:
                self._out(stream_content)
        if link:
            self.link(x, y, w, h, link)

        return info