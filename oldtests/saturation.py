# a project by me
import numpy as np
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]
amount = int(sys.argv[3])


with open(inFile, 'r') as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
header = content[:4]
pixels = content[4:]
width, height = int(content[2].split()[0]), int(content[2].split()[1])

"""
Builds a height x width Numpy array of tuples of the RGB values for each
corresponding pixel in the image, to be used in seam carving
"""
def build_grid(image_data, h, w):
    arr = np.empty((h, w), tuple)
    for i in range(h):
        for j in range(w):
            index = i * w * 3 + j * 3
            arr[i][j] = [int(image_data[index]), int(image_data[index + 1]), int(image_data[index + 2])]
    return arr

def lighten_shadows(image_data, intensity):
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

image = build_grid(pixels, height, width)
lighten_shadows(image, amount)
reprint(image)
