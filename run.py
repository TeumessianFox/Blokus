import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ww', '--width', type=int, default=20, help='Window width')
    parser.add_argument('-hh', '--height', type=int, default=20, help='Window height')
    parser.add_argument('-n', '--game_num', type=int, default=1, help='Number of games')
    parser.add_argument('-pn', '--player_num', type=int, default=4, help='Number of player')
    parser.add_argument('-p', '--players', nargs='+', default=['g', 'f'], help='List of player type')
    parser.add_argument('-b', '--block_size', type=int, default=30, help='Set block size to enlarge GUI')
    parser.add_argument('-g', '--use_gui', type=int, default=1, help='Active output to gui')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

