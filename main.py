"""
Software Carpentry EN.540.635.01
Final Project - Minesweeper Game
Dec. 2023

Contributors:
Yuqing Lu (Louise)
Xiaojun Chen (Sylvia)

Please refer to the README file for more info.
"""
import pygame
import random
from settings import *
import settings

################Xiaojun Chen########################################################
class Tile:
    """
    This class is a wrapper for defining tiles in this game.
    Tile type list:
        "." = unknown/un-clicked block
        "M" = mine
        "n" = numbers shown on board as clues
        "/" = blank/empty spot (not used)
    """

    def __init__(self, x, y, img, tile_type, reveal=False, flag=False):
        """
        Tile initialization.

        **Parameters**
            x: *int*
                x coordinate of the tile
            y: *int*
                y coordinate of the tile
            img: *pygame.Surface*
                The tile image
            title_type: *str*
                Type of the tile
            reveal: *bool*
                Whether the tile is revealed, default to False
            flag: *bool*
                Whether the tile is flagged, default to False
        """
        self.x = x * tile_size
        self.y = y * tile_size
        self.img = img
        self.tile_type = tile_type
        self.reveal = reveal
        self.flag = flag

    def make_board(self, board_surface):
        """
        Draws tiles on the given board surface.

        **Parameters**
            board_surface: *pygame.Surface*
                The surface of board on which to draw the tiles.
        """
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
        This can print the board in console as a string

        **Returns**
            *str*
                The string representation of board including tile types
        """
        return self.tile_type


class GameBoard:
    """
    This class is a wrapper for the Minesweeper game board.
    This class manages the tiles on the board, including their initial setup,
    placement of mines, and revealing tiles during gameplay.

    **Attributes**
        board_surface:*pygame.Surface*
            The surface on which the board elements/tiles are drawn
        board_element: *list[list[Tile]]*
            A 2D array of tile objects representing the game board
        lay_mine: *bool*
            Indication of whether mines have been laid on the board
        uncover_history: *list[tuple]*
            A list to keep track of uncovered tiles to prevent redundant operations
    """

    def __init__(self):
        """
        Initialization of the GameBoard
        """
        self.board_surface = pygame.Surface((default_width, default_height))
        self.board_element = [[Tile(c, r, tile_blank, ".")
                               for r in range(default_row)] for c in range(default_col)]
        self.lay_mine = True
        # self.lay_mine()
        # self.put_numbers()
        self.uncover_history = []

    def lay_mine(self):
        """
        Randomly places a predetermined number of mines on the board.
        This also ensures that each mine is placed on a unique tile.
        """
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
        """
        Assigns numbers to tiles based on the number of adjacent mines.
        This method is called after mines have been placed on the board.
        """
        for x in range(default_row):
            for y in range(default_col):
                if self.board_element[x][y].tile_type != "M":
                    mine_count = self.check_neighbors(x, y)
                    # If we found a block that needs a number in it
                    if mine_count > 0:
                        self.board_element[x][y].img = tile_list[mine_count - 1]
                        self.board_element[x][y].tile_type = "n"

    def place_mines_post_first_click(self, first_click_x, first_click_y):
        """
        Places mines on the board after the first click.
        This ensures that the first click we don't hit a mine.

        **Parameters**
            first_click_x: *int*
                x coordinate of the first click
            first_click_y: *int*
                y coordinate of the first click
        """
        # Define the safe zone around the first click
        safe_zone = [(x, y) for x in range(first_click_x - 1, first_click_x + 2)
                     for y in range(first_click_y - 1, first_click_y + 2)
                     if 0 <= x < default_row and 0 <= y < default_col]

        mines_placed = 0
        while mines_placed < num_mine:
            x = random.randint(0, default_row - 1)
            y = random.randint(0, default_col - 1)

            if (x, y) not in safe_zone and self.board_element[x][y].tile_type == ".":
                self.board_element[x][y].tile_type = "M"  # Change "X" to "M" to indicate mine
                self.board_element[x][y].img = tile_mine  # Assign the mine image
                mines_placed += 1
        self.put_numbers()

    @staticmethod
    def boundary_check(x, y):
        """
        This is to check if we're inside the boards' boundary.

        **Parameters**
            x: *int*
                The x coordinate to check
            y: *int*
                The y coordinate to check

        **Returns**
            check: *bool*
                True if within the boundary, False otherwise
        """
        check = 0 <= x < default_row and 0 <= y < default_col
        return check

    def check_neighbors(self, x, y):
        """
        Counts the number of neighboring mines adjacent to our tile of interest.

        **Parameters**
            x: *int*
                x coordinate of the tile
            y: *int*
                y coordinate of the tile

        **Returns**
            mine_count: *int*
                The number of neighboring mines
        """
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
        """
        Draws the current state of the game board on the given screen.
        This is responsible for displaying each tiles' current state, whether it's
        a revealed mine, a number, a flag, or an unrevealed tile.

        **Parameters**
            screen: *pygame.Surface*
                The surface onto which the board is drawn
        """
        if self.lay_mine:  # Only generate the board if mines are laid
            for r in self.board_element:
                for tile in r:
                    tile.make_board(self.board_surface)
            screen.blit(self.board_surface, (0, 0))

    def uncover(self, x, y):
        """
        Uncovers a tile at the specific coordinates and performs actions based on the type pf tile.
        If the tile is a mine, explodes.
        If the tile is a number, reveals itself.
        If the tile is a blank tile, it triggers a recursive uncovering of adjacent tiles.

        **Parameters**
            x: *int*
                x coordinate of the tile to uncover
            y: *int*
                y coordinate of the tile to uncover

        **Returns**
            *bool*
                True if the uncover action is successful and safe
                False if a mine is uncovered
        """
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
        for r in range(max(0, x - 1), min(default_row - 1, x + 1) + 1):
            for c in range(max(0, y - 1), min(default_col - 1, y + 1) + 1):
                # check if the coordinate is already explored
                if (r, c) not in self.uncover_history:
                    self.uncover(r, c)
        return True

    def show_board(self):
        """
        Prints the current state of the board to the console.
        Useful for debugging.
        """
        for r in self.board_element:
            print(r)

################Yuqing Lu########################################################

class PygameGame:
    """
    This class encapsulates the main game environment for a Minesweeper game. It initializes
    the game window, handles the game loop, processes user inputs, and renders the game's graphical components.

    Attributes:
        settings (module): An instance of the Settings module, containing configurations like screen size, title, and FPS.
        screen (pygame.Surface): The main screen surface for drawing graphical elements of the game.
        clock (pygame.time.Clock): A clock to regulate the game's frame rate.
        board (GameBoard): The game board, an instance of the GameBoard class.
        is_playing (bool): A flag to determine if the game is currently active.
        start_time (int): Variable to track the start time of the game.
        first_click (bool): A flag to indicate whether the first click has occurred.
        won (bool): A flag to indicate whether the player has won the game.
    """

    def __init__(self):
        pygame.init()
        self.settings = settings
        # set the width and weight from the setting file
        self.screen = pygame.display.set_mode((self.settings.default_width, self.settings.default_height))
        # set the window title according to setting
        pygame.display.set_caption(self.settings.title)
        # set a clock to count the time
        self.clock = pygame.time.Clock()
        self.board = GameBoard()
        self.is_playing = False
        self.start_time = None
        self.first_click = True
        # Set win status to True
        self.won = True

    def start_new_game(self):
        """
        Initializes and starts a new game of Minesweeper.
        Resets the game board, the start time, and relevant game flags.
        """
        self.board = GameBoard()
        # self.board.show_board()
        self.start_time = pygame.time.get_ticks()

    def game_loop(self):
        """
        The main game loop. Handles the sequence of actions that occur during the game.
        This includes event handling, screen updating, and timer rendering.
        Continues until the game ends.
        """
        self.is_playing = True
        while self.is_playing:
            self.clock.tick(self.settings.FPS)
            self.handle_events()
            self.update_screen()
            self.render_timer()
        else:
            self.show_end_screen()

    def update_screen(self):
        """
        Updates the game screen. Clears the screen, renders the board, and updates the display.
        """
        self.screen.fill(self.settings.bg_color)
        self.board.make_board(self.screen)
        pygame.display.flip()

    def render_timer(self):
        """
        Renders the timer on the game screen. Calculates elapsed time and displays it.
        """
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert milliseconds to seconds
        timer_font = pygame.font.Font(None, 36)  # Choose an appropriate font and size
        timer_surface = timer_font.render(str(elapsed_time), True, self.settings.white)  # Render the time as text
        self.screen.blit(timer_surface, (10, 10))  # Position the timer on the screen
        pygame.display.update()

    def check_victory(self):
        """
        Checks if the player has won the game.
        Victory is achieved when all non-mine tiles are revealed.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for row in self.board.board_element:
            for tile in row:
                # If a non-mine tile is not revealed, return False
                if tile.tile_type != "M" and not tile.reveal:
                    return False
        # If all non-mine tiles are revealed, return True
        return True

    def handle_events(self):
        """
        Handles user input events, including mouse clicks and game closure.
        Processes left and right mouse clicks and checks for game victory.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // self.settings.tile_size, my // self.settings.tile_size

                if event.button == 1:
                    self.left_click_action(x, y)

                if event.button == 3:
                    self.right_click_action(x, y)

        if self.check_victory():
            self.declare_victory()

    def left_click_action(self, x, y):
        """
        Handles the action when a left mouse click occurs on the board.
        If it's the first click, mines are placed. Otherwise, the tile is uncovered.

        Attributes:
            x (int): The x-coordinate (column) of the clicked tile.
            y (int): The y-coordinate (row) of the clicked tile.
        """
        if self.first_click:
            self.board.place_mines_post_first_click(x, y)
            self.first_click = False
            self.board.lay_mine = True
            self.board.show_board()
        if not self.board.board_element[x][y].flag:
            if not self.board.uncover(x, y):
                self.explode_mines()
                self.is_playing = False

    def right_click_action(self, x, y):
        """
        Handles the action when a right mouse click occurs on the board.
        Toggles a flag on the clicked tile if it is not revealed.

        Attributes:
            x (int): The x-coordinate (column) of the clicked tile.
            y (int): The y-coordinate (row) of the clicked tile.
        """
        tile = self.board.board_element[x][y]
        if not tile.reveal:
            tile.flag = not tile.flag

    def explode_mines(self):
        """
        Handles the scenario when a mine is clicked.
        Reveals all mines and marks wrongly flagged tiles.
        Also sets the game's win status to False.
        """
        # if exploded, set the status to false
        self.won = False
        for row in self.board.board_element:
            for tile in row:
                if tile.tile_type == "M":
                    tile.reveal = True  # Reveal all mines
                    # tile.img = self.settings.tile_mine  # Show mine image
                if tile.flag and tile.tile_type != "M":
                    tile.flag = False
                    tile.reveal = True
                    tile.img = self.settings.tile_mine_wrong

    def show_end_screen(self):
        """
        Displays the end screen when the game is over.
        Shows the final game state, a message indicating the outcome, and the total time played.
        """
        # Calculate total elapsed time
        total_time = (pygame.time.get_ticks() - self.start_time) // 1000  # in seconds
        if self.won:
            message = "You Win!"
        else:
            message = "Game Over!"
        print(message + f" Time used: {total_time} seconds")
        # Render total time on screen
        font = pygame.font.Font(None, 36)
        message_surface = font.render(message, True, self.settings.white)
        time_surface = font.render(f"Time: {total_time} sec", True, self.settings.white)

        # Reveal all tiles
        self.explode_mines()

        # Show the final state of the board
        end_time = pygame.time.get_ticks() + 120000  # 2 minutes
        while pygame.time.get_ticks() < end_time:
            self.update_screen()
            self.screen.blit(message_surface, (self.settings.default_width // 2, 20))  # Adjust position as needed
            self.screen.blit(time_surface, (self.settings.default_width // 2, 60))  # Adjust position as needed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def declare_victory(self):
        """
        Sets the game's playing status to False.
        """
        self.is_playing = False


if __name__ == "__main__":
    game = PygameGame()
    game.start_new_game()
    game.game_loop()
