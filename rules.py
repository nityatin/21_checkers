SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if board[er][ec] != ".":
        return False

    row_change = er - sr
    col_change = abs(ec - sc)

    if col_change != 1:
        return False

    piece = board[sr][sc]

    if piece == player + "K":
        return abs(row_change) == 1

    direction = -1 if player == "R" else 1
    return row_change == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    piece = board[sr][sc]

    if piece != player and piece != player + "K":
        return False

    if piece != player + "K":
        direction = -1 if player == "R" else 1
        if er - sr != 2 * direction:
            return False

    mr = (sr + er) // 2
    mc = (sc + ec) // 2

    return board[mr][mc] not in (".", player, player + "K")


def has_capture(board, player, start):
    for er in range(SIZE):
        for ec in range(SIZE):
            if capture_move(board, player, start, (er, ec)):
                return True

    return False


def player_has_capture(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] in (player, player + "K"):
                if has_capture(board, player, (r, c)):
                    return True

    return False


def promote(board):
    promoted = []

    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append((0, c))

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append((SIZE - 1, c))

    return promoted