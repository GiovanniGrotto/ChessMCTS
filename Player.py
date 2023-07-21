import chess


class Player:

    def __init__(self, name, engine, time_limit=None, depth_limit=None):
        self.name = name
        if time_limit:
            self.name += f"_{time_limit}sec"
        if depth_limit:
            self.name += f"_depth_{depth_limit}"
        self.engine = engine
        self.time_limit = None if not time_limit else time_limit
        self.depth_limit = None if not depth_limit else depth_limit

    def best_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit, depth=self.depth_limit))
        return result.move
