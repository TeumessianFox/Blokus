import numpy as np
from pieces import pieces

color_order = ['blue', 'yellow', 'red', 'green']


class GameState:
    def __init__(self, player_num, height, width):
        self.player_num = player_num
        self.height = height
        self.width = width

        self.board = np.zeros((height, width))
        self.player_pieces_left = [np.arange(21).tolist(),
                                   np.arange(21).tolist(),
                                   np.arange(21).tolist(),
                                   np.arange(21).tolist()]
        self.last_piece_played = [None, None, None, None]
        self.round = 1
        self.players_turn = 1
        self.game_over = False
        self.scores = [0, 0, 0, 0]
        self.next_possible_moves_current_player = \
            self.possible_moves_current_player()

    def __repr__(self):
        board = self.board
        s = "Round: " + str(self.round) + "\n"
        s += "Player's turn: " + str(self.players_turn) + "\n"
        s += 'o' + '-' * self.width + 'o'
        for line in board.T[0:]:
            display_line = ['\n|']
            for grid in line:
                if grid == 0:
                    display_line.append('0')
                elif grid == 1:
                    display_line.append('1')
                elif grid == 2:
                    display_line.append('2')
                elif grid == 3:
                    display_line.append('3')
                elif grid == 4:
                    display_line.append('4')
                else:
                    display_line.append('X')
            display_line.append('|')
            s += "".join(display_line)

        s += '\no' + '-' * self.width + 'o\n'
        return s

    def eval_game(self):
        for player in self.player_num:
            if len(self.player_pieces_left[player]) == 0:
                self.scores[player] = 15
                if self.last_piece_played == 0:
                    self.scores[player] += 5
            else:
                score = 0
                for piece_num in self.player_pieces_left[player]:
                    piece = pieces[piece_num]
                    for h in range(piece.shape[0]):
                        for l in range(piece.shape[1]):
                            if piece[h][l] != 0:
                                score += 1
                score = -score
                self.scores[player] = score
        return None

    def possible_moves_current_player(self):
        moves = list()
        for piece_num in self.player_pieces_left[self.players_turn - 1]:
            piece = pieces[piece_num]
            piece = self._change_piece_colour(piece)
            if piece_num == 0 or piece_num == 7 or piece_num == 20:
                for x in range(self.height - piece.shape[0] + 1):
                    for y in range(self.width - piece.shape[1] + 1):
                        if self._check_move(piece, (x, y)):
                            moves.append((piece_num, piece, (x, y)))
            elif piece_num == 1 or piece_num == 2 or \
                    piece_num == 4 or piece_num == 9:
                for rotation in range(2):
                    rot_piece = np.rot90(piece, rotation)
                    for x in range(self.height - rot_piece.shape[0] + 1):
                        for y in range(self.width - rot_piece.shape[1] + 1):
                            if self._check_move(rot_piece, (x, y)):
                                moves.append((piece_num, rot_piece, (x, y)))
            else:
                for rotation in range(4):
                    rot_piece = np.rot90(piece, rotation)
                    for x in range(self.height - rot_piece.shape[0] + 1):
                        for y in range(self.width - rot_piece.shape[1] + 1):
                            if self._check_move(rot_piece, (x, y)):
                                moves.append((piece_num, rot_piece, (x, y)))
        return moves

    def commit_move(self, piece_num, piece, anchor):
        if self._check_move(piece, anchor):
            for x in range(piece.shape[0]):
                for y in range(piece.shape[1]):
                    xm = x + anchor[0]
                    ym = y + anchor[1]
                    if piece[x][y] != 0:
                        self.board[xm][ym] = self.players_turn
            self.last_piece_played[self.players_turn-1] = piece_num
            self.player_pieces_left[self.players_turn-1].remove(piece_num)
            if self.players_turn < 4:
                self.players_turn += 1
            else:
                self.players_turn = 1
                self.round += 1
            self.next_possible_moves_current_player = \
                self.possible_moves_current_player()
            counter = 0
            while len(self.next_possible_moves_current_player) == 0 \
                    and counter < 4:
                if self.players_turn < 4:
                    self.players_turn += 1
                else:
                    self.players_turn = 1
                    self.round += 1
                counter += 1
                if counter == 4:
                    self.game_over = True
                    self._eval_game()
                self.next_possible_moves_current_player = \
                    self.possible_moves_current_player()
        else:
            print("Error move not possible")

    def _eval_game(self):
        for player in range(self.player_num):
            if len(self.player_pieces_left[player]) == 0:
                self.scores[player] = 15
                if self.last_piece_played == 0:
                    self.scores[player] += 5
            else:
                score = 0
                for piece_num in self.player_pieces_left[player]:
                    piece = pieces[piece_num]
                    for h in range(piece.shape[0]):
                        for l in range(piece.shape[1]):
                            if piece[h][l] != 0:
                                score += 1
                score = -score
                self.scores[player] = score

        return None

    def _change_piece_colour(self, piece):
        for x in range(piece.shape[0]):
            for y in range(piece.shape[1]):
                if piece[x][y] != 0:
                    piece[x][y] = self.players_turn
        return piece

    def _check_move(self, piece, anchor):
        if self._check_free_space(piece, anchor) and \
                self._check_placement_rules(piece, anchor):
            return True
        return False

    def _check_placement_rules(self, piece, anchor):
        touch_corner = 0
        touch_own_stone = 0
        board_corner = [(0, 0), (0, self.width - 1), (self.height - 1, 0),
                        (self.height - 1, self.width - 1)]
        for h in range(piece.shape[0]):
            for l in range(piece.shape[1]):
                hm = h + anchor[0]
                lm = l + anchor[1]
                # In case of the first round
                if piece[h][l] == 0:
                    continue
                if self.round == 1 and piece[h][l] != 0:
                    if (hm, lm) == board_corner[self.players_turn - 1]:
                        touch_corner = 1
                if (0 <= hm - 1 < self.height and lm < self.width and
                    self.board[hm - 1][lm] == self.players_turn) or \
                        (hm + 1 < self.height and lm < self.width and
                         self.board[hm + 1][lm] == self.players_turn) or \
                        (hm < self.height and 0 <= lm - 1 < self.width and
                         self.board[hm][lm - 1] == self.players_turn) or \
                        (hm < self.height and lm + 1 < self.width and
                         self.board[hm][lm + 1] == self.players_turn):
                    return False
                if (0 <= hm - 1 < self.height and 0 <= lm - 1 < self.width and
                    self.board[hm - 1][lm - 1] == self.players_turn) or \
                        (hm + 1 < self.height and 0 <= lm - 1 < self.width and
                         self.board[hm + 1][
                             lm - 1] == self.players_turn) or \
                        (0 <= hm - 1 < self.height and lm + 1 < self.width and
                         self.board[hm - 1][
                             lm + 1] == self.players_turn) or \
                        (hm + 1 < self.height and lm + 1 < self.width and
                         self.board[hm + 1][
                             lm + 1] == self.players_turn):
                    touch_own_stone = 1
        if self.round == 1:
            if touch_corner == 0:
                return False
            else:
                return True
        elif touch_own_stone == 0:
            return False
        else:
            return True

    def _check_free_space(self, piece, anchor):
        for h in range(piece.shape[0]):
            for l in range(piece.shape[1]):
                hm = h + anchor[0]
                lm = l + anchor[1]
                if piece[h][l] != 0 and ((hm < 0 or hm > self.height - 1) or
                                         (lm < 0 or lm > self.width - 1)):
                    return False
                else:
                    if piece[h][l] != 0 and self.board[hm][lm] != 0:
                        return False
        return True
