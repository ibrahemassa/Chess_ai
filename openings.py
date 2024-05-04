import os
import json
import chess.pgn
import collections

def get_data():
    openings = collections.defaultdict(int)
    def parse_database(path):
        nonlocal openings
        with open(path) as db:
            game = chess.pgn.read_game(db)
            while game:
                board = game.board()
                for move in game.mainline_moves():
                    openings[board.fen()] += 1
                    board.push(move)
                game = chess.pgn.read_game(db)

    for data_set in os.listdir('./data_sets'):
        data_set = os.path.join('./data_sets', data_set)
        try:
            parse_database(data_set)
        except:
            continue
    
    return openings

def write_data(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)

def load_data(path):
    with open(path, 'r') as file:
        return json.load(file)

