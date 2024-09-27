

class Player:
    def __init__(self, num):
        self.phase = 1
        self.num = num
        self.cards = []

    def get_id(self):
        return self.num

    def set_cards(self, cards):
        self.cards = cards
