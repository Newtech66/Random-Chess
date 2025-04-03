import chess
import random
import os

class Game:
    def __init__(self, white_player, black_player):
        self.board = chess.Board()
        self.players = [white_player, black_player]
        self.turn = 0 # 0 is white, 1 is black
    
    def show_board(self):
        print(self.board)
    
    def is_game_over(self):
        return self.board.is_game_over()
    
    def outcome(self):
        return self.board.outcome()
    
    def play_move(self, move):
        self.board.push(move)
        self.turn ^= 1
    
    def current_player(self):
        return self.players[self.turn]
    
    def _move_count(self):
        return (self.board.legal_moves.count() + 4) // 5
    
    def get_moves(self):
        available_moves = list(self.board.legal_moves)
        k = self._move_count()
        return random.sample(available_moves, k)

class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    def request_move(self, move_list: list[chess.Move]):
        print(self.name + ', please input your move:')
        for i, move in enumerate(move_list, 1):
            print(f'{i}: {move}')
        print('Please input the move number: ', end='')
        n = int(input())
        return move_list[n - 1]
            
    
white_player = HumanPlayer('White')
black_player = HumanPlayer('Black')
game = Game(white_player, black_player)

while not game.is_game_over():
    os.system('cls')
    game.show_board()
    moves = game.get_moves()
    played_move = game.current_player().request_move(moves)
    game.play_move(played_move)

outcome = game.outcome()
if not outcome.winner:
    print(f'The game has been drawn.')
else:
    print(f'{white_player.name if outcome.winner else black_player.name} wins by {outcome.termination.name}!')