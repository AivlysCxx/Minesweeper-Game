

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
