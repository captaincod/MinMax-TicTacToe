from LocalBoard import LocalBoard


class GlobalBoard:
    def __init__(self):
        self.field = [[LocalBoard() for i in range(3)] for j in range(3)]
        self.winner = 0

    def check(self, force: bool = False):
        if force:
            for i in range(3):
                for j in range(3):
                    self.field[i][j].check()
        for i in range(3):
            if self.field[0][i].winner > 0:
                if (self.field[0][i].winner == self.field[1][i].winner) and (self.field[0][i].winner == self.field[2][i].winner):
                    self.winner = self.field[0][i].winner
                    return
            if self.field[i][0].winner > 0:
                if (self.field[i][0].winner == self.field[i][1].winner) and (self.field[i][0].winner == self.field[i][2].winner):
                    self.winner = self.field[i][0].winner
                    return
        if self.field[1][1].winner > 0:
            if (self.field[1][1].winner == self.field[0][0].winner) and (self.field[1][1].winner == self.field[2][2].winner):
                self.winner = self.field[1][1].winner
                return
            if (self.field[1][1].winner == self.field[0][2].winner) and (self.field[1][1].winner == self.field[2][0].winner):
                self.winner = self.field[1][1].winner
                return
        boards_to_play_left = 9
        for i in range(3):
            for j in range(3):
                if self.field[i][j].winner != 0:
                    boards_to_play_left -= 1
        if boards_to_play_left == 0:
            self.winner = 3