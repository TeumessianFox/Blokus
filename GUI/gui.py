import os
import pygame

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

pygame.init()


class UIVariables:
    framerate = 50  # Bigger -> Slower
    shape_names = ['T', 'J', 'L', 'Z', 'S', 'I', 'O']

    # Fonts
    font_path = os.path.join(DIR_PATH, "fonts/OpenSans-Light.ttf")
    font_path_b = os.path.join(DIR_PATH, "fonts/OpenSans-Bold.ttf")
    font_path_i = os.path.join(DIR_PATH, "fonts/Inconsolata/Inconsolata.otf")

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h3 = pygame.font.Font(font_path, 25)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
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

    # Tetrimino colors
    cyan = (11, 160, 228)    # I
    blue = (33, 68, 198)     # J
    orange = (216, 93, 13)   # L
    yellow = (224, 154, 0)   # O
    green = (89, 175, 16)    # S
    pink = (185, 32, 138)    # T
    red = (200, 15, 46)      # Z

    t_color = {
        -2: grey_game_background,
        -1: grey_garbage,
        0: grey_board,
        1: pink,
        2: blue,
        3: orange,
        4: red,
        5: green,
        6: cyan,
        7: yellow,
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
        self.pressed_key = None

        self.block_size = block_size

        self.screen_width = width * block_size + 100
        self.screen_height = height * block_size + 50
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

    def get_brighter_color(self, color, factor=1.2):
        brighter_color = tuple([int(x * factor) if int(x * factor) < 255 else
                                255 for x in color])
        return brighter_color

    # Draw board of one player
    def _draw_board(self, board):
        for x in range(20):
            for y in range(20):
                dx = 50 + self.block_size * x
                dy = 50 + self.block_size * y
                self._draw_block(dx, dy, UIVariables.t_color[int(board[x][y])])

    # Draw score bar for one player
    def _draw_score(self):
        # Draw sidebar
        pygame.draw.rect(
            self.screen,
            UIVariables.white,
            pygame.Rect(0, 0, self.screen_width, self.screen_height)
        )

        # Draw texts
        # text_player = UIVariables.h3.render(
        #    f"P{player_id+1}: {self.global_state.players[player_id]}",
        #    1, UIVariables.black)

        # Place texts
        # self.screen.blit(text_player, (x_start + 5 * self.block_size + 10,
        # y_start + 20))

    # Render all players screen
    def _draw_all_screen(self, board):
        # Background gray
        self.screen.fill(UIVariables.black)

        self._draw_score()
        self._draw_board(board)
        pygame.display.flip()

    # Updates the whole screen on call
    def update_screen(self, board):
        pygame.time.wait(UIVariables.framerate)
        self._draw_all_screen(board)
