from collections import Counter
import chess

class Ai:
    def __init__(self, color=-1):
        #-1 for black and 1 for white
        self.color = color

    def minimax(self, board: chess.Board, depth, player=-1):
        if depth == 0 or board.is_game_over():
            return (self.eval(board), None)
        
        moves = board.legal_moves
        #Ai turn(maximize)
        if player == self.color:
            cur_max = float('-inf')
            best_move = None
            for move in moves:
                board.push(move)
                cur = self.minimax(board, depth-1, player=1)
                cur_score = cur[0]
                board.pop()
                if cur_score > cur_max:
                    cur_max = cur_score
                    best_move = move
            return (cur_max, best_move)

        #Player turn(minimize)
        else:
            cur_min = float('inf')
            best_move = None
            for move in moves:
                board.push(move)
                cur = self.minimax(board, depth-1, player=-1)
                cur_score = cur[0]
                board.pop()
                if cur_score < cur_min:
                    cur_min = cur_score
                    best_move = move
            return (cur_min, best_move)

    def eval(self, board):
        pieces = [('p', 10), ('n', 30), ('b', 30), ('r', 50), ('q', 90), ('k', 1000)]
        if self.color == 1:
            pieces = list(map(str.upper, pieces))
        points = 0
        cur_pos = Counter(str(board))
        for piece in pieces:
            points += cur_pos[piece[0]] * piece[1]
        return points
