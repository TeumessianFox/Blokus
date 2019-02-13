class ExampleAgent:
    # self.name is required
    def __init__(self, player_id):
        self.player_id = player_id
        self.name = "Crazy fancy name"
        print("____ Bot ready")

    # choose_move function is required
    def choose_move(self, game_state):
        # All possible moves
        all_moves = game_state.next_possible_moves_current_player

        # Check for no possible move
        if len(all_moves) == 0:
            return None

        return None
