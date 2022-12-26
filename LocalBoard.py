class LocalBoard:
    def __init__(self):
        self.field = [[0] * 3 for i in range(3)]
        self.winner = 0

    def check(self):
        for i in range(3):
            if self.field[0][i] > 0:
                if (self.field[0][i] == self.field[1][i]) and (self.field[0][i] == self.field[2][i]):
                    self.winner = self.field[0][i]
                    return
            if self.field[i][0] > 0:
                if (self.field[i][0] == self.field[i][1]) and (self.field[i][0] == self.field[i][2]):
                    self.winner = self.field[i][0]
                    return
        if self.field[1][1] > 0:
            if (self.field[1][1] == self.field[0][0]) and (self.field[1][1] == self.field[2][2]):
                self.winner = self.field[1][1]
                return
            if (self.field[1][1] == self.field[0][2]) and (self.field[1][1] == self.field[2][0]):
                self.winner = self.field[1][1]
                return
        legal_moves_left = 9
        for i in range(3):
            for j in range(3):
                if (self.field[i][j] != 0):
                    legal_moves_left -= 1
        if (legal_moves_left == 0):
            self.winner = 3