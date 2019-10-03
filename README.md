# Photoshop lite

## Overview
This project was made to showcase the ability to modify images by applying transformations on the image pixels. Images in a .ppm format have a text-based RGB value for each pixel. This program utilizes the simple interpretability of that format to read the data into matrices, which can then be modified and re-printed into a new image. I came up with the idea for this project after working on image rectification software for GM/Cruise Automation's autonomous Chevy Bolts in the summer of 2017.

### How to use
To run Photoshop Lite on an image, the image needs to be in .ppm format. You can convert almost all image types to .ppm using free tools such as GNU Imagine Manipulation ([GIMP](https://www.gimp.org/)). Additionally, some sample images in .ppm format are provided here to play with.

Documentation on how to call each program is below. See `demo.txt `for example calls on real files.

The program `processorSuite.py` can be run by calling `python3 processorSuite.py <EFFECT_NAME> <INPUT_FILE.ppm> <OUTPUT_FILE.ppm> <AMOUNT>` for effects lightenShadows, contrast, and saturate. Where amount is an integer from 0-255

The program `watermark.py` can be called by running `python3 watermark.py <TARGET_IMAGE.ppm> <WATERMARK_LOGO.ppm> <OUTPUT_FILE.ppm> <AMOUNT> <X_ALIGNMENT> <Y_ALIGNMENT>` where amount is an integer 0-255, and x and y alignment are integers greater than 0 and less than the pixel width and height of the input image, respectively. Note that the size (in pixels) of the watermark logo is how large it will appear on the target image.

The program `seamcarver.py` can be run by calling `python3 seamcarver.py <INPUT_FILE.ppm> <OUTPUT_FILE.ppm>`. This returns the image with a single seam removed (i.e. one pixel narrower in width). To do multiple pixels, write a shell loop with the same input and output file names. This will take time because the pixel heat map needs to be recomputed for each pass.
