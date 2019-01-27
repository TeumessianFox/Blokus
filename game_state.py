import numpy as np
from old_pieces import pieces

color_order = ['blue', 'yellow', 'red', 'green']

class GameState:
    def __int__(self, player_num, height, length):
        self.player_num = player_num
        self.height = height
        self.length = length

        self.board = np.zeros(height, length)
        self.player_pieces_left =np.repeat(np.arange(21), 4)
        self.round = 1
        self.players_turn = 0
        self.game_over = False
        self.scores = [0, 0, 0, 0]

    def game_over(self):
        for player in self.player_num:
            if self.possible_moves() is not None:
                return False
        return True

    def possible_moves(self):
        moves = list()
        for piece in self.player_pieces_left[self.players_turn]:
            if piece == 0 or piece == 7 or piece == 20:

            elif piece == 1 or piece == 2 or piece == 4 or piece 9:
                for rotation in range(2):

            else:
                for rotation in range(4):

    def try_move(self, piece, anchor):
        if valid_placement
        return True

    def valid_placement(self, piece, anchor):
        touch_corner = 0
        for h in range(piece.shape[0]):
            for l in range(piece.shape[1]):
                hm = h + anchor[0]
                lm = l + anchor[1]
                if self.round == 1:
                    if
                if pieces[piece][h][l] != 0 and ((hm < 0 or hm > self.height-1) or (lm < 0 or lm > self.length-1)):
                    return False
                else:
                    if pieces[piece][h][l] != 0 and self.board[hm][lm] != 0:
                        return False

    def piece_rot90(self, piece):
        return np.rot90(piece)

    def piece_rot180(self, piece):
        return np.rot90(piece, 2)

    def piece_rot270(self, piece):
        return np.rot90(piece, 3)