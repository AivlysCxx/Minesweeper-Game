import pygame
from settings import *
from sprites import *
import random
import pygame
from settings import *
from sprites import *
# TRIAL

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((default_width, default_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = GameBoard()
        self.board.show_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(bg_color)
        self.board.make_board(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_element:
            for tile in row:
                if tile.tile_type != "M" and not tile.reveal:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= tile_size
                my //= tile_size

                if event.button == 1:
                    if not self.board.board_element[mx][my].flag:
                        # uncover and check if exploded
                        if not self.board.uncover(mx, my):
                            # explode
                            for row in self.board.board_element:
                                for tile in row:
                                    if tile.flag and tile.tile_type != "M":
                                        tile.flag = False
                                        tile.reveal = True
                                        tile.img = tile_mine_wrong
                                    elif tile.tile_type == "M":
                                        tile.reveal = True
                            self.playing = False

                if event.button == 3:
                    if not self.board.board_element[mx][my].reveal:
                        self.board.board_element[mx][my].flag = not self.board.board_element[mx][my].flag

                if self.check_win():
                    self.win = True
                    self.playing = False
                    for row in self.board.board_element:
                        for tile in row:
                            if not tile.reveal:
                                tile.flag = True

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return


game = Game()
while True:
    game.new()
    game.run()




#
# class Game:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((default_width, default_height))
#         pygame.display.set_caption(title)
#         self.clock = pygame.time.Clock()
#
#     def new(self):
#         self.board = GameBoard()
#         self.board.show_board()
#
#     def run(self):
#         self.playing = True
#         while self.playing:
#             self.clock.tick(FPS)
#             self.events()
#             self.draw()
#
#     def draw(self):
#         self.screen.fill(bg_color)
#         self.board.make_board(self.screen)
#         pygame.display.flip()
#
#     def events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit(0)
#
#
# game = Game()
# while True:
#     game.new()
#     game.run()
