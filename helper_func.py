from pieces import pieces


# Rows covered by a specific player
def rows_covered(board, player):
    rows_covered = 0

    for r in range(board.shape[1]):
        this_row = False
        for c in range(board.shape[0]):
            if board[c][r] == player:
                this_row = True
                break
        if this_row:
            rows_covered += 1

    return rows_covered


# Columns covered by a specific player
def columns_covered(board, player):
    columns_covered = 0

    for c in range(board.shape[0]):
        this_column = False
        for r in range(board.shape[1]):
            if board[c][r] == player:
                this_column = True
                break
        if this_column:
            columns_covered += 1

    return columns_covered


# For a given move returns the number of blocks for the stone
def move_blocks(move):
    piece = pieces[move[0]]
    blocks = 0
    for h in range(piece.shape[0]):
        for l in range(piece.shape[1]):
            if piece[h][l] != 0:
                blocks += 1
    return blocks
