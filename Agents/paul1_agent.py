import random
from pieces import pieces
from operator import itemgetter

import helper_func


class Pauls1Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.name = "Paul's Bot 1"
        print("Paul's bot ready")

    def choose_move(self, game_state):
        # All possible moves
        all_moves = game_state.next_possible_moves_current_player

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
            move_score += helper_func.move_blocks(move)

            # Amount of rows and columns covered
            rows_covered_before = helper_func.rows_covered(game_state.board, game_state.players_turn)
            columns_covered_before = helper_func.columns_covered(game_state.board, game_state.players_turn)
            rows_covered_after = helper_func.rows_covered(successor_board, game_state.players_turn)
            columns_covered_after = helper_func.columns_covered(successor_board, game_state.players_turn)
            rows_covered = rows_covered_after - rows_covered_before
            columns_covered = columns_covered_after - columns_covered_before
            move_score += rows_covered
            move_score += columns_covered

            # Own corner difference
            old_corners = len(game_state.find_empty_corners(
                game_state.board, game_state.players_turn))
            new_corners = len(game_state.find_empty_corners(
                successor_board, game_state.players_turn))
            move_score += (new_corners - old_corners)

            # Sum of enemy corners

            # Penetrate

            # Area

            move_scores.append((move_score, move))
        choice = max(move_scores, key=itemgetter(0))
        return choice[1]
