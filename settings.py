"""
This code is for game settings.
1. Color settings
2. Game default values settings
3. Import tiles
"""

import pygame
import os

# Color settings
white = (255, 255, 255)
bg_color = (40, 40, 40)

# Game default values setting
tile_size = 32
default_row = 15
default_col = 15
num_mine = 20
default_width = tile_size * default_row
default_height = tile_size * default_col
FPS = 60
title = "Minesweeper Game"

# Import all the tiles from the assets folder
# Tile type - numbers
tile_list = []
filename = "assets"
for i in range(1, 9):  # since mine number is up to 8
    # resize tile img we have to fit the tile size in our game which is a square
    tile_list.append(pygame.transform.scale
                     (pygame.image.load(os.path.join(filename, f"Tile{i}.png")),
                      (tile_size, tile_size)))
# Tile type - background tile
tile_blank = (pygame.transform.scale
              (pygame.image.load(os.path.join(filename, "TileEmpty.png")), (tile_size, tile_size)))
# Tile type - mine that explodes due to missclick
tile_mine_explode = (pygame.transform.scale
                     (pygame.image.load(os.path.join(filename, "TileExploded.png")), (tile_size, tile_size)))
# Tile type - user flags the tile indicating a mine under
tile_flag = (pygame.transform.scale
             (pygame.image.load(os.path.join("assets", "TileFlag.png")), (tile_size, tile_size)))
# Tile type - mine tile
tile_mine = (pygame.transform.scale
             (pygame.image.load(os.path.join("assets", "TileMine.png")), (tile_size, tile_size)))
# Tile type - blank or unclicked tiles
tile_unknown = (pygame.transform.scale
                (pygame.image.load(os.path.join("assets", "TileUnknown.png")), (tile_size, tile_size)))
# Tile type - this means users mis-flags the tile, there's actually no mine under
tile_mine_wrong = (pygame.transform.scale
                   (pygame.image.load(os.path.join("assets", "TileNotMine.png")), (tile_size, tile_size)))
