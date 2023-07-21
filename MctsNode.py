import math
from copy import deepcopy
import random


C = 1


class MctsNode:

    def __init__(self, board, parent=None, move=None, done=False, N=0, T=0, children=None):
        self.parent = parent
        self.children = children
        self.T = T
        self.N = N
        self.move = move
        self.board = board
        self.done = done

    def __str__(self, level=0):
        ret = "   " * level + repr(self) + "\n"
        if self.children:
            for child in self.children.values():
                ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return f"N: {self.N}, T: {self.T}, move: {self.move}"

    def __add__(self, other):
        if isinstance(other, type(self)):
            # Perform the summation of N and T parameters
            summed_N = self.N + other.N
            summed_T = self.T + other.T
            if self.children and other.children:
                # Recursively sum the children lists
                summed_children = {
                    child.move: child + other.children[child.move]
                    for child in self.children.values()
                    if child.move in other.children
                }
            elif self.children and not other.children:
                summed_children = self.children
            elif not self.children and other.children:
                summed_children = other.children
            else:
                summed_children = None
            # Create a new instance of SomeObject with the summed values and children
            return type(self)(board=self.board, parent=self.parent, move=self.move, N=summed_N, T=summed_T, children=summed_children)
        else:
            # Raise an exception if the addition is not supported
            raise TypeError("Unsupported operand type for +")

    def ucb_score(self):
        if self.N == 0:
            return float('inf')
        top_node = self
        if top_node.parent:
            top_node = top_node.parent
        score = (self.T / self.N)/1000 + (C * (math.sqrt(math.log(top_node.N) / self.N)))

        return score

    def add_children(self, node_class):
        self.children = dict()
        for move in self.board.legal_moves:
            new_board = deepcopy(self.board)
            new_board.push(move)
            done = True if new_board.outcome() else False
            child = node_class(new_board, self,  move, done)
            self.children[move] = child

    def explore(self):
        node = self
        while node.children:
            move_ucb_score = {key: value.ucb_score() for key, value in node.children.items()}
            max_value = max(move_ucb_score.values())
            node_with_max_value = [key for key, value in move_ucb_score.items() if value == max_value]
            random_max_node = random.choice(node_with_max_value)
            node = node.children[random_max_node]
        return node

    def rollout(self):
        if self.done:
            return 0
        tot_reward = 0
        done = False
        new_board = deepcopy(self.board)
        color = 'WHITE' if new_board.turn else 'BLACK'
        while not done and new_board.legal_moves:
            move = random.choice(list(new_board.legal_moves))
            new_board.push(move)
            reward = 0
            if new_board.outcome() and not new_board.outcome().winner:
                reward = 0.5
                done = True
            elif new_board.outcome() and new_board.outcome().winner == color:
                reward = 1
                done = True
            elif new_board.outcome() and new_board.outcome().winner != color:
                reward = -1
                done = True
            tot_reward += reward
        return tot_reward

    def backpropagation(self, reward):
        node = self
        while node.parent:
            node.T += reward
            node.N += 1
            node = node.parent
        node.T += reward
        node.N += 1