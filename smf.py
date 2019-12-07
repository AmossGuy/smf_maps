#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageChops
from pathlib import Path
from sys import argv
import csv

myfolder = Path(argv[0]).resolve().parent

csvpath = myfolder / Path(input("Path to CSV file (relative to the directory this script is in): "))

with open(csvpath, "r") as csvfile:
    level = []
    reader = csv.reader(csvfile)
    for i in reader:
        level.append(list(map(int, i)))

tile_size = 16

sprites = {
    61: ("goomba", 0, 1, False),
    66: ("koopa", 0, -7, False),
    70: ("piranha", 8, -7, True),
    72: ("piranha", 0, -7, True)
}

spritestoadd = []

image = Image.new("RGBA", (len(level[0]) * 16, len(level) * 16), None)
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
for y in range(len(level)):
    for x in range(len(level[y])):
        if level[y][x] in sprites:
            sprite = myfolder / (sprites[level[y][x]][0] + ".png")
            pos = (x * tile_size + sprites[level[y][x]][1], y * tile_size + sprites[level[y][x]][2])
            spritestoadd.append((sprite, pos, sprites[level[y][x]][3]))
        else:
            tile = myfolder / (str(level[y][x]) + ".png")
            pos = (x * tile_size, y * tile_size)
            if tile.exists():
                image.paste(Image.open(tile), pos)
            else:
                draw.text(pos, str(level[y][x]), font=font)

for i in spritestoadd:
    j = Image.open(i[0])
    if i[2]:
        topleft = i[1]
        size = j.size
        mask = ImageChops.invert(image.convert("RGBA").crop((topleft[0], topleft[1], topleft[0]+size[0], topleft[1]+size[1])))
    else:
        mask = j.convert("RGBA")
    image.paste(j, i[1], mask)

image.save(Path(argv[0]).parent / Path("output.png"), "PNG")
