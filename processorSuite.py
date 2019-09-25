import numpy as np
import sys
import time

#library called imagemagick

"""
Run the commands as follows:
python processorSuite.py [desired action] [inputFile.ppm] [outputName.ppm] [intensity]
Desired actions include contrast, lightenShadows, and saturation
"""

command = sys.argv[1]
inFile = sys.argv[2]
outFile = sys.argv[3]
amount = int(sys.argv[4])

"""
Reads the content from the input file into an array
"""
def readContent():
    with open(inFile, 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    header = content[:4]
    pixels = content[4:]
    width, height = int(content[2].split()[0]), int(content[2].split()[1])
    return pixels, width, height, header

"""
Builds a height x width Numpy array of tuples of the RGB values for each
corresponding pixel in the image, to be used in seam carving
"""
def buildGrid(image_data, h, w):
    arr = np.empty((h, w), tuple)
    for i in range(h):
        for j in range(w):
            index = i * w * 3 + j * 3
            arr[i][j] = [int(image_data[index]), int(image_data[index + 1]), int(image_data[index + 2])]
    return arr

def changeContrast(image_data, intensity):
    for i in range(height):
        for j in range(width):
            if image_data[i][j][0] + image_data[i][j][1] + image_data[i][j][2] < 200:
                for color in range(3):
                    image_data[i][j][color] -= intensity
                    if image_data[i][j][color] < 0:
                        image_data[i][j][color] = 0
            elif image_data[i][j][0] + image_data[i][j][1] + image_data[i][j][2] > 400:
                for color in range(3):
                    image_data[i][j][color] += intensity
                    if image_data[i][j][color] > 255:
                        image_data[i][j][color] = 255

def greyscale(image_data):
    for i in range(height):
        for j in range(width):
            average = (image_data[i][j][0] + image_data[i][j][1] + image_data[i][j][2])//3
            for color in range(len(image_data[i][j])):
                image_data[i][j][color] = average

def lightenShadows(image_data, intensity):
    for i in range(height):
        for j in range(width):
            if image_data[i][j][0] + image_data[i][j][1] + image_data[i][j][2] < 200:
                for color in range(3):
                    image_data[i][j][color] += intensity
                    if image_data[i][j][color] < 0:
                        image_data[i][j][color] = 0

def saturate(image_data, intensity):
    for i in range(height):
        for j in range(width):
            if image_data[i][j][0] + image_data[i][j][1] + image_data[i][j][2] < 640:
                max_color = 0
                max_val = 0
                for color in range(3):
                    if image_data[i][j][color] > max_val:
                        max_val = image_data[i][j][color]
                        max_color = color
                image_data[i][j][max_color] += intensity

"""
Saves the output image in .ppm format to [outputName.ppm]
"""
def reprint(grid):
    with open(outFile,'w') as o:
        o.write(header[0] + "\n")
        o.write(header[1] + "\n")
        dimensions = str(width) + " " + str(height)
        o.write(dimensions + "\n")
        o.write("255" + "\n")
        for i in range(height):
            for j in range(width):
                o.write(str(grid[i][j][0]) + "\n")
                o.write(str(grid[i][j][1]) + "\n")
                o.write(str(grid[i][j][2]) + "\n")


pixels, width, height, header = readContent()
print("done reading", time.clock())
image = buildGrid(pixels, height, width)
print("done building grid", time.clock())
if command == "contrast":
    changeContrast(image, amount)
if command == "lightenShadows":
    lightenShadows(image, amount)
if command == "saturate":
    saturate(image, amount)
if command == "grey":
    greyscale(image)
print("done applying effect", time.clock())
reprint(image)
print("done saving", time.clock())
