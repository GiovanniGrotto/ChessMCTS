from MctsNode import MctsNode
from StockfishEvalRolloutMcts import StockfishEvalRolloutMcts
from StokfishRolloutMcts import StockfishRolloutMctsNode
import random
from multiprocessing import Pool
import chess
import time


def explore_tree(root, node_class):
    exec_time = []
    for _ in range(400):
        start = time.time()
        node = root.explore()
        if node.N != 0:
            node.add_children(node_class)
            node = random.choice(list(node.children.values()))
        reward = node.rollout()
        node.backpropagation(reward)
        exec_time.append(time.time()-start)
    print(f"Medium time for every iteration: {sum(exec_time)/len(exec_time)}")
    return root


def find_best_node(node):
    children = node.children
    max_key = max(children.items(), key=lambda item: (item[1].N, item[1].T))[0]
    max_key_relative = max(children.items(), key=lambda item: (item[1].T/item[1].N))[0]
    print(children[max_key].move)
    print(children[max_key_relative].move)
    return children[max_key]


if __name__ == "__main__":
    node_class = StockfishRolloutMctsNode
    board = chess.Board()
    root1 = node_class(board)
    root2 = node_class(board)
    root3 = node_class(board)
    root4 = node_class(board)
    root5 = node_class(board)
    root6 = node_class(board)
    start_time = time.time()

    with Pool() as pool:
        result = pool.starmap(explore_tree, [(root1, node_class), (root2, node_class), (root3, node_class)])#, (root4, node_class), (root5, node_class), (root6, node_class)])
    print(f"Program finished in {time.time() - start_time} seconds")
    final_tree = sum(result[1:], result[0])
    best_move = find_best_node(final_tree)
    print("-------------------------------------------------------------")
    """start_time = time.time()
    for root in [root1, root2, root3]:
        res = explore_tree(root, node_class)
    print(f"Program finished in {time.time() - start_time} seconds")
    start_time = time.time()
    res = explore_tree(root3, node_class)
    print(f"Program finished in {time.time() - start_time} seconds")"""
    print()
