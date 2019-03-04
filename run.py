import argparse
from global_engine import GlobalEngine
import numpy as np
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--game_num', type=int,
                        default=1, help='Number of games')
    parser.add_argument('-p', '--players', nargs='+',
                        default=['g', 'f'], help='List of player type')
    parser.add_argument('-g', '--use_gui', type=int,
                        default=1, help='Active output to gui')
    parser.add_argument('-t', '--use_terminal', type=int,
                        default=0, help='Active output to terminal')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    player_wins = [0, 0, 0, 0]
    start_time = time.time()
    for i in range(args.game_num):
        ge = GlobalEngine(4, 40, args.use_gui, args.use_terminal, 20, 20)
        winner = ge.play_game()
        player_wins[winner - 1] += 1
    elapsed_time = time.time() - start_time
    print("\n\nTime elapsed: " + str(elapsed_time))
    max_winner = np.argmax(player_wins)
    print("Player " + str(max_winner + 1) + " has won " +
          str(player_wins[max_winner]/args.game_num * 100) + "%")
