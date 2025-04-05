import chess, chess.engine
import chess.svg
import random

# Set this to wherever your chess engine is located
CHESS_ENGINE_PATH = 'C:\Program Files\stockfish\stockfish-windows-x86-64-avx2.exe'

class RandomChess:
    def __init__(self, white_player, black_player):
        self.board = chess.Board()
        self.players = [black_player, white_player]

    def svg_board(self):
        return chess.svg.board(self.board, size=600)

    def is_game_over(self):
        return self.board.is_game_over()

    def end_game(self):
        for player in self.players:
            if isinstance(player, CPUPlayer):
                player.quit()
        return self.board.outcome()
    
    def play_move_uci(self, move):
        self.board.push_uci(move)

    def current_player(self):
        return self.players[self.board.turn]

    def _move_count(self):
        return (self.board.legal_moves.count() + 4) // 5

    def get_moves(self) -> list[chess.Move]:
        available_moves = list(self.board.legal_moves)
        k = self._move_count()
        return random.sample(available_moves, k)

class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def request_move(self, move_list: list[chess.Move], board):
        print(self.name + ', please input your move:')
        for i, move in enumerate(move_list, 1):
            print(f'{i}: {move}')
        while True:
            print('Please input the move number: ', end='')
            s = input()
            try:
                n = int(s)
                if 1 <= n <= len(move_list):
                    return move_list[n - 1]
                else:
                    raise ValueError
            except ValueError:
                print(f'Please enter an integer between 1 to {len(move_list)}.')

class CPUPlayer:
    def __init__(self, name):
        self.name = name
        self.engine = chess.engine.SimpleEngine.popen_uci(CHESS_ENGINE_PATH)

    def request_move(self, move_list: list[chess.Move], board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1), root_moves=move_list)
        return result.move

    def quit(self):
        self.engine.quit()

# white_player = CPUPlayer('White')
# black_player = CPUPlayer('Black')
# game = RandomChess(white_player, black_player)

# while not game.is_game_over():
#     os.system('cls')
#     game.show_board()
#     moves = game.get_moves()
#     played_move = game.current_player().request_move(moves, game.board)
#     game.play_move(played_move)

# game.end_game()
# print(game.board)
# svg_board = chess.svg.board(board=game.board, size=600)
# cairosvg.svg2png(bytestring=svg_board.encode(), write_to='./board.png', output_width=720, output_height=720)