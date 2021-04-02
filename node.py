import numpy as np
from collections import defaultdict
from initiate_battle import Battle

def main():
    """initialize root node"""
    root = MonteCarloTreeSearchNode(state=initial_state)
    selected_node = root.best_action()
    return


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.to_play = to_play  # player whose turn it is 1\-1

        self.state = None  # board state on this node
        self.parent = parent
        self.parent_action = parent_action
        self.children = []  # all legal reachable children

        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._number_of_visits = 0  # number of visits of this node
        self.value_sum = 0  # the total value of this state from all visits
        # self.prior = prior  # prior probability to select this node, PROBABLY USELESS

    def node_value(self):
        # value of this node
        return self.value_sum / self._number_of_visits

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def expand(self):
        """
        From present stance,
        next state is generated depending on the action
        which is carried out.
        All possible children nodes gathered
        :return:
        """
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        """From this state happening simulation of entire game
            return: outcome of the game: 1 for win/ -1 for loss/ 0 tie"""
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        """
        All statistics updated through all traveled nodes
        """        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """
        if no available actions left (all children visited)
        It's becomw fully expanded
        """
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        """
        Out of all children select best child to explore (exploitation + exploitation)
        :param c_param:
        :return:
        """
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        """
        Randomly select move
        :param possible_moves: moves
        :return:
        """
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        """
        Selecting nodes to perform rollout
        :return:
        """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        """This returns best possible move"""
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def get_legal_action(self):
        """
        List of all possible actions
        :return: list
        """
        # todo send list of valid (or usable) moves

    def is_game_over(self):
        """

        :return:
        """
        # todo add condition for game end

    def game_result(self):

    # todo decide use -1/0/1 or use range based of left hp

    def move(self, action: int):
        """
        Change state of game by taking selected move
        :param action: currently in form of integer
        - that select action from list or select movement direction
        :return: new state
        """
    #todo pass into combat_handler to continue