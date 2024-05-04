from collections import Counter
import chess

class Ai:
    def __init__(self, color=-1):
        #-1 for black and 1 for white
        self.color = color
    
    def special(self, board, move):
        extra_score = 0
        conditions = {board.is_en_passant: 4, board.is_capture: 5, board.is_castling: 3, board.is_check: 6}
        for condition in conditions:
            try:
                if condition(move):
                    extra_score += conditions[condition]
            except:
                if condition:
                    extra_score += conditions[condition]
        return extra_score

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
                board.pop()
                if cur_score < cur_min:
                    cur_min = cur_score
                    best_move = move
                beta = min(beta, cur_min)
                if beta <= alpha:
                    break
            return (cur_min, best_move)

    def eval(self, board):
        # pieces_val = [('P', 10), ('N', 30), ('B', 30), ('R', 50), ('Q', 90), ('K', 1000)]
        pieces_val = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 1000}
        pieces_eval = {
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
                    e = pieces_eval[piece][i][j] if self.color == 1 else pieces_eval[piece][::-1][i][j]
                    points += pieces_val[piece] + pieces_eval[piece][i][j]

            # square = chess.square(file, rank)
            # piece = board.piece_at(square)
        return points
