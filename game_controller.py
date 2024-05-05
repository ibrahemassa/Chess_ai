import chess

class GameController:
    def __init__(self, ai_player):
        self.ai_player = ai_player
        
        di = {'easy': 2, 'mid': 3}

        try:
            self.difficulty = di[input("Enter the difficulty(easy/mid): ").strip().lower()]
        except:
            self.difficulty = 3

        try:
            self.hint = int(input("Do you want to get hints(0/1): "))
        except:
            self.hint = 1

        try:
            self.player = int(input('Do you want to play as white(1)(default) or black(-1): '))
        except:
            self.player = 1

        self.ai_player.color = -self.player


    def player_move(self, board):
        if self.hint:
            print(f'Legal moves: {str(board.legal_moves).split()[3:]}\n')
        # print(f'Best move: {(board.variation_san([chess.Move.from_uci(str(ai.eval(board, 1)[0]))]))[1:]}')
        move = input('Enter a move: ')
        try:
            board.push_san(move)
        except:
            print('Illegal move!\nTry again!')
            self.player_move(board)

    def ai_move(self, board):
        best = self.ai_player.minimax(board, self.difficulty)
        print(best)
        board.push(best[1])


    def cool_board(self, board):
        piece_symbols = {
            chess.PAWN: {'b': '♙', 'w': '♟'},
            chess.KNIGHT: {'b': '♘', 'w': '♞'},
            chess.BISHOP: {'b': '♗', 'w': '♝'},
            chess.ROOK: {'b': '♖', 'w': '♜'},
            chess.QUEEN: {'b': '♕', 'w': '♛'},
            chess.KING: {'b': '♔', 'w': '♚'},
            None: '.'
        }

        result = ""
        ranks = list(range(1, 9))
        files = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '\n']
        for rank in range(7, -1, -1):
            result += f'{ranks[rank]} '
            for file in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece:
                    color = 'w' if board.color_at(square) == chess.WHITE else 'b'
                    result += piece_symbols[piece.piece_type][color] + ' '
                else:
                    result += piece_symbols[None] + ' '
            result += '\n'
        for file in files:
            result += f'{file} '
        return result

    def print_board(self, board):
        print(f'\n{self.cool_board(board)}')


