import random


class Engine:

    def __init__(self, node_class):
        self.node_class = node_class
        self.root = None

    def play(self, board, limit):
        """
        Qui cerchiamo di conservare l'albero precedentemente calcolato, se però non abbiamo mai fatto calcoli sui nodi
        che matchano con la partita in corso inizializziamo una nuova root da 0
        """
        if not self.root:
            self.root = self.node_class(board)
        else:
            pre_calculated_root = [x for x in self.root.children.values() if x.board == board]
            self.root = pre_calculated_root[0] if pre_calculated_root else self.node_class(board)
        explored_tree = self.explore_tree(self.root, limit.depth)
        best_move = self.find_best_node(explored_tree)
        return best_move

    def explore_tree(self, root, limit):
        for _ in range(limit):
            node = root.explore()
            if node.N != 0:
                node.add_children(self.node_class)
                if node.children:
                    node = random.choice(list(node.children.values()))
            reward = node.rollout()
            node.backpropagation(reward)
        return root

    def find_best_node(self, node):
        children = node.children
        max_key = max(children.items(), key=lambda item: (item[1].N, item[1].T))[0]
        self.root = children[max_key]
        del self.root.parent
        self.root.parent = None
        return children[max_key]

