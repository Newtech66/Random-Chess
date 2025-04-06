import chess, chess.engine
import chess.svg
import random

# Set this to wherever your chess engine is located
CHESS_ENGINE_PATH = 'C:\Program Files\stockfish\stockfish-windows-x86-64-avx2.exe'

class RandomChess:
    def __init__(self, white_player=None, black_player=None):
        self.board = None
        self.players = [black_player, white_player]
    
    def add_white(self, white_player):
        if self.players[1] is not None:
            raise ValueError('White player already exists.')
        self.players[1] = white_player

    def add_black(self, black_player):
        if self.players[1] is not None:
            raise ValueError('Black player already exists.')
        self.players[1] = black_player

    def init_game(self):
        if self.board is not None:
            raise ValueError('Game has already begun.')
        self.board = chess.Board()

    def svg_board(self):
        if self.board is None:
            raise ValueError('Game has not begun.')
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

class CPUPlayer:
    def __init__(self, name):
        self.name = name
        self.engine = chess.engine.SimpleEngine.popen_uci(CHESS_ENGINE_PATH)

    def request_move(self, move_list: list[chess.Move], board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1), root_moves=move_list)
        return result.move

    def quit(self):
        self.engine.quit()
