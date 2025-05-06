import time
import math

class MCTSNode:
    def __init__(self, hand, board, parent=None, scenario=None):
        self.hand = hand
        self.board = board
        self.parent = parent
        self.scenario = scenario
        self.visits = 0
        self.wins = 0
        self.children = {}
        
    def ucb1(self, c=1.414):
        """
        Calculate the UCB1 value for the node (default c = sqrt(2))
        """
        if self.visits == 0:
            return float('inf')
        
        exploitation = self.wins / self.visits
        # For root node, there's no parent for the exploration term
        if self.parent is None:
            return exploitation
            
        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration
    
    def select_child(self, c=1.414):
        """
        Select the child node with the highest UCB1 value
        """
        if not self.children:
            return self
        return max(self.children.values(), key=lambda n: n.ucb1(c))


class PokerBot:
    def __init__(self, hand, board, deck, evaluator):
        self.hand = hand
        self.board = board
        self.deck = deck
        self.evaluator = evaluator
        self.root = MCTSNode(hand, board)
        
    def generate_scenario(self):
        """
        Generate a random possible rollout scenario
        """
        if not self.deck or len(self.deck.cards) < 2:
            return None
        
        # Create a copy to avoid messing up the deck
        deck_copy = self.deck.copy()
        deck_copy.shuffle()
        
        # Generate opponent's hand
        op_hand = deck_copy.deal(2)
        
        # Generate remaining board cards if needed
        needed = 5 - len(self.board)
        new_board = deck_copy.deal(needed) if needed > 0 else []
        
        return (op_hand, new_board)
        
    def select(self):
        """
        Navigate from root to a leaf node by picking the best children
        """
        node = self.root
        
        # While the node has children, select the best child according to UCB1
        while node.children:
            node = node.select_child()
        
        return node
        
    def expand(self, node):
        """
        Ccreate a new child node with a random rollout scenario
        """
        scenario = self.generate_scenario()
        if scenario is None:
            return node  # Cannot expand
            
        # Check if this scenario is already explored
        scenario_key = hash((frozenset(scenario[0]), frozenset(scenario[1])))
        if scenario_key in node.children:
            return node.children[scenario_key]
            
        # Create a new child node
        child = MCTSNode(
            hand=node.hand,
            board=node.board,
            parent=node,
            scenario=scenario
        )
        node.children[scenario_key] = child
        
        return child
    
    def simulate(self, node):
        """
        Determine the outcome of the scenario (win/loss) using hand evaluator
        """
        # If the node doesn't have a scenario (root), generate one
        scenario = node.scenario
        if scenario is None:
            scenario = self.generate_scenario()
            if scenario is None:
                return 0  # Default to a loss if no valid scenario
                
        op_hand, new_board = scenario

        # Evaluate who wins
        result, _, _ = self.evaluator.compare_hands(self.hand, op_hand, self.board + new_board)
        return 1 if result == 1 else 0
        
    def backpropagate(self, node, result):
        """
        Update stats (wins/visits) for all nodes along the path to root
        """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent
            
    def search(self, time_limit=10):
        """
        Run MCTS for the given time limit (default 10 seconds)
        """
        start_time = time.time()
        simulations = 0
        
        while time.time() - start_time < time_limit:
            leaf = self.select()
            if leaf.visits > 0: # expand only if node has been visited before
                leaf = self.expand(leaf)
            result = self.simulate(leaf)
            self.backpropagate(leaf, result)
            simulations += 1
            
        # Calculate win probability based on root node stats
        win_prob = self.root.wins / self.root.visits if self.root.visits > 0 else 0
        print(f"Completed {simulations} MCTS simulations in {time.time() - start_time:.2f} seconds")
        print(f"Win probability: {win_prob:.4f} ({self.root.wins}/{self.root.visits})")
        
        return win_prob

    def make_decision(self, time_limit=10, threshold=0.5):
        """
        Decide whether to fold or stay based on win probability
        """
        print(f"My hand: {self.root.hand}")
        print(f"Board cards: {self.root.board}")
        
        win_prob = self.search(time_limit=time_limit)
        
        # Make decision based on the threshold
        decision = "STAY" if win_prob >= threshold else "FOLD"
        print(f"Decision: {decision}")

        return decision
