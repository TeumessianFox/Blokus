import random
from pieces import pieces
from operator import itemgetter


class PaulsAgent:
    def __init__(self, player_id):
        self.player_id = player_id
        print("Paul's bot ready")

    def choose_move(self, game_state):
        # All possible moves
        all_moves = game_state.possible_moves_current_player()

        # Check for no possible move
        if len(all_moves) == 0:
            return None

        # Random shuffle of the moves
        random.shuffle(all_moves)

        if game_state.round < 4:
            if game_state.round == 1:
                all_moves = [move for move in all_moves if move[0] == 14]
            elif game_state.round == 2:
                all_moves = [move for move in all_moves if move[0] == 17]
            else:
                all_moves = [move for move in all_moves if move[0] == 19]

        # Get scores
        move_scores = list()
        for move in all_moves:
            move_score = 0

            # Evaluate successor state after commiting this move
            successor_board = game_state.board_after_move(move[0], move[1],
                                                          move[2])

            # Scoring:
            ##################################
            # For every block
            move_score += self.move_blocks(move)

            # Amount of rows and columns covered
            rows_covered_before, columns_covered_before = self.\
                row_columns_covered(game_state.board, game_state.players_turn)
            rows_covered_after, columns_covered_after = self.\
                row_columns_covered(successor_board, game_state.players_turn)
            rows_covered = rows_covered_after - rows_covered_before
            columns_covered = columns_covered_after - columns_covered_before
            move_score += rows_covered
            move_score += columns_covered

            move_scores.append((move_score, move))
        choice = max(move_scores, key=itemgetter(0))
        return choice[1]

    def row_columns_covered(self, board, player):
        rows_covered = 0
        columns_covered = 0

        for r in range(board.shape[1]):
            this_row = False
            for c in range(board.shape[0]):
                if board[c][r] == player:
                    this_row = True
                    break
            if this_row:
                rows_covered += 1

        for c in range(board.shape[0]):
            this_column = False
            for r in range(board.shape[1]):
                if board[c][r] == player:
                    this_column = True
                    break
            if this_column:
                columns_covered += 1

        return rows_covered, columns_covered

    def move_blocks(self, move):
        piece = pieces[move[0]]
        blocks = 0
        for h in range(piece.shape[0]):
            for l in range(piece.shape[1]):
                if piece[h][l] != 0:
                    blocks += 1
        return blocks
