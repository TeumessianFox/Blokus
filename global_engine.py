import game_state
from GUI.gui import GUI
from random_agent import RandomAgent

color_order = ['blue', 'yellow', 'red', 'green']


class GlobalEngine:
    def __int__(self, player_num, block_size, activate_gui, height, length, window_height, window_length):
        self.player_num = player_num
        self.height = height
        self.length = length

        self.activate_gui = activate_gui
        self.block_size = block_size
        self.window_height = window_height
        self.window_length = window_length

        self.AIs = [None, None, None, None]

        self.state = game_state.GameState(player_num, height, length)

    def play_game(self):
        gui = GUI(self.state, self.block_size)
        self.start_AIs()
        while not self.state.game_over:
            piece_num, piece, anchor = self.pick_move()
            self.commit_move(piece_num, piece, anchor)
            #  update gui
        # gui game end

    # each AI needs to be an own class
    # each AIs start-up function will be called before the game started
    def start_ais(self):
        self.AIs[0] = RandomAgent(1)
        self.AIs[1] = RandomAgent(2)
        self.AIs[2] = RandomAgent(3)
        self.AIs[3] = RandomAgent(4)

    # each AI gets a deepcopy of the game state and has to return piece_num, piece, anchor
    def pick_move(self):
        if self.player_num == 1:
            piece_num, piece, anchor =
        elif self.player_num == 2:
            piece_num, piece, anchor =
        elif self.player_num == 3:
            piece_num, piece, anchor =
        elif self.player_num == 4:
            piece_num, piece, anchor =
        return piece_num, piece, anchor

    def commit_move(self, piece_num, piece, anchor):
        self.state.commit_move(piece_num, piece, anchor)
        return
