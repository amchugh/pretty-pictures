from PIL import Image

TILE_SIZE = 16


def get_boundaries_by_pos(x, y=None):
    if y == None:
        y = x[1]
        x = x[0]
    left = x * TILE_SIZE
    top = y * TILE_SIZE
    return (left, top, left + TILE_SIZE, top + TILE_SIZE)


PLAIN = (2, 3)
SPACE = (4, 6)
FLOOR1 = (0, 2)
FLOOR2 = (1, 2)
FLOOR3 = (2, 2)
WALL1 = (0, 1)
WALL2 = (1, 1)
WALL3 = (2, 1)


def generate_tiles():
    tileset = Image.open("tileset.png")
    tiles = {}
    tiles["floor"] = tileset.crop(get_boundaries_by_pos(PLAIN))
    tiles["wall"] = tileset.crop(get_boundaries_by_pos(WALL2))
    tiles["space"] = tileset.crop(get_boundaries_by_pos(SPACE))
    return tiles


def image_from_array(arr):
    height = len(arr)
    width = len(arr[0])
    out = Image.new("RGB", (width * TILE_SIZE, height * TILE_SIZE), "purple")
    tiles = generate_tiles()

    for y in range(height):
        for x in range(width):
            el = arr[y][x]
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            if el == 1:
                # Draw a wall
                out.paste(tiles["floor"], pos)
            elif el == 2:
                out.paste(tiles["wall"], pos)
            elif el == 0:
                out.paste(tiles["space"], pos)

    out.save("out.png")


if __name__ == "__main__":
    arr = [[0, 0], [1, 2], [0, 0]]
    image_from_array(arr)
    # im = Image.open("tileset.png")
    # im = im.crop(get_boundaries_by_pos(WALL2))
    # im.save("out.png")
