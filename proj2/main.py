from deck import Deck
from eval import HandEvaluator
from bot import PokerBot

if __name__ == "__main__":
    evaluator = HandEvaluator()
    deck = Deck()
    deck.shuffle()
    
    # Deal hole cards to both players
    hand = deck.deal(2)
    op_hand = deck.deal(2)
    
    bot = PokerBot(hand, [], deck, evaluator)
    
    print("=== Pre-Flop Decision ===")
    decision = bot.make_decision(time_limit=10)
    if decision == "FOLD":
        exit(0)
    
    # Deal the flop
    flop = deck.deal(3)
    bot = PokerBot(hand, flop, deck, evaluator)
    
    print("\n=== Pre-Turn Decision ===")
    decision = bot.make_decision(time_limit=10)
    if decision == "FOLD":
        exit(0)
    
    # Deal the turn
    turn = deck.deal(1)
    bot = PokerBot(hand, flop+turn, deck, evaluator)
    
    print("\n=== Pre-River Decision ===")
    decision = bot.make_decision(time_limit=10)
    if decision == "FOLD":
        exit(0)
    
    # Deal the river
    river = deck.deal(1)
    print(f"\nFinal board: {flop+turn+river}")
    print(f"My Hand: {hand}")
    print(f"Opponent's hand: {op_hand}")
     
    # Compare hands and determine winner
    result, my_eval, opp_eval = evaluator.compare_hands(hand, op_hand, flop+turn+river)
    if result == 1:
        print(f"Bot WINS with {my_eval[3]}")
    elif result == -1:
        print(f"Opponent WINS with {opp_eval[3]}")
    else:
        print(f"It's a TIE with {my_eval[3]}")
