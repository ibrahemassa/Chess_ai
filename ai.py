import openings
import chess
import json

class Ai:
    def __init__(self, moves_cache, color=-1):
        #-1 for black and 1 for white
        self.color = color

        self.opening_count = 10
        self.openings_dp = openings.load_data('./data_sets/openings.json')

        self.players = {1: chess.WHITE, -1: chess.BLACK}

        self.moves_cache = moves_cache
        # self.positions_count = positions_count
        
    

    def special(self, board, move):
        extra_score = 0
        conditions = {board.is_en_passant: 4,
                      board.is_capture: 5 + self.get_values()[board.piece_at(move.to_square).symbol().upper()],
                      board.is_castling: 3,
                      board.is_check: 6,
                      board.is_checkmate: 1000,
                      }
        for condition in conditions:
            try:
                if condition(move):
                    extra_score += conditions[condition]
            except:
                if condition:
                    extra_score += conditions[condition]
        return extra_score

    def opening_score(self, board, move):
        if board.fullmove_number <= self.opening_count:
            if board.piece_at(move.to_square).piece_type == chess.KING or board.piece_at(move.to_square).piece_type == chess.ROOK:
                return -1000000
        fen = board.fen()
        if str(fen)[4] != 'k':
            return -1000000
        return 20 + (self.openings_dp[fen]/100) if (self.openings_dp and fen in self.openings_dp) else 0

    def calc_score(self, board, move):
        if board.fullmove_number <= self.opening_count and board.piece_at(move.to_square).piece_type == chess.KING:
            return -1000000
        cur_score = 0
        cur_score += self.special(board, move)
        cur_score -= self.king_safety(board)
        cur_score += self.opening_score(board, move)
        # if self.is_fork(board, move):
            # cur_score += 10
        return cur_score


    def minimax(self, board: chess.Board, depth, player=-1, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or board.is_game_over():
        #or self.repeated(board):
            return (self.eval(board), None)
        
        if board.fen() in self.moves_cache:
            return self.moves_cache[board.fen()]
        
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: board.is_capture(move), reverse=True)
        #Ai turn(maximize)
        if player == self.color:
            cur_max = float('-inf')
            best_move = None
            for move in moves:
                board.push(move)
                if board.is_fivefold_repetition():
                    continue
                cur = self.minimax(board, depth-1, player=-player)
                cur_score = cur[0]
                #if the move results in one of the special conditions it value more points(Advantage for Ai)
                cur_score += self.calc_score(board, move)
                board.pop()
                if cur_score > cur_max:
                    cur_max = cur_score
                    best_move = move
                alpha = max(cur_score, alpha)
                if beta <= alpha:
                    break
            self.moves_cache[board.fen()] = (cur_max, best_move)
            return (cur_max, best_move)

        #Player turn(minimize)
        else:
            cur_min = float('inf')
            best_move = None
            for move in moves:
                board.push(move)
                if board.is_fivefold_repetition():
                    continue
                cur = self.minimax(board, depth-1, player=-player)
                cur_score = cur[0]
                #if the move results in one of the special conditions it value more points(Advantage for Player)
                cur_score += self.calc_score(board, move)
                board.pop()
                if cur_score < cur_min:
                    cur_min = cur_score
                    best_move = move
                beta = min(beta, cur_score)
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
        pieces_val = self.get_values()
        pieces_eval = self.get_pos_values()
        
        points = 0
        for i in range(8):
            for j in range(8):
                piece = board.piece_at(chess.square(j, i))
                if piece and piece.symbol().upper() in pieces_val:
                    piece = piece.symbol().upper()
                    e = pieces_eval[piece][i][j] if self.color == 1 else pieces_eval[piece][7 - i][j]
                    points += pieces_val[piece] + pieces_eval[piece][i][j]
                    # if self.repeated(board):
                        # points -= 100
        points -= self.king_safety(board, self.players[self.color])
        return points

    def get_move(self, board, depth=3):
        return self.minimax(board, depth, player=self.color)[1]
  

###################################################
# def track_pos(self, board):
    #     fen = board.fen()
    #     if fen in self.positions_count:
    #         self.positions_count[board.fen()] += 1
    #     else:
    #         self.positions_count[board.fen()] = 1
    #
    # def repeated(self, board):
    #     return self.positions_count.get(board.fen(), 0) >= 3
    
    # def is_fork(self, board, move):
        # piece = board.piece_at(move.to_square)
        # if piece and piece.piece_type == chess.KNIGHT:
        #     attacked_squ = list(board.attacks(move.to_square))
        #     attacked_pieces = [board.piece_at(square) for square in attacked_squ]
        #     if sum(1 for p in attacked_pieces if p and p.piece_type in [chess.KING, chess.QUEEN, chess.ROOK]) >= 2:
        #         return True
        # return False


