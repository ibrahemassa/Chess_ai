from pieces import *

class Chess:
    def __init__(self) -> None:
        white_pieces = [[Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)], [Pawn(1) for i in range(8)]]
        black_pieces = [[Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)], [Pawn(0) for i in range(8)]]
        self.grid = [[str(piece) for piece in black_pieces[0]],
                    [str(piece) for piece in black_pieces[1]]] + [['_'] * 8] * 4 + [[str(piece) for piece in white_pieces[1]],
                    [str(piece) for piece in white_pieces[0]]]
    
    def print_grid(self):
        for i in self.grid:
            print(i)

    def move(color, piece, move):
        pass

    def checkmate(self):
        pass

