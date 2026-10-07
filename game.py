from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    player_has_capture,
    has_capture
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))
    
    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()
            raw = input(f"{self.player}> ").strip().lower().split()
            if raw == ["q"]:
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)
            forced_capture = player_has_capture(self.board, self.player)

            if forced_capture and not capture_move(self.board, self.player, start, end):
                print("You must capture.")
                continue

            if capture_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)

                promoted = promote(self.board)

                if (end[0], end[1]) in promoted:
                    print(f"{self.player} promoted to king.")
                else:
                    print(f"{self.player} captured a piece.")

                if (end[0], end[1]) in promoted:
                    self.player = "B" if self.player == "R" else "R"
                    continue

                if has_capture(self.board, self.player, end):
                    continue

                self.player = "B" if self.player == "R" else "R"

            elif simple_move(self.board, self.player, start, end):
                if forced_capture:
                    print("You must capture.")
                    continue

    def has_pieces(self, player):
        return any(cell in (player, player + "K") for row in self.board for cell in row)

    def has_legal_move(self, player):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] not in (player, player + "K"):
                    continue

                start = (r, c)

                for er in range(SIZE):
                    for ec in range(SIZE):
                        end = (er, ec)

                        if capture_move(self.board, player, start, end):
                            return True

                        if simple_move(self.board, player, start, end):
                            return True

        return False