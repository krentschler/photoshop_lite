# a project by me
import numpy as np
import sys
inFile = sys.argv[1]
markFile = sys.argv[2]
outFile = sys.argv[3]
opacity = int(sys.argv[4])
starting_row = int(sys.argv[5])
starting_col = int(sys.argv[6])


with open(inFile, 'r') as f:
    content = f.readlines()

with open(markFile, 'r') as f:
    mark = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
mark = [x.strip() for x in mark]

mark_pixels = mark[4:]
mark_width, mark_height = int(mark[2].split()[0]), int(mark[2].split()[1])

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

def apply_mark(original, stamp, origin):
    for i in range(stamp.shape[0]):
        for j in range(stamp.shape[1]):
            if stamp[i][j][0] + stamp[i][j][1] + stamp[i][j][2] < 100:
                for color in range(3):
                    original[i + origin[0]][j + origin[1]][color] += opacity
                    if original[i + origin[0]][j + origin[1]][color] > 255:
                        original[i + origin[0]][j + origin[1]][color] = 255

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
M = build_grid(mark_pixels, mark_height, mark_width)
apply_mark(image, M, (starting_row,starting_col))
reprint(image)
