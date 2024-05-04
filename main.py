from ai import Ai
import chess
import os


title = """
                                                                                           
  ###    #                   #             ####           ##           #        #          
 #   #   #                   #              #  #           #           #                   
 #      ####    ###    ###   #   #          #  #   ###     #    # ##   # ##    ##    # ##  
  ###    #     #   #  #   #  #  #           #  #  #   #    #    ##  #  ##  #    #    ##  # 
     #   #     #   #  #      ###            #  #  #   #    #    ##  #  #   #    #    #   # 
 #   #   #  #  #   #  #   #  #  #           #  #  #   #    #    # ##   #   #    #    #   # 
  ###     ##    ###    ###   #   #         ####    ###    ###   #      #   #   ###   #   # 
                                                                #                          
                                                                #
"""

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

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


board = chess.Board()
ai = Ai()
di = {'easy': 2, 'mid': 3}

print(title)

try:
    difficulty = di[input("Enter the difficulty(easy/mid): ").strip().lower()]
except:
    difficulty = 3

try:
    hint = int(input("Do you want to get hints(0/1): "))
except:
    hint = 1

print(f'\n{cool_board(board)}')
# player = 1
while not board.is_game_over():
    if hint:
        print(f'Legal moves: {str(board.legal_moves).split()[3:]}\n')
    # print(f'Best move: {(board.variation_san([chess.Move.from_uci(str(ai.eval(board, 1)[0]))]))[1:]}')
    player_move = input('Enter a move: ')
    try:
        board.push_san(player_move)
    except:
        print('Illegal move!\nTry again!')
        continue
    clear_screen()
    best = ai.minimax(board, difficulty)
    print(best)
    board.push(best[1])
    print(f'{cool_board(board)}\n')

results = {'1-0': 'White wins!', '0-1': 'Black wins!', '1/2-1/2': 'It is a draw!'}
print(results[board.result()])
