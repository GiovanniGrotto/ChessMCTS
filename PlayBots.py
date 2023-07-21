import chess
from utils import parse_outcome
from tqdm import tqdm
from colorama import Fore, Back, Style
import logging


class PlayBots:

    def __init__(self, player1, player2, test_size=None):
        self.player1 = player1
        self.player2 = player2
        self.player1_victories = 0
        self.player2_victories = 0
        self.test_size = test_size

    @staticmethod
    def play(player1, player2, board=None, outcome=False):
        board = chess.Board() if not board else board
        turn = True
        while not board.outcome():
            if turn:
                move = player1.best_move(board)
            else:
                move = player2.best_move(board)
            board.push(move)
            turn = not turn
        if outcome:
            parse_outcome(board.outcome())
        return board.outcome()

    def test_bots(self, board=None):
        if not self.test_size:
            logging.ERROR("No test_size specified, specify it before calling test_bots")
            return
        for _ in tqdm(range(int(self.test_size / 2)), desc=f"{self.player1.name} as WHITE"):
            outcome = self.play(self.player1, self.player2, board)
            if outcome.winner is True:
                self.player1_victories += 1
            elif outcome.winner is False:
                self.player2_victories += 1
        for _ in tqdm(range(int(self.test_size / 2)), desc=f"{self.player2.name} as WHITE"):
            outcome = self.play(self.player2, self.player1, board)
            if outcome.winner is True:
                self.player2_victories += 1
            elif outcome.winner is False:
                self.player1_victories += 1
        self.show_test_results_bars()

    def show_test_results(self):
        print(f"{self.player1.name} WON {self.player1_victories} times \n"
              f"{self.player2.name} WON {self.player2_victories} times \n"
              f"and there was {abs(self.test_size - self.player1_victories)} draws")

    def show_test_results_bars(self):
        print(f"\n{Fore.GREEN}{self.player1.name} {Fore.LIGHTBLACK_EX}VS {Fore.RED}{self.player2.name}")
        wins = self.player1_victories * 65 / self.test_size
        losses = self.player2_victories * 65 / self.test_size
        draws = (self.test_size - self.player1_victories - self.player2_victories) * 65 / self.test_size
        wins_str = f"WINS: {self.player1_victories}"
        losses_str = f"LOSSES: {self.player2_victories}"
        draws_str = f"DRAWS: {self.test_size - self.player1_victories - self.player2_victories}"
        shift_coeff = 1.85
        if wins:
            print(" " * int((wins - len(wins_str)) / shift_coeff) + Fore.GREEN + wins_str + " " * int((wins - len(wins_str)) / shift_coeff), end='')
        if draws:
            print(" " * int((draws - len(losses_str)) / shift_coeff) + Fore.LIGHTBLACK_EX + draws_str + " " * int((draws - len(losses_str)) / shift_coeff), end='')
        if losses:
            print(" " * int((losses - len(draws_str)) / shift_coeff) + Fore.RED + losses_str + " " * int((losses - len(draws_str)) / shift_coeff), end='')
        print()
        print(Fore.GREEN + "█" * int(wins), end='')
        print(Fore.LIGHTBLACK_EX + "█" * int(draws), end='')
        print(Fore.RED + "█" * int(losses))
