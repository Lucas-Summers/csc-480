import random

class Card:
    RANKS = {
        '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 
        'J': 9, 'Q': 10, 'K': 11, 'A': 12
    }
    SUITS = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
    
    def __init__(self, val):
        """
        Create a card either from a string (e.g., 'As') or integer (0-51)
        """
        self.value = self.get_value(val)

    @staticmethod 
    def get_value(val):
        """
        Returns the integer value of a card (0-51)
        """
        if isinstance(val, str):
            if len(val) != 2:
                raise ValueError(f"Invalid card string: {val}")
            if val[0] not in Card.RANKS:
                raise ValueError(f"Invalid rank: {val[0]}")
            if val[1] not in Card.SUITS:
                raise ValueError(f"Invalid suit: {val[1]}")
            return Card.RANKS[val[0]] * 4 + Card.SUITS[val[1]] + 1
        elif isinstance(val, int):
            if not (1 <= val <= 52):
                raise ValueError(f"Invalid card value: {val}")
            return val
        elif isinstance(val, Card):
            return val.value
        else:
            raise ValueError(f"{type(val)}")

    def __str__(self):
        adj_val = self.value - 1
        rank = list(Card.RANKS.keys())[adj_val // 4]
        suit = list(Card.SUITS.keys())[adj_val % 4]
        return f"{rank}{suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.value == other.value

    def __hash__(self):
        return self.value


class Deck:
    def __init__(self):
        """
        Init a standard deck with all 52 cards
        """
        self.cards = []
        for suit in Card.SUITS.keys():
            for rank in Card.RANKS.keys():
                self.cards.append(Card(f"{rank}{suit}"))

    def shuffle(self):
        """
        Shuffle the deck randomly
        """
        random.shuffle(self.cards)
    
    def deal(self, n=1):
        """
        Deal a specified number of cards from the deck
        """
        if n > len(self.cards):
            raise ValueError(f"Not enough cards in deck to deal")
        
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt

    def copy(self):
        """
        Create a new deck with all the cards in the current deck
        """
        deck = Deck()
        deck.cards = [Card(c.value) for c in self.cards]
        return deck

    def __len__(self):
        return len(self.cards)
