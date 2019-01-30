import numpy as np
from pieces import pieces
import game_state

color_order = ['blue', 'yellow', 'red', 'green']

class GlobalEngine:
    def __int__(self, player_num, block_size, activate_gui, height, length, window_height, window_length):
        self.player_num = player_num
        self.height = height
        self.length = length

        self.activate_gui = activate_gui
        self.block_size = block_size
        self.window_height = window_height
        self.window_length = window_length

        self.state = game_state.GameState(player_num, height, length)

    def commit_move(self, piece, anchor):

        return
