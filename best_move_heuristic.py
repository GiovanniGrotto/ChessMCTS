import random
import chess


# Function to calculate the weight of a piece
def calculate_weight(piece):
    # Assign weight values to different pieces
    weights = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
               'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0}
    return weights.get(piece, 0)


# Function to check if a move is a capture move
def is_capture_move(move, board):
    return board.is_capture(move)


# Function to check if a piece is defended
def is_defended_piece(square, board):
    attackers = board.attackers(not board.turn, square)
    return len(attackers) > 0


def is_development_move(move, board):
    piece = board.piece_at(move.from_square)
    if piece is not None and piece.color == board.turn:
        to_square = move.to_square
        if to_square in chess.SquareSet(chess.BB_CENTER):
            return True
        enemy_moves = board.attacks(to_square) & board.occupied_co[
            chess.WHITE if piece.color == chess.BLACK else chess.BLACK]
        if enemy_moves:
            return True
    return False


# Function to determine the best move
def determine_best_move(board, moves):
    capture_moves = []
    escape_moves = []
    development_moves = []

    for move in moves:
        if is_capture_move(move, board):
            if not is_defended_piece(move.to_square, board):
                capture_moves.append(move)
            else:
                start_piece = board.piece_at(move.from_square)
                end_piece = board.piece_at(move.to_square)
                if start_piece and end_piece:
                    if calculate_weight(end_piece.symbol()) > calculate_weight(start_piece.symbol()):
                        capture_moves.append(move)
        elif board.is_check() and not board.is_capture(move):
            escape_moves.append(move)
        elif not board.is_check() and is_development_move(move, board):
            development_moves.append(move)

    if capture_moves:
        # Sort capture moves by piece weight in descending order
        capture_moves.sort(key=lambda move: calculate_weight(board.piece_at(move.from_square).symbol()), reverse=True)
        return capture_moves[0]
    elif escape_moves:
        return random.choice(escape_moves)
    elif development_moves:
        return random.choice(development_moves)
    else:
        return random.choice(list(moves))


def main():
    # Example usage
    board = chess.Board()

    while not board.outcome():
        best_move = determine_best_move(board, board.legal_moves)
        board.push(best_move)
        print("Best move for white:", best_move, end='')
        best_move = determine_best_move(board, board.legal_moves)
        board.push(best_move)
        print(", best move for black:", best_move)
