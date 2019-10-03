"""
sources:
http://www.faculty.idc.ac.il/arik/SCWeb/imret/imret.pdf
https://en.wikipedia.org/wiki/Seam_carving
"""
import numpy as np
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]
cut_number = int(sys.argv[3])
with open(inFile, 'r') as f:
    content = f.readlines()
content = [x.strip() for x in content]


header = content[:4]
pixels = content[4:]
width, height = int(content[2].split()[0]), int(content[2].split()[1])

"""
Builds a height x width Numpy array of tuples of the RGB values for each
corresponding pixel in the image, to be used in seam carving
"""
def build_grid():
    arr = np.empty((height, width), tuple)
    for i in range(height):
        for j in range(width):
            index = i * width * 3 + j * 3
            arr[i][j] = ((int(pixels[index]), int(pixels[index + 1]), int(pixels[index + 2])))
    return arr

def compute_energies(grid):
    energies = np.empty((height, width), int)
    for i in range(height):
        for j in range(width):
            if j + 1 >= width:
                right_index = 0
            else:
                right_index = j + 1
            left_rgb_tup = grid[i][j-1]
            right_rgb_tup = grid[i][right_index]
            delta_x = (left_rgb_tup[0] - right_rgb_tup[0])**2 + \
                        (left_rgb_tup[1] - right_rgb_tup[1])**2 + \
                        (left_rgb_tup[2] - right_rgb_tup[2])**2
            if i + 1 >= height:
                bottom_index = 0
            else:
                bottom_index = i + 1
            top_rgb_tup = grid[i-1][j]
            bottom_rgb_tup = grid[bottom_index][j]
            delta_y = (top_rgb_tup[0] - bottom_rgb_tup[0])**2 + \
                        (top_rgb_tup[1] - bottom_rgb_tup[1])**2 + \
                        (top_rgb_tup[2] - bottom_rgb_tup[2])**2
            energies[i][j] = delta_x + delta_y
    return energies

def compute_cost_matrix(energy_grid):
    M = np.empty((height, width), int)
    prev = np.empty((height, width), tuple)
    #initializes bottom row to all zeroes
    for j in range(width):
        M[0][j] = energy_grid[0][j]
    for i in range(1, height):
        for j in range(width):
            if j == 0:
                middle = M[i-1][j]
                right = M[i-1][j+1]
                if min(middle, right) == middle:
                    prev[i,j] = (i-1, j)
                    M[i,j] = energy_grid[i,j] + middle
                else:
                    prev[i,j] = (i-1, j+1)
                    M[i,j] = energy_grid[i,j] + right
            elif j == width - 1:
                middle = M[i-1][j]
                left = M[i-1][j-1]
                if min(left, middle, right) == middle:
                    prev[i,j] = (i-1, j)
                    M[i,j] = energy_grid[i,j] + middle
                else:
                    prev[i,j] = (i-1, j-1)
                    M[i,j] = energy_grid[i,j] + left
            else:
                left = M[i-1][j-1]
                middle = M[i-1][j]
                right = M[i-1][j+1]
                if min(left, middle, right) == middle:
                    prev[i,j] = (i-1, j)
                    M[i,j] = energy_grid[i,j] + middle
                elif left < right:
                    prev[i,j] = (i-1, j-1)
                    M[i,j] = energy_grid[i,j] + left
                else:
                    prev[i,j] = (i-1, j+1)
                    M[i,j] = energy_grid[i,j] + right
    return M, prev

"""
Identifies n unique vertical seams that can be removed from the image.
These are stored in a returned list of dictionaries where the ith item
in the list contains a dictionary, where the keys correspond to the (i,k)
pixels we would like to remove.
"""
def find_vertical_seams(costs, previous, n):
    starting_pixels = {}
    for j in range(width):
        starting_pixels[j] = costs[height-1][j]
    priority = []
    for key in sorted(starting_pixels, key=starting_pixels.get):
        priority.append(key)
    end_queue = list(reversed(priority))
    print("end queue: ", end_queue)
    taken_pixels = []
    for i in range(height):
        taken_pixels.append({})
    # this loop ensures we find n complete seams
    for seam in range(n):
        finished = False
        while not finished:
            start = end_queue.pop()
            path = [start]
            p = previous[height-1][start]
            print("height: ", height)
            curr_row = height - 1
            while p is not None:
                curr_row -= 1
                print("row: ", curr_row)
                if p[1] in taken_pixels[curr_row]:
                    #print("row: ", curr_row)
                    print("exited")
                    break
                path.append(p[1])
                print("appended ", p[1])
                print("path: ", path)
                p = previous[p[0]][p[1]]
            if len(path) == height:
                finished = True
                true_path = list(reversed(path))
                for i in range(height):
                    taken_pixels[height-1-i][path[i]] = True
            print("blacklist: ", taken_pixels)


    # for
    # end = None
    # min_val = float("inf")
    # for j in range(width):
    #     val = M[height-1][j]
    #     if val < min_val:
    #         min_val = val
    #         end = j
    # p = prev[height-1][end]
    # ret_list = [end]
    # while p is not None:
    #     ret_list.append(p[1])
    #     p = prev[p[0]][p[1]]
    # return list(reversed(ret_list))

def reprint(grid, blacklist, n):
    print("passed in list: ", blacklist)
    with open(outFile,'w') as o:
        o.write(header[0] + "\n")
        o.write(header[1] + "\n")
        dimensions = str(width - n) + " " + str(height)
        o.write(dimensions + "\n")
        o.write("255" + "\n")
        for i in range(height):
            for j in range(width):
                if j not in blacklist[i]:
                    o.write(str(grid[i][j][0]) + "\n")
                    o.write(str(grid[i][j][1]) + "\n")
                    o.write(str(grid[i][j][2]) + "\n")
G = build_grid()
E = compute_energies(G)
DP, prevs = compute_cost_matrix(E)
print("M: ", DP)
print("previous: ", prevs)
B = find_vertical_seams(DP, prevs, cut_number)
reprint(G, B, cut_number)
