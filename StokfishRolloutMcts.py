from copy import deepcopy
import chess
from utils import create_stockfish_engine
from MctsNode import MctsNode
from utils import score_to_int
from best_move_heuristic import determine_best_move

class StockfishRolloutMctsNode(MctsNode):

    def rollout(self):
        if self.done:
            return 0
        tot_reward = 0
        done = False
        new_board = deepcopy(self.board)
        engine = create_stockfish_engine()
        # engine.configure({"Skill Level": 1})
        color = 'WHITE' if new_board.turn else 'BLACK'
        cont = 0
        while not done and new_board.legal_moves:
            #result = engine.play(new_board, chess.engine.Limit(time=0.01))
            result = determine_best_move(new_board, new_board.legal_moves)
            new_board.push(result)
            if new_board.outcome():
                new_board.pop()
                info = engine.analyse(new_board, chess.engine.Limit(time=0.1))
                tot_reward += score_to_int(info['score'], new_board.turn)
                done = True
            if cont == 50:
                info = engine.analyse(new_board, chess.engine.Limit(time=0.1))
                tot_reward += score_to_int(info['score'], new_board.turn)
                done = True
            cont += 1
        engine.quit()
        return tot_reward
