import game_state
import copy
import numpy as np
from GUI.gui import GUI
from random_agent import RandomAgent

color_order = ['blue', 'yellow', 'red', 'green']


class GlobalEngine:
    def __init__(self, player_num, block_size, activate_gui,
                 height, width):
        self.player_num = player_num
        self.height = height
        self.width = width

        self.activate_gui = activate_gui
        self.block_size = block_size

        self.AIs = list()

        self.state = game_state.GameState(player_num, height, width)

    def play_game(self):
        if self.activate_gui:
            gui = GUI(self.block_size, self.height, self.width)
            gui.update_screen(self.state)
        self.start_ais()
        while not self.state.game_over:
            move = self.pick_move()
            piece_num, piece, anchor = move
            self.commit_move(piece_num, piece, anchor)
            if self.activate_gui:
                # update gui
                gui.update_screen(self.state)
            else:
                print(self.state)
        # gui game end
        print("Game_Over")
        print(self.state.scores)
        print("Player " + str(np.argmax(self.state.scores) + 1) + " has won!")
        while 1:
            continue

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


if __name__ == '__main__':
    ge = GlobalEngine(4, 40, 1, 20, 20)
    ge.play_game()
