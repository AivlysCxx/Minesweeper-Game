import pygame
from settings import Settings
from sprites import Sprites


class PygameGame:
    """
    This class represents the main game environment. It is responsible for initializing
    the game window, handling the game loop, processing user inputs, and rendering the game's graphical components.

    Attributes:
        settings (Settings): An instance of the Settings class, holding game settings like screen size, title, and FPS.
        screen (pygame.Surface): The main screen surface where all graphical elements are drawn.
        clock (pygame.time.Clock): A clock to control the game's frame rate.
        sprites (Sprites): An instance of the Sprites class, used to manage game sprites.
        board (Board): The game board, an instance of the Board class from Sprites.
        is_playing (bool): A flag to indicate whether the game is currently being played.
    """

    def __init__(self):
        """Initialize the game by setting up the pygame display, clock, and other necessary components."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()
        self.sprites = Sprites()

    def start_new_game(self):
        """
        Starts a new game. Initializes the game board and prepares it for display.
        This method should be called each time a new game session is begun.
        """
        self.board = self.sprites.create_board()
        self.board.show()

    def game_loop(self):
        """
        The main loop of the game. This method keeps the game running, updating the screen,
        and responding to user events until the game ends. The loop runs at a rate defined by the FPS setting.
        """
        self.is_playing = True
        while self.is_playing:
            self.clock.tick(self.settings.fps)
            self.handle_events()
            self.update_screen()
        else:
            self.show_end_screen()

    def update_screen(self):
        """
        Redraws the game screen with the current state of the game board. This method is called
        every frame to update the game's graphical elements.
        """
        self.screen.fill(self.settings.bg_color)
        self.board.render(self.screen)
        pygame.display.update()

    def check_victory(self):
        """
        Checks if the player has won the game. A player wins if all tiles that are not mines are revealed.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return all(tile.revealed or tile.type == "X" for row in self.board.tiles for tile in row)

    def handle_events(self):
        """
        Processes all user input events such as mouse clicks and window closing.
        This method is responsible for the interactive part of the game, reacting to player actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // self.settings.tile_size, mouse_y // self.settings.tile_size

                if event.button == 1:
                    self.left_click_action(grid_x, grid_y)

                if event.button == 3:
                    self.right_click_action(grid_x, grid_y)

                if self.check_victory():
                    self.declare_victory()

    def left_click_action(self, x, y):
        """
        Handles the action triggered by a left mouse click. If the clicked tile is not flagged, it either
        uncovers the tile or triggers the explosion of mines depending on whether the tile is a mine.

        Args:
            x (int): The x-coordinate of the tile in the grid.
            y (int): The y-coordinate of the tile in the grid.
        """
        if not self.board.tiles[x][y].flagged:
            if not self.board.uncover(x, y):
                self.explode_mines()
                self.is_playing = False

    def right_click_action(self, x, y):
        """
        Handles the action triggered by a right mouse click. It toggles the flagged state of a tile,
        indicating a potential mine.

        Args:
            x (int): The x-coordinate of the tile in the grid.
            y (int): The y-coordinate of the tile in the grid.
        """
        tile = self.board.tiles[x][y]
        if not tile.revealed:
            tile.flagged = not tile.flagged

    def explode_mines(self):
        """
        Triggers when a mine is uncovered. It reveals all mines and marks incorrectly flagged tiles.
        This method is called to end the game when a mine is clicked.
        """
        for row in self.board.tiles:
            for tile in row:

