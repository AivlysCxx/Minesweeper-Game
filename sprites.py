"""
Sylvia's Code
"""
from settings import *
import random


# type of tile list


class Tile:
    """
    type list:
        "U" = unknown/unclicked block
        "M" = mine
        "N" = numbers shown on board as clues
        "B" = blank/empty spot
    """

    def __init__(self, x, y, img, tile_type, reveal=False, flag=False):
        self.x = x * tile_size
        self.y = y * tile_size
        self.img = img
        self.tile_type = tile_type
        self.reveal = reveal
        self.flag = flag

    def make_board(self, board_surface):
        board_surface.blit(self.img, (self.x, self.y))

    def __repr__(self):
        """
        This can print the board in console
        """
        return self.tile_type


class GameBoard:
    def __init__(self):
        self.board_surface = pygame.Surface((default_width, default_height))
        self.board_element = [[Tile(c, r, tile_blank, "B")
                               for r in range(default_row)] for c in range(default_col)]
        self.lay_mine()
        self.put_numbers()

    def lay_mine(self):
        for _ in range(num_mine):
            while True:
                # Generate a random location for laying mines
                x_val = random.randint(0, default_row - 1)
                y_val = random.randint(0, default_col - 1)
                # Change the existing blank tile to mine tile
                if self.board_element[x_val][y_val].tile_type == "B":
                    self.board_element[x_val][y_val].img = tile_mine
                    self.board_element[x_val][y_val].tile_type = "M"
                    break

    def put_numbers(self):
        for x in range(default_row):
            for y in range(default_col):
                if self.board_element[x][y].tile_type != "M":
                    mine_count = self.check_neighbors(x, y)
                    # If we found a block that needs a number in it
                    if mine_count > 0:
                        self.board_element[x][y].img = tile_list[mine_count-1]
                        self.board_element[x][y].tile_type = "N"

    @staticmethod
    def boundary_check(x, y):
        """
        This is to check if we're inside the boards' boundary.
        """
        check = 0 <= x < default_row and 0 <= y < default_col
        return check

    def check_neighbors(self, x, y):
        mine_count = 0
        # coordinates of the neighbors around our tile of interest
        # starting from top left of it which is (-1,-1)
        for x1 in range(-1, 2):
            for y1 in range(-1, 2):
                nb_x = x + x1
                nb_y = y + y1
                # check if neighbor is within boundary
                if self.boundary_check(nb_x, nb_y):
                    # check if neighbor is a mine
                    if self.board_element[nb_x][nb_y].tile_type == "M":
                        mine_count += 1
        return mine_count



    def make_board(self, screen):
        for r in self.board_element:
            for tile in r:
                tile.make_board(self.board_surface)
        screen.blit(self.board_surface, (0, 0))  # top left corner of the screen

    def show_board(self):
        for r in self.board_element:
            print(r)
