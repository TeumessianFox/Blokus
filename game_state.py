import numpy as np
import copy
from pieces import pieces


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

    #####################################################################

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

    def find_empty_corners(self, player):
        # For starting move
        if self.round == 1:
            board_corner = [(0, 0), (0, self.width - 1), (self.height - 1, 0),
                            (self.height - 1, self.width - 1)]
            return [board_corner[player - 1]]

        # Find possible corners to place stones
        empty_corners = list()
        for h in range(self.height):
            for w in range(self.width):
                if self.board[h][w] == 0:
                    if (0 <= h - 1 < self.height and w < self.width and
                        self.board[h - 1][w] == player) or \
                            (h + 1 < self.height and w < self.width and
                             self.board[h + 1][w] == player) or \
                            (h < self.height and 0 <= w - 1 < self.width and
                             self.board[h][w - 1] == player) or \
                            (h < self.height and w + 1 < self.width and
                             self.board[h][w + 1] == player):
                        continue
                    if (0 <= h - 1 < self.height and
                        0 <= w - 1 < self.width and
                        self.board[h - 1][w - 1] == player) or \
                            (h + 1 < self.height and
                             0 <= w - 1 < self.width and
                             self.board[h + 1][w - 1] == player) or \
                            (0 <= h - 1 < self.height and
                             w + 1 < self.width and
                             self.board[h - 1][w + 1] == player) or \
                            (h + 1 < self.height and
                             w + 1 < self.width and
                             self.board[h + 1][w + 1] == player):
                        empty_corners.append((h, w))
        return empty_corners

    def possible_moves_current_player(self):
        moves = list()
        empty_corners = self.find_empty_corners(self.players_turn)

        for piece_num in self.player_pieces_left[self.players_turn - 1]:
            piece = pieces[piece_num]
            piece = self._change_piece_colour(piece)
            if piece_num == 0 or piece_num == 7 or piece_num == 20:
                for h in range(self.height - piece.shape[0] + 1):
                    for w in range(self.width - piece.shape[1] + 1):
                        if self._check_move(piece, (h, w), empty_corners):
                            moves.append((piece_num, piece, (h, w)))
            elif piece_num == 1 or piece_num == 2 or \
                    piece_num == 4 or piece_num == 9:
                for rotation in range(2):
                    rot_piece = np.rot90(piece, rotation)
                    for h in range(self.height - rot_piece.shape[0] + 1):
                        for w in range(self.width - rot_piece.shape[1] + 1):
                            if self._check_move(rot_piece, (h, w),
                                                empty_corners):
                                moves.append((piece_num, rot_piece, (h, w)))
            else:
                for rotation in range(4):
                    rot_piece = np.rot90(piece, rotation)
                    for h in range(self.height - rot_piece.shape[0] + 1):
                        for w in range(self.width - rot_piece.shape[1] + 1):
                            if self._check_move(rot_piece, (h, w),
                                                empty_corners):
                                moves.append((piece_num, rot_piece, (h, w)))
        return moves

    # Returns the board after making a move
    # Does NOT check if move is possible
    def board_after_move(self, piece_num, piece, anchor):
        board_copy = copy.deepcopy(self.board)
        for h in range(piece.shape[0]):
            for w in range(piece.shape[1]):
                hm = h + anchor[0]
                wm = w + anchor[1]
                if piece[h][w] != 0:
                    board_copy[hm][wm] = self.players_turn
        return board_copy

    def commit_move(self, piece_num, piece, anchor):
        empty_corners = self.find_empty_corners(self.players_turn)
        if self._check_move(piece, anchor, empty_corners):
            for h in range(piece.shape[0]):
                for w in range(piece.shape[1]):
                    hm = h + anchor[0]
                    wm = w + anchor[1]
                    if piece[h][w] != 0:
                        self.board[hm][wm] = self.players_turn
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

    #####################################################################

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
                        for w in range(piece.shape[1]):
                            if piece[h][w] != 0:
                                score += 1
                score = -score
                self.scores[player] = score

        return None

    def _change_piece_colour(self, piece):
        for h in range(piece.shape[0]):
            for w in range(piece.shape[1]):
                if piece[h][w] != 0:
                    piece[h][w] = self.players_turn
        return piece

    # Checks every placement rule for one move
    def _check_move(self, piece, anchor, empty_corners):
        if self._check_at_empty_corner(piece, anchor, empty_corners) and \
                self._check_free_space(piece, anchor) and \
                self._check_placement_rules(piece, anchor):
            return True
        return False

    # Start placement check
    # Checks if one viable empty corner is filled
    def _check_at_empty_corner(self, piece, anchor, empty_corners):
        for h in range(piece.shape[0]):
            for w in range(piece.shape[1]):
                if piece[h][w] == 0:
                    continue
                hm = h + anchor[0]
                wm = w + anchor[1]
                if (hm, wm) in empty_corners:
                    return True
        return False

    # Check if no own stone blocks the placement
    def _check_placement_rules(self, piece, anchor):
        for h in range(piece.shape[0]):
            for w in range(piece.shape[1]):
                hm = h + anchor[0]
                wm = w + anchor[1]
                # In case of the first round
                if piece[h][w] == 0:
                    continue
                if (0 <= hm - 1 < self.height and wm < self.width and
                    self.board[hm - 1][wm] == self.players_turn) or \
                        (hm + 1 < self.height and wm < self.width and
                         self.board[hm + 1][wm] == self.players_turn) or \
                        (hm < self.height and 0 <= wm - 1 < self.width and
                         self.board[hm][wm - 1] == self.players_turn) or \
                        (hm < self.height and wm + 1 < self.width and
                         self.board[hm][wm + 1] == self.players_turn):
                    return False
        return True

    # Checks if all blocks are placed on empty fields
    def _check_free_space(self, piece, anchor):
        for h in range(piece.shape[0]):
            for w in range(piece.shape[1]):
                hm = h + anchor[0]
                wm = w + anchor[1]
                if piece[h][w] != 0 and ((hm < 0 or hm > self.height - 1) or
                                         (wm < 0 or wm > self.width - 1)):
                    return False
                else:
                    if piece[h][w] != 0 and self.board[hm][wm] != 0:
                        return False
        return True
