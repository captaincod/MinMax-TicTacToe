from Game import Game
from GlobalBoard import GlobalBoard


class Bot:
    def __init__(self, depth_in_half_moves: int):
        self.depth = depth_in_half_moves

        # коэффициенты для статичной функции оценивания (глубина = 0)

        # метка на локальной доске
        self.local_points = {(0, 1): 2., (1, 0): 2., (1, 2): 2., (2, 1): 2.,
                             (0, 0): 3., (0, 2): 3., (2, 0): 3., (2, 2): 3.,
                             (1, 1): 4.}
        # коэффициент глобальной доски для метки на локальной доске
        # итоговый вес одной поставленной метки = local_points[move] * global_points[move]
        self.local_global = {(0, 1): 1., (1, 0): 1., (1, 2): 1., (2, 1): 1.,
                             (0, 0): 1.5, (0, 2): 1.5, (2, 0): 1.5, (2, 2): 1.5,
                             (1, 1): 2.}
        # метка на глобальной доске (победа на локальной доске)
        # значения этих досок находятся под косвенным влиянием local_points и local_global
        self.global_points = {(0, 1): 32., (1, 0): 32., (1, 2): 32., (2, 1): 32.,
                              (0, 0): 32., (0, 2): 32., (2, 0): 32., (2, 2): 32.,
                              (1, 1): 32.}
        # атака на локальной доске
        self.local_attack = 5
        # максимальная сумма очков за атаку на одной локальной доске
        self.local_attack_max = 12
        # атака на глобальной доске
        self.global_attack = 45.
        # захвачена клетка поля, отправляющая обратно в исходную доску
        self.reference = 3.
        # победа на глобальной доске
        self.game_win = 9000.

    def eval(self, game: Game):
        maximizing = True
        if game.current_player == 2:
            maximizing = False

        legal_moves = game.get_legal_moves()
        # print(legal_moves)
        evaluations = []
        for move in legal_moves:
            game.make_move(move)
            evaluations.append(self.minimax(game, self.depth - 1, -self.game_win, self.game_win, not maximizing))
            game.revert_move()

        # print(evaluations)
        best_move = legal_moves[0]
        best_eval = evaluations[0]
        for i in range(1, len(evaluations)):
            if maximizing:
                if evaluations[i] > best_eval:
                    best_eval = evaluations[i]
                    best_move = legal_moves[i]
            else:
                if evaluations[i] < best_eval:
                    best_eval = evaluations[i]
                    best_move = legal_moves[i]
        return best_move

    def minimax(self, game: Game, depth: int, alpha: float, beta: float, maximizingPlayer: bool):
        if depth < 1 or game.board.winner != 0:
            return self.static(game.board)

        legal_moves = game.get_legal_moves()
        if maximizingPlayer:
            maxEval = -self.game_win
            for move in legal_moves:
                game.make_move(move)
                eval = self.minimax(game, depth - 1, alpha, beta, False)
                game.revert_move()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = self.game_win
            for move in legal_moves:
                game.make_move(move)
                eval = self.minimax(game, depth - 1, alpha, beta, True)
                game.revert_move()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def static(self, global_board: GlobalBoard):
        result = self.game_win * self.__k(global_board.winner)
        if result != 0:
            return result
        for i in range(3):
            for j in range(3):
                result += self.reference * self.__k(global_board.field[i][j].field[i][j])
                result += self.global_points[(i, j)] * self.__k(global_board.field[i][j].winner)
                for k in range(3):
                    for l in range(3):
                        result += self.local_points[(k, j)] * self.local_global[(i, j)] * self.__k(
                            global_board.field[i][j].field[k][l])
        # поиск атак - до победы на глобальной или локальной доске нехватает одного хода
        for i in range(3):
            result += self.__atk(
                self.__k(global_board.field[0][i].winner) + self.__k(global_board.field[1][i].winner) + self.__k(
                    global_board.field[2][i].winner), self.global_attack)
            result += self.__atk(
                self.__k(global_board.field[i][0].winner) + self.__k(global_board.field[i][1].winner) + self.__k(
                    global_board.field[i][2].winner), self.global_attack)
        result += self.__atk(
            self.__k(global_board.field[0][0].winner) + self.__k(global_board.field[1][1].winner) + self.__k(
                global_board.field[2][2].winner), self.global_attack)
        result += self.__atk(
            self.__k(global_board.field[0][2].winner) + self.__k(global_board.field[1][1].winner) + self.__k(
                global_board.field[2][0].winner), self.global_attack)
        # максимальный вес за атаки на локальной доске ограничен
        temp = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    temp += self.__atk(self.__k(global_board.field[i][j].field[0][k]) + self.__k(
                        global_board.field[i][j].field[1][k]) + self.__k(global_board.field[i][j].field[2][k]),
                                       self.local_attack)
                    temp += self.__atk(self.__k(global_board.field[i][j].field[k][0]) + self.__k(
                        global_board.field[i][j].field[k][1]) + self.__k(global_board.field[i][j].field[k][2]),
                                       self.local_attack)
                temp += self.__atk(self.__k(global_board.field[i][j].field[0][0]) + self.__k(
                    global_board.field[i][j].field[1][1]) + self.__k(global_board.field[i][j].field[2][2]),
                                   self.local_attack)
                temp += self.__atk(self.__k(global_board.field[i][j].field[0][2]) + self.__k(
                    global_board.field[i][j].field[1][1]) + self.__k(global_board.field[i][j].field[2][0]),
                                   self.local_attack)
                result += min(max(temp, -self.local_attack_max), self.local_attack_max)
        return result

    def __k(self, player: int):
        return {
            player == 0: 0,
            player == 1: 1,
            player == 2: -1,
            player == 3: 0
        }[True]

    def __atk(self, temp: int, add: float):
        if temp == 2:
            return add
        elif temp == -2:
            return -add
        return 0