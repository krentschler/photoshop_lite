# Photoshop lite

## Overview
This project was made to showcase the ability to modify images by applying transformations on the image pixels. Images in a .ppm format have a text-based RGB value for each pixel. Utilizing the simple interpretability of this format, we can read the data into matrices which can then be modified and re-printed into a new image. I came up with the idea for this project after working on image rectification software for GM/Cruise Automation's autonomous Chevy Bolts in the summer of 2017.

The main goal of this project was to implement content-aware image resizing, or seam carving, from scratch to work on real images. Seam carving allows a user to re-scale an image by removing pixels with little added information (i.e. pixels that are very similar to their surrounding pixels) rather than "squish" all parts of the photo equally. This is most useful for images with a lot of empty space between objects.

I added a suite of other features as well to adjust other aspects of an image, and hope to add some more features at some point. Hence this project is called "Photoshop Lite", essentially a very bare-bones and rudimentary photoshop program that works by modifying images on a pixel-by-pixel basis.

### Features
* Seam Carving: smart rescaling of an image by removing lines of low-value pixels
* Lighten Shadows: Bring up the lightness of dark pixels in shaded areas
* Adjust Contrast: Increase the difference between light and dark borders
* Adjust Saturation: Increase or decrease the intensity and brightness of colors
* Watermark: Stamp a logo or text onto an existing image such that it is translucent and still shows the underlying parts of the image


### How to use
To run Photoshop Lite on an image, the image needs to be in .ppm format. You can convert almost all image types to .ppm using free tools such as GNU Imagine Manipulation ([GIMP](https://www.gimp.org/)). Additionally, some sample images in .ppm format are provided here to play with.

Documentation on how to call each program is below. See `demo.txt `for example calls on real files.

The program `processorSuite.py` can be run by calling `python3 processorSuite.py <EFFECT_NAME> <INPUT_FILE.ppm> <OUTPUT_FILE.ppm> <AMOUNT>` for effects lightenShadows, contrast, and saturate. Where amount is an integer from 0-255

The program `watermark.py` can be called by running `python3 watermark.py <TARGET_IMAGE.ppm> <WATERMARK_LOGO.ppm> <OUTPUT_FILE.ppm> <AMOUNT> <X_ALIGNMENT> <Y_ALIGNMENT>` where amount is an integer 0-255, and x and y alignment are integers greater than 0 and less than the pixel width and height of the input image, respectively. Note that the size (in pixels) of the watermark logo is how large it will appear on the target image.

The program `seamcarver.py` can be run by calling `python3 seamcarver.py <INPUT_FILE.ppm> <OUTPUT_FILE.ppm>`. This returns the image with a single seam removed (i.e. one pixel narrower in width). To do multiple pixels, write a shell loop with the same input and output file names. This will take time because the pixel heat map needs to be recomputed for each pass.
