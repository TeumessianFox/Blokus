import random
from pieces import pieces
from operator import itemgetter


class BetterRandomAgent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.name = "Better random Bot"

    def choose_move(self, game_state):
        # All possible moves
        all_moves = game_state.next_possible_moves_current_player

        # Check for no possible move
        if len(all_moves) == 0:
            return None

        # Random shuffle of the moves
        random.shuffle(all_moves)

        # Get scores
        move_scores = list()
        for move in all_moves:
            move_score = self.move_blocks(move)
            move_scores.append((move_score, move))
        choice = max(move_scores, key=itemgetter(0))
        return choice[1]

    def move_blocks(self, move):
        piece = pieces[move[0]]
        blocks = 0
        for h in range(piece.shape[0]):
            for l in range(piece.shape[1]):
                if piece[h][l] != 0:
                    blocks += 1
        return blocks
