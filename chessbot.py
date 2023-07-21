from utils import create_stockfish_engine
from Player import Player
from MctsNode import MctsNode
from PlayBots import PlayBots
from Engine import Engine
from StokfishRolloutMcts import StockfishRolloutMctsNode
from StockfishEvalRolloutMcts import StockfishEvalRolloutMcts

stockfish_engine = create_stockfish_engine()
stockfish_engine.configure({"Skill Level": 1})  # UCI_Elo, UCI_LimitStrength per settare elo
vanilla_mcts = Engine(MctsNode)
stockfish_rollout_mcts_engine = Engine(StockfishRolloutMctsNode)
stockfish_eval_rollout_mcts_engine = Engine(StockfishEvalRolloutMcts)
player1 = Player("STOCKFISH", stockfish_engine, time_limit=0.01)
player2 = Player("VANILLA-MCTS", vanilla_mcts, depth_limit=100)
player3 = Player("STOCKFISH", stockfish_engine, depth_limit=1)
player4 = Player("STOCKFISH-ROLLOUT-MCTS", stockfish_rollout_mcts_engine, depth_limit=60)
player5 = Player("STOCKFISH-EVAL-ROLLOUT-MCTS", stockfish_eval_rollout_mcts_engine, depth_limit=100)
play_bots = PlayBots(player2, player5, 10)
play_bots.test_bots()


