from game_state import GameState
import random

class RandomAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def choose_move(self, game_state):
        all_moves = game_state.possible_move()
        choice = random.choice(all_moves)
        return choice