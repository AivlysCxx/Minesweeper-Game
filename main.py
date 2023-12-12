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
