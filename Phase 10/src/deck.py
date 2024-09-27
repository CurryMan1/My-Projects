import random
from pprint import pprint
from src.constants import COLOURS
from src.utils import pop_multiple


class Deck:
    def __init__(self):
        self.cards = []
        
        self.reset()
        self.shuffle()

    def reset(self):
        #normal cards
        self.cards = [
            colour+str(num+1)
            for colour in COLOURS
            for i in range(2)
            for num in range(12)
        ]+['w' for i in range(8)
        ]+['s' for i in range(4)]

        #pprint(self.cards)
        
    def shuffle(self):
        random.shuffle(self.cards)
        #pprint(self.cards)

    def get_cards(self, num):
        cards = pop_multiple(0, num, self.cards)
        return cards
