# 0 is black and 1 is white
class Piece:
    def __init__(self, color, symbols, value=0):
        if color:
            self.symbol = symbols[1]
        else:
            self.symbol = symbols[0]
        self.value = value

    def __str__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, ('♙', '♟'), 1.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, ('♘', '♞'), 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, ('♗', '♝'), 3.1)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, ('♖', '♜'), 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, ('♕', '♛'), 9.0)


class King(Piece):
    def __init__(self, color):
        super().__init__(color, ('♔', '♚'), float('inf'))
