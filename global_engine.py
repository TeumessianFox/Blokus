import game_state
import copy
# from GUI.gui import GUI
from random_agent import RandomAgent

color_order = ['blue', 'yellow', 'red', 'green']


class GlobalEngine:
    def __init__(self, player_num, block_size, activate_gui,
                 height, length, window_height, window_length):
        self.player_num = player_num
        self.height = height
        self.length = length

        self.activate_gui = activate_gui
        self.block_size = block_size
        self.window_height = window_height
        self.window_length = window_length

        self.AIs = list()

        self.state = game_state.GameState(player_num, height, length)

    def play_game(self):
        # gui = GUI(self.state, self.block_size)
        self.start_ais()
        while not self.state.game_over:
            move = self.pick_move()
            piece_num, piece, anchor = move
            self.commit_move(piece_num, piece, anchor)
            #  update gui
        # gui game end
        print("Game_Over")
        print(self.state.scores)

    # each AI needs to be an own class
    # each AIs start-up function will be called before the game started
    def start_ais(self):
        self.AIs.append(RandomAgent(1))
        self.AIs.append(RandomAgent(2))
        self.AIs.append(RandomAgent(3))
        self.AIs.append(RandomAgent(4))
        print("AIs started!")

    # each AI gets a deepcopy of the game state
    # has to return piece_num, piece, anchor
    def pick_move(self):
        state_copy = copy.deepcopy(self.state)
        move = self.AIs[self.player_num - 1].choose_move(state_copy)
        return move

    def commit_move(self, piece_num, piece, anchor):
        self.state.commit_move(piece_num, piece, anchor)
        print(self.state)


if __name__ == '__main__':
    ge = GlobalEngine(4, 20, 0, 20, 20, 400, 400)
    ge.play_game()
