from game_controller import GameController
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
print(title)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

ai = Ai()
game_controller = GameController(ai)
board = chess.Board()
player = game_controller.player

game_controller.print_board(board)

while not board.is_game_over():
    if player == 1:
        game_controller.player_move(board)
        game_controller.ai_move(board)
        clear_screen()
    else:
        clear_screen()
        game_controller.ai_move(board)
        game_controller.print_board(board)
        game_controller.player_move(board)
    game_controller.print_board(board)

results = {'1-0': 'White wins!', '0-1': 'Black wins!', '1/2-1/2': 'It is a draw!'}
print(results[board.result()])
