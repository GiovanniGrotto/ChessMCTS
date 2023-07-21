import os
import chess
import chess.engine


STOCKFISH_ENV_VAR = 'STOCKFISH_EXECUTABLE'


def parse_outcome(outcome):
    winner_str = {True: 'WHITE', False: 'BLACK'}
    if not outcome.winner:
        print(f"DRAW by {outcome.termination.name}")
    else:
        print(f"{winner_str[outcome.winner]} WON by {outcome.termination.name}")


def create_stockfish_engine():
    os.environ[STOCKFISH_ENV_VAR] = "C:/Users/giova/OneDrive/Desktop/SynthBot/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"
    # make sure stockfish environment variable exists
    if STOCKFISH_ENV_VAR not in os.environ:
        raise KeyError(
            'TroutBot requires an environment variable called "{}" pointing to the Stockfish executable'.format(
                STOCKFISH_ENV_VAR))

    # make sure there is actually a file
    stockfish_path = os.environ[STOCKFISH_ENV_VAR]
    if not os.path.exists(stockfish_path):
        raise ValueError('No stockfish executable found at "{}"'.format(stockfish_path))
    # initialize the stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
    return engine


def get_best_stockfish_move(board, time_limit=None, depth_limit=None):
    engine = create_stockfish_engine()
    result = engine.play(board, chess.engine.Limit(time=time_limit, depth=depth_limit))
    del engine
    return result


def score_to_int(score, color):
    if score.relative.score() is None:
        evaluation = 1000 - (10 * score.relative.moves)
    else:
        evaluation = score.relative.score()
    evaluation = evaluation if score.turn == color else (evaluation * -1)
    return evaluation


def is_draw(fen):
    # Questa non deve ritornare pareggio per materiale, quello lo fa già board.outcome()
    # Questa deve detectare situazioni di pareggio chiaro, re e regine, re e 1 pedone a testa e simili
    # Controlla se lo fa effettivamente, sembra di no

    # Split the FEN string to extract the board position
    board = fen.split()[0]

    # Check if only kings are present on the board
    if '/' not in board and 'k' in board and 'K' in board:
        return True

    # Check if any non-king pieces are present on the board
    non_king_pieces = set(['q', 'r', 'b', 'n', 'p', 'Q', 'R', 'B', 'N', 'P'])
    if any(piece in non_king_pieces for piece in board):
        return False

    # Check if there are insufficient mating materials
    material_counts = {piece: board.count(piece) for piece in board}
    if material_counts.get('b', 0) >= 2 or material_counts.get('B', 0) >= 2:
        # More than one bishop on the same color
        return True
    if material_counts.get('n', 0) >= 2 or material_counts.get('N', 0) >= 2:
        # More than one knight
        return True
    if (
        material_counts.get('b', 0) + material_counts.get('B', 0) >= 1 and
        material_counts.get('n', 0) + material_counts.get('N', 0) >= 1
    ):
        # Bishop(s) and knight(s)
        return True

    # Otherwise, it is not a draw
    return False

