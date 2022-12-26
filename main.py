from Bot import Bot
from Game import Game

if __name__ == "__main__":
    game = Game()
    bot = Bot(6)
    player_first = True
    move = None
    player_choice = ''
    while player_choice not in ['X', 'Х', '0', 'O', 'О']:
        player_choice = input("Вы за крестики или за нолики? Напишите X или 0: ")
    if player_choice in ['X', 'Х']:
        player_first = True
    elif player_choice in ['0', 'O', 'О']:
        player_first = False

    if player_first:
        while game.board.winner == 0:
            game.print()
            while True:
                print("Сейчас ходят:", game.int_to_char(game.current_player))
                user_input = input("Ход в формате \" y_глобальный x_глобальный y_локальный x_локальный \" : ")
                move = list(int(item) for item in user_input.split())
                move = tuple([move[1], move[0], move[3], move[2]])
                if game.is_legal_move(move):
                    break
            game.make_move(move)

            if game.board.winner != 0:
                break

            game.print()
            print("Сейчас ходят:", game.int_to_char(game.current_player))
            move = bot.eval(game)
            print("Бот сходил на:", move[1], move[0], move[3], move[2])
            game.make_move(move)

    else:
        while game.board.winner == 0:
            game.print()
            print("Сейчас ходят:", game.int_to_char(game.current_player))
            move = bot.eval(game)
            print("Бот сходил на:", move[1], move[0], move[3], move[2])
            game.make_move(move)

            if game.board.winner != 0:
                break

            game.print()
            while True:
                print("Сейчас ходят:", game.int_to_char(game.current_player))
                user_input = input("Ход в формате \" y_глобальный x_глобальный y_локальный x_локальный \" : ")
                move = list(int(item) for item in user_input.split())
                move = tuple([move[1], move[0], move[3], move[2]])
                if game.is_legal_move(move):
                    break
            game.make_move(move)

    game.print()
    print("Игра окончена.")
    print("Победа за:", game.int_to_char(game.board.winner))
