import torch
import mcts
from copy import copy


class Connect4Zero:
    def __init__(self, policy='connect4Zero3000.mypolicy', timeout=20.):
        self.policy = torch.load(policy)
        self.TIMER_THRESHOLD = timeout

    def search(self, game, time_left):
        self.tree = mcts.Node(copy(game))
        self.time_left = time_left

        while True:
            if self.time_left() < self.TIMER_THRESHOLD:
                break

            self.tree.explore(self.policy)
            self.tree_next, _ = self.tree.next(temperature=0.1)

        return self.tree_next.game.last_move[0]