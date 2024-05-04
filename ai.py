from collections import Counter
import openings
import chess
import json

class Ai:
    def __init__(self, color=-1):
        #-1 for black and 1 for white
        self.color = color
        self.openings_dp = openings.load_data('./data_sets/openings.json')
        
    
    def special(self, board, move):
        extra_score = 0
        conditions = {board.is_en_passant: 4, board.is_capture: 5 + self.get_values()[board.piece_at(move.to_square).symbol().upper()], board.is_castling: 3, board.is_check: 6}
        for condition in conditions:
            try:
                if condition(move):
                    extra_score += conditions[condition]
            except:
                if condition:
                    extra_score += conditions[condition]
        return extra_score

    def is_opening_move(self, board):
        fen = board.fen()
        return self.openings_dp and fen in self.openings_dp

    def minimax(self, board: chess.Board, depth, player=-1, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or board.is_game_over():
            return (self.eval(board), None)
        
        moves = board.legal_moves
        #Ai turn(maximize)
        if player == self.color:
            cur_max = float('-inf')
            best_move = None
            for move in moves:
                board.push(move)
                cur = self.minimax(board, depth-1, player=-player)
                cur_score = cur[0]
                #if the move results in one of the special conditions it value more points(Advantage for Ai)
                cur_score += self.special(board, move)
                cur_score -= self.king_safety(board)
                if board.fullmove_number <= 6:
                    if self.is_opening_move(board):
                        cur_score += 20
                board.pop()
                if cur_score > cur_max:
                    cur_max = cur_score
                    best_move = move
                alpha = max(cur_max, alpha)
                if beta <= alpha:
                    break
            return (cur_max, best_move)

        #Player turn(minimize)
        else:
            cur_min = float('inf')
            best_move = None
            for move in moves:
                board.push(move)
                cur = self.minimax(board, depth-1, player=-player)
                cur_score = cur[0]
                #if the move results in one of the special conditions it value more points(Advantage for Player)
                cur_score += self.special(board, move)
                cur_score -= self.king_safety(board)
                if board.fullmove_number <= 10:
                    if self.is_opening_move(board):
                        cur_score += 20
                board.pop()
                if cur_score < cur_min:
                    cur_min = cur_score
                    best_move = move
                beta = min(beta, cur_min)
                if beta <= alpha:
                    break
            return (cur_min, best_move)

    def king_safety(self, board, side=None):
        # valueOfAttacks * attackWeight[attackingPiecesCount] / 100 
        attack_weight = {0: 0, 1: 0, 2: 50, 3: 75, 4: 88, 5: 94, 6: 97, 7: 99}
        attack_val = {'P': 5,'N': 20, 'B': 20, 'R': 40, 'Q': 80}
        count = 0
        val = 0
        if not side:
            side = not board.turn
        king = board.king(side)
        legal_moves = [move.to_square for move in board.generate_legal_moves(king)]
        squares = chess.SquareSet(legal_moves) | board.attacks(king)
        for square in squares:
            if board.piece_at(square):
                piece = board.piece_at(square)
                if piece.color != side:
                    count += 1 
                    val += attack_val[piece.symbol().upper()]

        score = val * attack_weight[count] / 100
        return score
    
    def get_values(self):
        return {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 1000}

    def get_pos_values(self):
        return {
                    'P': [
                [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
                        ],
                    'N': [
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
                        ],
                    'B': [
                [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
                        ],
                    'R': [
                [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
                    ],
                'Q': [
            [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
                    ],
                'K': [
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
            [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
                    ]
            }

    def eval(self, board):
        # pieces_val = [('P', 10), ('N', 30), ('B', 30), ('R', 50), ('Q', 90), ('K', 1000)]
        pieces_val = self.get_values()
        pieces_eval = self.get_pos_values()
        
        # if self.color == -1:
            # pieces_val = list(map(str.lower, pieces_val))
            # pieces_eval = list(map(str.lower, pieces_eval))
            # pieces_val = {key.lower(): value for key, value in pieces_val.items()}
            # pieces_eval = {key.lower(): value[::-1] for key, value in pieces_eval.items()}
        points = 0
        # cur_pos = Counter(str(board))
        # for piece in pieces_val:
            # points += cur_pos[piece[0]] * piece[1]
        for i in range(8):
            for j in range(8):
                piece = board.piece_at(chess.square(j, i))
                if piece and piece.symbol().upper() in pieces_val:
                    piece = piece.symbol().upper()
                    e = pieces_eval[piece][i][j] if self.color == 1 else pieces_eval[piece][7 - i][j]
                    points += pieces_val[piece] + pieces_eval[piece][i][j]
        points += self.king_safety(board, chess.BLACK)
        return points
