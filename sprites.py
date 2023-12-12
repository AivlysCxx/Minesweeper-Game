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
        "n" = numbers shown on board as clues
        "." = blank/empty spot
    """

    def __init__(self, x, y, img, tile_type, reveal=False, flag=False):
        self.x = x * tile_size
        self.y = y * tile_size
        self.img = img
        self.tile_type = tile_type
        self.reveal = reveal
        self.flag = flag

    def make_board(self, board_surface):
        # We put either a mine or number on a revealed (clicked) tile
        # We also make sure that this tile has no flag
        if not self.flag and self.reveal:
            board_surface.blit(self.img, (self.x, self.y))
        # We put a flag on unknown (revealed) tile if right-clicked
        elif self.flag and not self.reveal:
            board_surface.blit(tile_flag, (self.x, self.y))
        # Placing unknown tile
        elif not self.reveal:
            board_surface.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        """
        This can print the board in console
        """
        return self.tile_type


class GameBoard:
    def __init__(self):
        self.board_surface = pygame.Surface((default_width, default_height))
        self.board_element = [[Tile(c, r, tile_blank, ".")
                               for r in range(default_row)] for c in range(default_col)]
        self.lay_mine()
        self.put_numbers()
        self.uncover_history = []

    def lay_mine(self):
        for _ in range(num_mine):
            while True:
                # Generate a random location for laying mines
                x_val = random.randint(0, default_row - 1)
                y_val = random.randint(0, default_col - 1)
                # Change the existing blank tile to mine tile
                if self.board_element[x_val][y_val].tile_type == ".":
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
                        self.board_element[x][y].tile_type = "n"

    def place_mines_post_first_click(self, first_click_x, first_click_y):
        # Define the safe zone around the first click
        safe_zone = [(x, y) for x in range(first_click_x - 1, first_click_x + 2)
                     for y in range(first_click_y - 1, first_click_y + 2)
                     if 0 <= x < default_row and 0 <= y < default_col]

        mines_placed = 0
        while mines_placed < num_mine:
            x = random.randint(0, default_row - 1)
            y = random.randint(0, default_col - 1)

            if (x, y) not in safe_zone and self.board_element[x][y].tile_type == ".":
                self.board_element[x][y].tile_type = "X"
                mines_placed += 1
        self.put_numbers()

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

    def uncover(self, x, y):
        self.uncover_history.append((x, y))
        # If we uncover and hit a mine, mine explodes
        if self.board_element[x][y].tile_type == "M":
            self.board_element[x][y].reveal = True
            self.board_element[x][y].img = tile_mine_explode
            return False
        # If we uncover and hit a number
        elif self.board_element[x][y].tile_type == "n":
            self.board_element[x][y].reveal = True
            return True
        self.board_element[x][y].reveal = True
        # Recursively run this loop when we uncover and hit a blank tile
        # This loop will stop when it finds a number
        for r in range(max(0, x-1), min(default_row-1, x+1)+1):
            for c in range(max(0, y - 1), min(default_col - 1, y+1)+1):
                # check if the coordinate is already explored
                if (r, c) not in self.uncover_history:
                    self.uncover(r, c)
        return True


    def show_board(self):
        for r in self.board_element:
            print(r)
