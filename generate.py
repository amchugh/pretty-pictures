from gen_image import *
import random
import numpy as np
import time

MAX_ENTROPY = 3

arr = [
    [0, 2, 0],
    [2, 1, 2],
    [0, 2, 0],
]

# image_from_array(arr)


def lowest_entropy(g):
    lowest = MAX_ENTROPY + 1
    lowest_place = (0, 0)
    for y, row in enumerate(g):
        for x, el in enumerate(row):
            if type(el) == int:
                continue
            if len(el) < lowest:
                lowest = len(el)
                lowest_place = (x, y)
    return lowest_place


def collapse(grid, sel):
    possible = grid[sel[1]][sel[0]]
    grid[sel[1]][sel[0]] = random.choice(possible)


def update(grid, sel):
    # look in the four directions
    x, y = sel[0], sel[1]
    height = len(grid)
    width = len(grid[0])
    if grid[y][x] == 0:
        # Need to remove the 2's
    elif grid[y][x] == 2:
        # Need to remove the 0's
    # Don't need to do anything for 1's

# grid = [[[[0, 1, 2]] * 3], [[[0, 1, 2]] * 3], [[[0, 1, 2]] * 3]]
tmp = np.array([[0, 1, 2] * 9])
print(tmp)
grid = tmp.reshape((3, 3, 3))
grid = grid.tolist()
print(grid)

for i in range(9):
    # Find the next piece to condense
    sel = lowest_entropy(grid)
    # Decide of a value for it
    collapse(grid, sel)
    update(grid, sel)
    print(f"Collapsed {sel} to {grid[sel[1]][sel[0]]}")
    image_from_array(grid)
    time.sleep(1)

# print(grid)
