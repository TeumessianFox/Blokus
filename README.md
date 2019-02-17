# Blokus

Block-us if you can

## Introduction

#### Game Components:
* a board of 400 squares
* 84 pieces in four different colors (21 pieces per color).

Each of the 21 pieces for a color is of a different shape.
There are: 1 piece of only one square, 1 piece of two squares, 2 pieces of three squares, 5 pieces of four squares, and 12 pieces of five squares.

#### Game Play:

Each player chooses a color and places that set of 21 pieces in front of his/her side of the board. The order of play is as follows: blue, yellow, red, green.

The first piece played by each player must cover a corner square.
Each new piece must touch at least one other piece of the same color, but only at the corners. Pieces of the same color cannot be in contact along an edge.
There are no restrictions on how many pieces of different colors may be in contact with each other.
Once a piece has been placed on the board it cannot be moved during subsequent turns.

#### End of the game:

The game ends when all players are blocked from laying down any more of their pieces. This also includes any players who may have placed all of their pieces on the board.

Scores are tallied, and the player with the highest score is the winner.

Each player then counts the number of unit squares in his/her remaining pieces (1 unit square = -1 point).

A player earns +15 points if all his/her pieces have been placed on the board plus 5 additional bonus points if the last piece placed on the board was the smallest piece (one square).


## Installation

1. Download
```
cd ~/git
git clone git@github.com:TeumessianFox/Blokus.git
```

## Play the Game

```
$ cd src
$ python run.py -h
pygame 1.9.4
Hello from the pygame community. https://www.pygame.org/contribute.html
usage: global_engine.py [-h] [-ww WIDTH] [-hh HEIGHT] [-n GAME_NUM]
                        [-kn KO_NUM_TO_WIN] [-p PLAYERS [PLAYERS ...]]
                        [-b BLOCK_SIZE] [-g USE_GUI]

optional arguments:
  -h, --help            show this help message and exit
  -n GAME_NUM, --game_num GAME_NUM
                        Number of games
  -g USE_GUI, --use_gui USE_GUI
                        Active output to gui
  -t USE_TERMINAL, --use_terminal USE_TERMINAL
                        Active output to terminal

# Example: 10 games, no output
$ python run -n 10 -g 0
```

## Workflow

Please follow the [Github Flow](https://guides.github.com/introduction/flow/) in this project.

Open a branch if you want to work on a new feature. As soon as the feature is working, make a pull request. After a review we will push it to the master.

To edit .md files follow [markdown guide](https://guides.github.com/features/mastering-markdown/).

## Coding style

Please follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) coding style.


## Reference

1. http://www.ultraboardgames.com/blokus/game-rules.php

2. https://entertainment.howstuffworks.com/leisure/brain-games/blokus.htm

99. https://open.spotify.com/user/1124279316/playlist/0MJBni0UzdnML1amikx0Rc?si=lkGLwjNyQvC3V_yP5VBOmg


## Authors

[TeumessianFox](https://github.com/TeumessianFox/)
