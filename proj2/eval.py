import os
import struct
from deck import Card

class HandEvaluator:
    # Hand types mapping
    HAND_TYPES = {
        1: "High Card",
        2: "One Pair",
        3: "Two Pair",
        4: "Three of a Kind",
        5: "Straight",
        6: "Flush",
        7: "Full House",
        8: "Four of a Kind",
        9: "Straight Flush"
    }
    
    def __init__(self, fname='HandRanks.dat'):
        """
        Initialize the hand evaluator by loading the TwoPlusTwo lookup table
        """
        if not os.path.exists(fname):
            raise FileNotFoundError(f"{fname}")
        
        with open(fname, 'rb') as f:
            # The HandRanks file contains a lookup table of integers (4 bytes)
            self.hand_ranks = list(struct.unpack('I' * (os.path.getsize(fname) // 4), f.read()))
    
    def evaluate_hand(self, cards):
        """
        Evaluate a 7-card poker hand using the loaded lookup table
        """
        # Get numerical values of cards (0-51)
        vals = [Card.get_value(card) for card in cards]
        
        # Ensure we have exactly 7 cards
        if len(vals) != 7:
            raise ValueError(f"Must be 7 cards to evaluate")
        
        # Evaluate the hand using the lookup table
        p = 53  # Starts at index 53
        for c in vals:
            p = self.hand_ranks[p + c]
        
        # Extract the evaluation results
        value = p
        hand_type = value >> 12
        hand_rank = value & 0x00000FFF
        hand_name = HandEvaluator.HAND_TYPES.get(hand_type, "Unknown")

        return (value, hand_rank, hand_type, hand_name)

    def compare_hands(self, hand1, hand2, board):
        """
        Compare two 2-card hands given a 5-card board
        """
        if len(hand1) != 2 or len(hand2) != 2:
            raise ValueError("Each hand must contain exactly 2 cards")
        if len(board) != 5:
            raise ValueError("Board must contain exactly 5 cards")

        eval1 = self.evaluate_hand(hand1 + board)
        eval2 = self.evaluate_hand(hand2 + board)

        if eval1[0] > eval2[0]:
            return 1, eval1, eval2  # Hand 1 wins
        elif eval2[0] > eval1[0]:
            return -1, eval1, eval2  # Hand 2 wins
        else:
            return 0, eval1, eval2  # Tie


# Example usages
if __name__ == "__main__":
    evaluator = HandEvaluator()

    def print_evaluation(hand_name, cards, eval_result):
        print(f"\n{hand_name}:")
        print(f"  Cards: {', '.join(str(c) for c in cards)}")
        print(f"  Hand Type: {eval_result[3]} (Type {eval_result[2]})")
        print(f"  Hand Value: {eval_result[0]}")
        print(f"  Hand Rank: {eval_result[1]}")
    
    # High Card
    high_card = ["As", "5d", "7h", "9c", "Jd", "2s", "3h"]
    high_card_eval = evaluator.evaluate_hand(high_card)
    print_evaluation("High Card", high_card, high_card_eval)
    
    # One Pair
    one_pair = ["As", "Ad", "7h", "9c", "Jd", "2s", "3h"]
    one_pair_eval = evaluator.evaluate_hand(one_pair)
    print_evaluation("One Pair", one_pair, one_pair_eval)
    
    # Two Pair
    two_pair = ["As", "Ad", "7h", "7c", "Jd", "2s", "3h"]
    two_pair_eval = evaluator.evaluate_hand(two_pair)
    print_evaluation("Two Pair", two_pair, two_pair_eval)
    
    # Three of a Kind
    three_kind = ["As", "Ad", "Ah", "9c", "Jd", "2s", "3h"]
    three_kind_eval = evaluator.evaluate_hand(three_kind)
    print_evaluation("Three of a Kind", three_kind, three_kind_eval)
    
    # Straight
    straight = ["As", "Kd", "Qh", "Jc", "Td", "2s", "3h"]
    straight_eval = evaluator.evaluate_hand(straight)
    print_evaluation("Straight", straight, straight_eval)
    
    # Flush
    flush = ["As", "Ks", "Qs", "9s", "2s", "3h", "4d"]
    flush_eval = evaluator.evaluate_hand(flush)
    print_evaluation("Flush", flush, flush_eval)
    
    # Full House
    full_house = ["As", "Ad", "Ah", "Kc", "Kd", "2s", "3h"]
    full_house_eval = evaluator.evaluate_hand(full_house)
    print_evaluation("Full House", full_house, full_house_eval)
    
    # Four of a Kind
    four_kind = ["As", "Ad", "Ah", "Ac", "Jd", "2s", "3h"]
    four_kind_eval = evaluator.evaluate_hand(four_kind)
    print_evaluation("Four of a Kind", four_kind, four_kind_eval)
    
    # Straight Flush
    straight_flush = ["As", "Ks", "Qs", "Js", "Ts", "2h", "3d"]
    straight_flush_eval = evaluator.evaluate_hand(straight_flush)
    print_evaluation("Straight Flush", straight_flush, straight_flush_eval)
