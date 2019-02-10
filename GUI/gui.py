import os
import pygame
from pieces import pieces, layout_anchor
import numpy as np
from game_state import GameState

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

pygame.init()


class UIVariables:
    framerate = 50  # Bigger -> Slower

    # Fonts
    font_path = os.path.join(DIR_PATH, "fonts/OpenSans-Light.ttf")
    font_path_b = os.path.join(DIR_PATH, "fonts/OpenSans-Bold.ttf")
    font_path_i = os.path.join(DIR_PATH, "fonts/Inconsolata/Inconsolata.otf")

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 40)
    h3 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 25)
    h5 = pygame.font.Font(font_path, 20)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Background colors
    black = (10, 10, 10)     # rgb(10, 10, 10)
    white = (255, 255, 255)  # rgb(255, 255, 255)
    background = (200, 255, 200)
    grey_garbage = (119, 120, 115)
    grey_game_background = (75, 75, 75)
    grey_boarder = (26, 26, 26)
    grey_board = (35, 35, 35)

    # Colors
    cyan = (11, 160, 228)
    blue = (33, 68, 198)
    orange = (216, 93, 13)
    yellow = (224, 154, 0)
    green = (89, 175, 16)
    pink = (185, 32, 138)
    red = (200, 15, 46)

    t_color = {
        -2: grey_game_background,
        -1: grey_garbage,
        0: grey_board,
        1: pink,
        2: blue,
        3: yellow,
        4: red,
        5: green,
        6: cyan,
        7: orange,
        8: white
    }


class GUI:
    # Get global engine and setup gui
    def __init__(self, block_size, height, width):
        # Initial values
        self.blink = False
        self.pause = False
        self.start = True
        self.game_over = False
        self.done = False

        self.block_size = block_size

        self.screen_width = width * block_size + 800
        self.screen_height = height * block_size + 150
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))
        pygame.time.set_timer(pygame.USEREVENT, UIVariables.framerate * 10)
        pygame.display.set_caption("Blokus with noobs")

    # Draw block
    def _draw_block(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(x, y, self.block_size, self.block_size)
        )
        inner_pad = self.block_size // 7
        pygame.draw.rect(
            self.screen,
            self.get_brighter_color(color),
            pygame.Rect(x+inner_pad, y+inner_pad, self.block_size-inner_pad*2,
                        self.block_size-inner_pad*2),
            inner_pad
        )
        r, g, b = color
        if not (r == g and g == b):
            pygame.draw.rect(
                self.screen,
                self.get_brighter_color(color, 2),
                pygame.Rect(x+1, y+1, 3, 3),
                3
            )
        pygame.draw.rect(
            self.screen,
            UIVariables.grey_boarder,
            pygame.Rect(x, y, self.block_size, self.block_size),
            1
        )

    def _draw_stone(self, x, y, color, size):
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(x, y, size, size)
        )

    def get_brighter_color(self, color, factor=1.2):
        brighter_color = tuple([int(x * factor) if int(x * factor) < 255 else
                                255 for x in color])
        return brighter_color

    # Draw board of one player
    def _draw_board(self, board):
        for x in range(20):
            for y in range(20):
                dx = 400 + self.block_size * x
                dy = 100 + self.block_size * y
                self._draw_block(dx, dy, UIVariables.t_color[int(board[x][y])])

    def _draw_sidebar(self, rep, tx, ty, size):
        for x in range(24):
            for y in range(21):
                dx = tx + size * x
                dy = ty + size * y
                if int(rep[x][y]) == 0:
                    self._draw_stone(dx, dy, UIVariables.white, size)
                else:
                    self._draw_stone(dx, dy, UIVariables.t_color[int(rep[x][y])], size)

    # Draw game info in top area
    def _draw_top_bar(self, game_state):

        # Draw texts
        text_players_turn = UIVariables.h1.render(
           "Player " + str(game_state.players_turn) + " turn",
           1, UIVariables.black)
        text_round = UIVariables.h3.render(
            "Round " + str(game_state.round),
            1, UIVariables.black)

        # Place texts
        self.screen.blit(text_players_turn, (400, 20))
        self.screen.blit(text_round, (1070, 60))

    def _draw_player_bars(self, game_state):
        start_points = [(40, 100), (40, 500), (1240, 100), (1240, 500)]

        for player in range(game_state.player_num):
            text_player = UIVariables.h2.render(
                "Player " + str(player + 1), 1, UIVariables.t_color[player + 1])
            self.screen.blit(text_player, start_points[player])
            rep = self._get_pieces_left_rep(game_state.player_pieces_left[player], player)
            self._draw_sidebar(rep, start_points[player][0], start_points[player][1] + 70, 15)

    def _get_pieces_left_rep(self, pieces_left, player):
        rep = np.zeros((24, 21))
        for piece_num in range(21):
            piece = pieces[piece_num]
            anchor = layout_anchor[piece_num]
            for h in range(piece.shape[0]):
                for l in range(piece.shape[1]):
                    if piece[h][l] != 0:
                        if piece_num in pieces_left:
                            rep[anchor[0] + h][anchor[1] + l] = player + 1
                        else:
                            rep[anchor[0] + h][anchor[1] + l] = -1
        return rep

    # Updates the whole screen on call
    def update_screen(self, game_state):
        # Background gray
        self.screen.fill(UIVariables.white)

        self._draw_board(game_state.board)
        self._draw_top_bar(game_state)
        self._draw_player_bars(game_state)
        pygame.display.flip()
