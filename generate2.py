import random
import gen_image
import copy
import time
import numpy as np

width = 20
height = 20

# grid = [
#     [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
#     [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
#     [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
# ]

tmp = np.array([[0, 1, 2] * width * height])
grid = tmp.reshape((height, width, 3))
grid = grid.tolist()

rules = {
    0: {
        "left": [0, 2],
        "right": [0, 2],
        "up": [0, 2],
        "down": [0, 2],
    },
    1: {
        "left": [2, 1],
        "right": [2, 1],
        "up": [2, 1],
        "down": [2, 1],
    },
    2: {
        "left": [0, 1, 2],
        "right": [0, 1, 2],
        "up": [0, 1, 2],
        "down": [0, 1, 2],
    },
}


def is_tile_valid(x, y):
    if x < 0 or x >= width:
        return False
    return not (y < 0 or y >= height)


def update_grid(x, y, newval, direction):
    if is_tile_valid(x, y):
        rule = rules[newval][direction]
        updated = False
        for possible in grid[y][x]:
            if possible not in rule:
                grid[y][x].remove(possible)
                updated = True
        if updated:
            # We also need to push this to neighboring tiles!
            update_grid(x, y, newval, direction)


def update_possibilities(x, y, acceptable_values):
    updated = False
    if is_tile_valid(x, y):
        vals = grid[y][x]
        if type(vals) == int:
            # We already assigned this tile
            if vals not in acceptable_values:
                print("Found a contradiction!", vals, acceptable_values, x, y)
                return False, False
            return False, True
        for val in grid[y][x]:
            if val not in acceptable_values:
                grid[y][x].remove(val)
                updated = True
    return updated, True


def find_possibilities(x, y, direction):
    possibles = grid[y][x]
    if type(possibles) == int:
        # It's collapsed, so we only look at one
        return rules[possibles][direction]
    else:
        ret = []
        for p in possibles:
            for_val = rules[p][direction]
            for v in for_val:
                if v not in ret:
                    ret.append(v)
        return ret


def update_from_pos(selx, sely):
    also_update_from = []
    if is_tile_valid(selx - 1, sely):
        ps = find_possibilities(selx, sely, "left")
        updated, ok = update_possibilities(selx - 1, sely, ps)
        if not ok:
            return False
        if updated:
            also_update_from.append((selx - 1, sely))
    if is_tile_valid(selx + 1, sely):
        ps = find_possibilities(selx, sely, "right")
        updated, ok = update_possibilities(selx + 1, sely, ps)
        if not ok:
            return False
        if updated:
            also_update_from.append((selx + 1, sely))
    if is_tile_valid(selx, sely - 1):
        ps = find_possibilities(selx, sely, "up")
        updated, ok = update_possibilities(selx, sely - 1, ps)
        if not ok:
            return False
        if updated:
            also_update_from.append((selx, sely - 1))
    if is_tile_valid(selx, sely + 1):
        ps = find_possibilities(selx, sely, "down")
        updated, ok = update_possibilities(selx, sely + 1, ps)
        if not ok:
            return False
        if updated:
            also_update_from.append((selx, sely + 1))

    for pos in also_update_from:
        if not update_from_pos(pos[0], pos[1]):
            return False

    return True


# Push this to all neighboring tiles
# update_grid(selx - 1, sely, newval, "left")
# update_grid(selx + 1, sely, newval, "right")
# update_grid(selx, sely - 1, newval, "up")
# update_grid(selx, sely + 1, newval, "down")
# print(find_possibilities(0, 1, "up"))


def set_tile(x, y, val):
    global grid
    grid[y][x] = val
    update_from_pos(x, y)


# set_tile(1, 1, 2)
# set_tile(0, 0, 2)
# set_tile(2, 2, 2)


def is_complete():
    for row in grid:
        for val in row:
            if type(val) != int:
                return False
    return True


MAX_ENTROPY = 3


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


print(grid)
fails = 0
while not is_complete():
    # Pick a random unfilled position
    # rx = random.randint(0, width - 1)
    # ry = random.randint(0, height - 1)
    # while type(grid[ry][rx]) == int:
    #     rx = random.randint(0, width - 1)
    #     ry = random.randint(0, height - 1)
    p = lowest_entropy(grid)
    rx, ry = p[0], p[1]
    # Now, set that position to a random value from it's acceptable
    selected = random.choice(grid[ry][rx])
    # print(f"Setting {rx},{ry} to {selected}")
    tempgrid = copy.deepcopy(grid)
    grid[ry][rx] = selected
    ok = update_from_pos(rx, ry)
    # If that didn't go well, restore
    if not ok:
        print(f"Failed to set {rx},{ry} to {selected}.")
        grid = tempgrid
        fails += 1
        if fails == 10:
            break
        # break
        # print("Resetting due to contradiction")
        # print(grid)
    else:
        # gen_image.image_from_array(grid)
        # time.sleep(0.2)
        pass

gen_image.image_from_array(grid)
print(grid)
