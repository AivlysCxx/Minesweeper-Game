import pygame
import settings
import sprites


class PygameGame:
    def __init__(self):
        pygame.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption(self.settings.TITLE)
        self.clock = pygame.time.Clock()
        self.board = sprites.Board()
        self.is_playing = False
        self.start_time = None
        self.first_click = True

    def start_new_game(self):
        self.board = sprites.Board()
        self.board.display_board()
        self.is_playing = True
        self.start_time = pygame.time.get_ticks()

    def game_loop(self):
        while self.is_playing:
            self.clock.tick(self.settings.FPS)
            self.handle_events()
            self.update_screen()
            self.render_timer()
        self.show_end_screen()

    def update_screen(self):
        self.screen.fill(self.settings.BGCOLOUR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def render_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert milliseconds to seconds
        timer_font = pygame.font.Font(None, 36)  # Choose an appropriate font and size
        timer_surface = timer_font.render(str(elapsed_time), True, self.settings.WHITE)  # Render the time as text
        self.screen.blit(timer_surface, (10, 10))  # Position the timer on the screen
        pygame.display.update()

    def check_victory(self):
        for row in self.board.board_list:
            for tile in row:
                # If a non-mine tile is not revealed, return False
                if tile.type != "X" and not tile.revealed:
                    return False
        # If all non-mine tiles are revealed, return True
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // self.settings.TILESIZE, my // self.settings.TILESIZE

                if event.button == 1:
                    self.left_click_action(x, y)

                if event.button == 3:
                    self.right_click_action(x, y)

        if self.check_victory():
            self.declare_victory()

    def left_click_action(self, x, y):
        if self.first_click:
            self.board.place_mines_post_first_click(x, y)
            self.first_click = False

        if not self.board.board_list[x][y].flagged:
            if not self.board.dig(x, y):
                self.explode_mines()
                self.is_playing = False

    def right_click_action(self, x, y):
        tile = self.board.board_list[x][y]
        if not tile.revealed:
            tile.flagged = not tile.flagged

    def explode_mines(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type == "X":
                    tile.revealed = True  # Reveal all mines
                    tile.image = self.settings.tile_mine  # Show mine image
                if tile.flagged and tile.type != "X":
                    tile.image = self.settings.tile_not_mine

    def show_end_screen(self):
        print("Game Over!")
        self.explode_mines()  # Reveal all tiles

        # Show the final state of the board for 2 minutes
        end_time = pygame.time.get_ticks() + 120000  # 120000 milliseconds = 2 minutes
        while pygame.time.get_ticks() < end_time:
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def declare_victory(self):
        self.is_playing = False


if __name__ == "__main__":
    game = PygameGame()
    game.start_new_game()
    game.game_loop()




---------------------------------------------------------------
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
        # set the width and weight from the setting file
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        # set the window title according to setting
        pygame.display.set_caption(self.settings.title)
        # creat a clock that can be used to control the game
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

#################
import pygame
from settings import Settings
from sprites import Sprites


class PygameGame:
    """
    Main game class for handling game initialization, loop, and events.
    """

    def __init__(self):
        """Initialize the game, setting up the screen, clock, and other settings."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()
        self.sprites = Sprites()

    def start_new_game(self):
        """Start a new game by initializing the game board and displaying it."""
        self.board = self.sprites.create_board()
        self.board.show()

    def game_loop(self):
        """Main game loop that keeps running while the game is being played."""
        self.is_playing = True
        while self.is_playing:
            self.clock.tick(self.settings.fps)  # Control game's frame rate
            self.handle_events()  # Handle user inputs
            self.update_screen()  # Refresh the game screen
        else:
            self.show_end_screen()  # Show end screen when the game ends

    def update_screen(self):
        """Update the game screen by redrawing all elements and updating the display."""
        self.screen.fill(self.settings.bg_color)
        self.board.render(self.screen)
        pygame.display.update()

    def check_victory(self):
        """Check if all non-mine tiles are revealed, indicating a win."""
        return all(tile.revealed or tile.type == "X" for row in self.board.tiles for tile in row)

    def handle_events(self):
        """Handle all events from the user, such as mouse clicks and quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // self.settings.tile_size, mouse_y // self.settings.tile_size

                if event.button == 1:  # Left Click
                    self.left_click_action(grid_x, grid_y)

                if event.button == 3:  # Right Click
                    self.right_click_action(grid_x, grid_y)

                if self.check_victory():
                    self.declare_victory()

    def left_click_action(self, x, y):
        """Handle left-click action on the game board."""
        if not self.board.tiles[x][y].flagged:
            if not self.board.uncover(x, y):
                self.explode_mines()
                self.is_playing = False

    def right_click_action(self, x, y):
        """Handle right-click action for flagging tiles on the game board."""
        tile = self.board.tiles[x][y]
        if not tile.revealed:
            tile.flagged = not tile.flagged

    def explode_mines(self):
        """Reveal all mines and incorrect flags when a mine is uncovered."""
        for row in self.board.tiles:
            for tile in row:
                if tile.flagged and tile.type != "X":
                    tile.flagged = False
                    tile.revealed = True
                    tile.image = self.sprites.tile_not_mine_image
                elif tile.type == "X":
                    tile.revealed = True

    def declare_victory(self):
        """Declare victory and end the game when all non-mine tiles are revealed."""
        self.win = True
        self.is_playing = False
        for row in self.board.tiles:
            for tile in row:
                if not tile.revealed:
                    tile.flagged = True

    def show_end_screen(self):
        """Show an end screen that waits for user interaction before closing."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type is pygame.MOUSEBUTTONDOWN:
                    return


def main():
    """Entry point of the application. Initializes and runs the game loop."""
    game = PygameGame()
    while True:
        game.start_new_game()
        game.game_loop()

