from ai import Ai
import chess
import os

#Makes the board look cooler!
def cool_board(board):
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
    for rank in range(7, -1, -1):
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece:
                color = 'w' if board.color_at(square) == chess.WHITE else 'b'
                result += piece_symbols[piece.piece_type][color] + ' '
            else:
                result += piece_symbols[None] + ' '
        result += '\n'
    return result

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


board = chess.Board()
ai = Ai(color=1)

# player = 1
while not board.is_checkmate():
    print(f'Legal moves: {str(board.legal_moves).split()[3:]}\n')
    # print(f'Best move: {(board.variation_san([chess.Move.from_uci(str(ai.eval(board, 1)[0]))]))[1:]}')
    player_move = input('Enter a move: ')
    try:
        board.push_san(player_move)
    except:
        print('Illegal move!\nTry again!')
        continue
    clear_screen()
    best = ai.minimax(board, 3)
    print(best)
    board.push(best[1])
    print(f'{cool_board(board)}\n')
    # player *= -1
