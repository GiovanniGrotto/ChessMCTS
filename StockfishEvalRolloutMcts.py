from MctsNode import MctsNode
from copy import deepcopy
from utils import create_stockfish_engine, score_to_int, is_draw
import chess
import random


class StockfishEvalRolloutMcts(MctsNode):

    def rollout(self):
        if self.done:
            return 0
        tot_reward = 0
        done = False
        new_board = deepcopy(self.board)
        engine = create_stockfish_engine()
        color = new_board.turn
        cont = 0
        # One rollout politics
        """while not done and new_board.legal_moves:
            move = random.choice(list(new_board.legal_moves))
            new_board.push(move)
            evaluation = 0
            if cont == 80 or new_board.outcome():
                info = engine.analyse(new_board, chess.engine.Limit(time=0.1))
                evaluation = score_to_int(info['score'], color)
            if new_board.outcome() or abs(tot_reward) > 10000 or is_draw(new_board.fen()):
                done = True
            tot_reward += evaluation
            cont += 1
        engine.quit()
        return tot_reward"""
        # One other politics
        while not done and new_board.legal_moves:
            move = random.choice(list(new_board.legal_moves))
            new_board.push(move)
            if new_board.outcome():
                new_board.pop()
                info = engine.analyse(new_board, chess.engine.Limit(time=0.1))
                tot_reward += score_to_int(info['score'], color)
                done = True
            if cont == 50:
                info = engine.analyse(new_board, chess.engine.Limit(time=0.1))
                tot_reward += score_to_int(info['score'], color)
                done = True
            cont += 1
        engine.quit()
        return tot_reward
