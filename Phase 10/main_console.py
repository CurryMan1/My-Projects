from src.deck import Deck
from src.player import Player
from src.constants import PHASES
from pprint import pprint

class App:
    def __init__(self):
        while True:
            try:
                no_of_players = int(input('Enter the number of players: '))
                break
            except ValueError:
                pass

        self.players = [Player(i) for i in range(no_of_players)]
        
        self.running = True        
        self.deck = Deck()

        self.deal()

    def run(self):        
        while self.running:
            
            for player in self.players:
                print(f"Player {player.get_id()+1}'s turn.")
                print(f"Player is on Phase {player.phase}")
                pprint(player.cards)
                input()

    def deal(self):
        for player in self.players:
            cards = self.deck.get_cards(10)
            player.set_cards(cards)
                        
    
if __name__ == '__main__':
    app = App()
    app.run()
