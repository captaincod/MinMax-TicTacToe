from GlobalBoard import GlobalBoard


class Game:
    def __init__(self):
        self.board = GlobalBoard()
        self.next_board = None
        self.moves = []
        self.current_player = 1
        self.next_player = 2

    def make_move(self, move: tuple):
        self.moves.append(move)
        self.board.field[move[0]][move[1]].field[move[2]][move[3]] = self.current_player
        self.current_player, self.next_player = self.next_player, self.current_player
        self.board.field[move[0]][move[1]].check()
        self.board.check()
        self.__set_next_board()

    def revert_move(self):
        move = self.moves.pop()
        self.board.field[move[0]][move[1]].field[move[2]][move[3]] = 0
        self.current_player, self.next_player = self.next_player, self.current_player
        self.board.field[move[0]][move[1]].winner = 0
        self.board.winner = 0
        self.__set_next_board()

    def is_legal_move(self, move: tuple):
        if self.board.winner != 0:
            return False
        if not isinstance(move, tuple):
            return False
        if len(move) != 4:
            return False
        for i in range(4):
            if not isinstance(move[i], int):
                return False
            if move[i] < 0 or move[i] > 2:
                return False
        if self.next_board is None:
            if self.board.field[move[0]][move[1]].winner != 0:
                return False
        elif self.next_board != (move[0], move[1]):
            return False
        if self.board.field[move[0]][move[1]].field[move[2]][move[3]] != 0:
            return False
        return True

    def get_legal_moves(self):
        legal_moves = []
        if (self.next_board is None):
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for l in range(3):
                            if self.board.field[i][j].winner == 0 and self.board.field[i][j].field[k][l] == 0:
                                legal_moves.append((i, j, k, l))
        else:
            for i in range(3):
                for j in range(3):
                    if self.board.field[self.next_board[0]][self.next_board[1]].field[i][j] == 0:
                        legal_moves.append((self.next_board[0], self.next_board[1], i, j))
        return legal_moves

    def print(self):
        print("Текущая позиция:")
        print("     0       1       2  ")
        print("   0 1 2   0 1 2   0 1 2", end="")
        for i in range(3):
            for j in range(3):
                print(f"\n{j}|", end="")
                for k in range(3):
                    for l in range(3):
                        if self.is_legal_move((i, k, j, l)):
                            print(" ░", end="")
                        else:
                            print(f" {self.int_to_char(self.board.field[i][k].field[j][l])}", end="")
                    if k != 2:
                        print(" |", end="")
                if j == 1:
                    print(" ", i, end="")
            if i != 2:
                print("\n   ------+-------+------", end="")
        print("\n")

    def int_to_char(self, x: int):
        return {
            x == 0: " ",
            x == 1: "X",
            x == 2: "O",
            x == 3: "D"
        }[True]

    def __set_next_board(self):
        self.next_board = None
        if len(self.moves) > 0:
            move = self.moves[-1]
            if self.board.field[move[2]][move[3]].winner == 0:
                self.next_board = (move[2], move[3])