import random
from operator import itemgetter

import helper_func


class Pauls1Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.name = "Paul's Bot"
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

            # Evaluate successor state after committing this move
            successor_board = game_state.board_after_move(move[0], move[1],
                                                          move[2])

            # Scoring:
            ##################################
            # For every block
            move_score += helper_func.move_blocks(move)

            # First 9 rounds only play moves with more than 5 blocks
            if move_score < 5 and game_state.round < 9:
                move_scores.append((move_score, move))
                continue

            # Amount of rows and columns covered
            if game_state.round < 8:
                rows_covered_before = helper_func.rows_covered(
                    game_state.board, game_state.players_turn)
                columns_covered_before = helper_func.columns_covered(
                    game_state.board, game_state.players_turn)
                rows_covered_after = helper_func.rows_covered(
                    successor_board, game_state.players_turn)
                columns_covered_after = helper_func.columns_covered(
                    successor_board, game_state.players_turn)
                rows_covered = rows_covered_after - rows_covered_before
                columns_covered = columns_covered_after - columns_covered_before
                move_score += rows_covered
                move_score += columns_covered

            old_corners = game_state.find_all_player_empty_corners(
                game_state.board)
            new_corners = game_state.find_all_player_empty_corners(
                successor_board)
            # Own corner difference
            move_score += (len(new_corners[game_state.players_turn - 1])
                           - len(old_corners[game_state.players_turn - 1]))

            # Sum of enemy corners
            enemy_old_corners = 0
            enemy_new_corners = 0
            for enemy in helper_func.other_players_num(
                    game_state.players_turn):
                enemy_old_corners += len(old_corners[enemy - 1])
                enemy_new_corners += len(new_corners[enemy - 1])
            move_score += (enemy_old_corners - enemy_new_corners)

            move_scores.append((move_score, move))
        choice = max(move_scores, key=itemgetter(0))
        return choice[1]
