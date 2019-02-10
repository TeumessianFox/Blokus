import random


class RandomAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def choose_move(self, game_state):
        all_moves = game_state.possible_moves_current_player()
        if len(all_moves) != 0:
            choice = random.choice(all_moves)
        else:
            choice = None
        return choice
