import random
import sys
from collections import Counter, defaultdict
from graphics import *


class Card:
    Ranks = list("23456789TJQKA")
    Suits = list("HDCS")
    Suitsymbol = {"C": chr(9827), "D" : chr(9830), "H" : chr(9829), "S": chr(9824)}

    def __init__(self, rank, suit):
        if not (rank in Card.Ranks) or not (suit in Card.Suits):
            raise ValueError("Check your ranks and suits")
        else:
            self.rank = rank
            self.suit = suit
            self.face_up = False
        
    def __str__(self):
        if self.face_up:
            return str(self.rank) + Card.Suitsymbol[self.suit]
        else:
            return "??"
    
    def draw_face_down(self, win, pt):
        self.height = 2
        self.width = 0.6 * self.height
        self.rect = Rectangle(pt, Point(pt.getX() + self.width, pt.getY() + self.height))
        self.rect.setFill('gray')
        self.rect.draw(win)
        
    
    def draw_face_up(self, win, pt):
        self.height = 2
        self.width = 0.6 * self.height
        self.rect = Rectangle(pt, Point(pt.getX() + self.width, pt.getY() + self.height))
        self.rect.setFill('white')
        self.rect.draw(win)
        self.text = Text(self.rect.getCenter() , self.rank + self.Suitsymbol[self.suit])
        self.text.setSize(20)
        if self.suit == "H" or self.suit == "D":
            self.text.setTextColor("red")
        else:
            self.text.setTextColor("black")
        self.text.draw(win)

    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
    
    def getRank(self):
        return self.rank
    
    def getSuit(self):
        return self.suit

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        
    def create_deck(self):
        for suit in Card.Suits:
            for rank in Card.Ranks:
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("No more cards in the deck.")
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)

class PokerHand:
    hand_rankings = [
        "Straight Flush",
        "Four of a Kind",
        "Full House",
        "Flush",
        "Straight",
        "Three of a Kind",
        "Two Pair",
        "One Pair",
        "High Card"
    ] 
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def check_hand(self, table_cards):
        all_cards = self.cards + table_cards
        ranks = [card.rank for card in all_cards]
        suits = [card.suit for card in all_cards]

        # Check from highest rank to lowest
        if self.check_straight_flush(suits, ranks):
            return "Straight Flush"
        elif self.check_four_kind(ranks):
            return "Four of a Kind"
        elif self.check_full_house(ranks):
            return "Full House"
        elif self.check_flush(suits):
            return "Flush"
        elif self.check_straight(ranks):
            return "Straight"
        elif self.check_three_kind(ranks):
            return "Three of a Kind"
        elif self.check_two_pairs(ranks):
            return "Two Pair"
        elif self.check_one_pair(ranks):
            return "One Pair"
        else:
            return "High Card"
    


    def check_straight_flush(self, suits, ranks):
        # Get all suits and ranks
        all_suits = ['H', 'D', 'C', 'S']
        all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        # Check each suit
        for suit in all_suits:
            # Get ranks of cards with this suit
            suited_ranks = [rank for rank, s in zip(ranks, suits) if s == suit]

            if self.check_straight(suited_ranks):
              return True

        return False

        
    def check_straight(self, ranks):
        if (len(ranks)) < 5: return False
        all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        rank_indicies = sorted(set(all_ranks.index(rank) for rank in ranks))
        for i in range(len(rank_indicies) - 4):
          start = rank_indicies[i]
          if rank_indicies[i:i+5] == [start, start+1, start+2, start+3, start+4]:
            return True 

        return False

    def check_four_kind(self, ranks):
        rank_count = Counter(ranks)
        return 4 in rank_count.values()

    def check_three_kind(self, ranks):
        rank_count = Counter(ranks)
        return 3 in rank_count.values()

    def check_full_house(self, ranks):
        rank_count = Counter(ranks)
        return 2 in rank_count.values() and 3 in rank_count.values()

    def check_flush(self, suits):
        suit_count = Counter(suits)
        return 5 in suit_count.values()

    def check_two_pairs(self, ranks):
        rank_count = Counter(ranks)
        return list(rank_count.values()).count(2) >= 2

    def check_one_pair(self, ranks):
        rank_count = Counter(ranks)
        return 2 in rank_count.values()
        
    def get_pair_rank(self):
        rank_count = Counter([card.rank for card in self.cards])
        pairs = [rank for rank, count in rank_count.items() if count == 2]
        if pairs:
            
            all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
            pair_ranks = sorted(pairs, key=all_ranks.index)
            return pair_ranks[0]   
    def get_high_card(self):
        all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        card_ranks = sorted([card.rank for card in self.cards], key=all_ranks.index)
        return card_ranks[0]
    
   
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_hole = PokerHand()
        self.player_hole = PokerHand()
        self.table_cards = []
        self.betting_round = 1
        self.controls = {
            'STAY': self.stay,
            'FOLD': self.fold,
            'DEAL': self.deal,
            'QUIT': self.quit
        }
        self.results = {
            'average_score': 0,
            'games_played': 0
        }
        self.deal_initial_cards()
        self.folded_round = 0
        self.score = 0
        self.win = GraphWin("Poker Game", 600, 600)
        self.win.setCoords(0, 0, 10, 10)
        self.controlText = Text(Point(8.5, 7.5), "CONTROLS")
        self.controlText.draw(self.win)
        self.controls_box = Rectangle(Point(7, 7.9), Point(10, 10)) 
        self.controls_box.draw(self.win)
        self.controls_text = Text(self.controls_box.getCenter(), "")
        self.controls_text.draw(self.win)
        self.dealText = Text(Point(1.5, 7.5), "DEALER'S HOLE")
        self.dealText.draw(self.win)
        self.playText = Text(Point(8.5, 3.5), "PLAYER'S HOLE")
        self.playText.draw(self.win)
        self.resultText = Text(Point(1.5, 3.5), "RESULTS")
        self.resultText.draw(self.win)
        self.results_box = Rectangle(Point(0, 0), Point(3.5, 3.2)) 
        self.results_box.draw(self.win)
        self.results_text = Text(self.results_box.getCenter(), "")
        self.results_text.draw(self.win)
   

    def draw_player_cards(self):
        x = 7
        y = 1
        for card in self.player_hole.cards:
            card.draw_face_up(self.win, Point(x, y))
            x += 1.5
    def draw_dealer_cards(self):
        x = 0.3
        y = 7.8
        for card in self.dealer_hole.cards:
            card.draw_face_down(self.win, Point(x, y))
            x += 1.5
    
    def draw_table_cards(self):
        x = 4
        y = 5
        for card in self.table_cards:
            card.draw_face_down(self.win, Point(x, y))
            x += 1.5
        
    """def get_user_action(self):
        while True:
            click_point = self.win.getMouse()
            for button in self.buttons:
                if button.clicked(click_point):
                    return button.getLabel()"""
        
    """def create_graphics(self):
        self.win = GraphWin("Poker Game", 600, 600)
        self.win.setCoords(0, 0, 10, 10)
        for i, hand in enumerate(self.hands):
            for j, card in enumerate(hand.cards):
                card.draw(self.win, Point(2 *j + 1, 2*i +1))"""

    def deal_initial_cards(self):
        for _ in range(2):
            self.dealer_hole.add_card(self.deck.deal())
            self.player_hole.add_card(self.deck.deal())
        
    def stay(self):
        if self.betting_round == 1:
            self.deal_table_cards(3)
        elif self.betting_round == 2:
            self.deal_table_cards(1)
        elif self.betting_round == 3:
            self.deal_table_cards(1)
        elif self.betting_round == 4:
            print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in self.dealer_hole.cards])
        self.next_betting_round()
        

    def fold(self):
        print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in self.dealer_hole.cards])
        if self.betting_round == 1:
            self.deal_table_cards(5)
        elif self.betting_round == 2:
            self.deal_table_cards(2)
        elif self.betting_round == 3:
            self.deal_table_cards(1)
        self.folded_round = self.betting_round
        self.next_betting_round()
        
        
    def deal_table_cards(self, n):
        for _ in range(n):
            self.table_cards.append(self.deck.deal())
      
    def deal(self):
        if self.betting_round < 3:
            for hand in self.hands:
                hand.add_card(self.deck.deal())
        self.next_betting_round()

    def quit(self):
        print("Quitting the game.")
        sys.exit()

    def next_betting_round(self):
        self.betting_round += 1
        if self.betting_round > 4:
            self.betting_round = 1
            self.results['games_played'] += 1
            self.evaluate_and_results()
            self.reset_game()
    
    def evaluate_and_results(self):
        dealer_result = self.dealer_hole.check_hand(self.table_cards)
        player_result = self.player_hole.check_hand(self.table_cards)
        print("Dealer's hole: ", dealer_result)
        print("Player's hole: ", player_result)
        game_points = 0
        if dealer_result == player_result:
            if dealer_result == "One Pair":
                dealer_pair_rank = self.dealer_hole.get_pair_rank()
                player_pair_rank = self.player_hole.get_pair_rank()
                if dealer_pair_rank and player_pair_rank and dealer_pair_rank > player_pair_rank:
                    print("Dealer wins!")
                    game_points = -100
                else:
                    print("Player wins!")
                    game_points = 100
            elif dealer_result == "High Card":
                dealer_high_card = self.dealer_hole.get_high_card()
                player_high_card = self.player_hole.get_high_card()
                if dealer_high_card and player_high_card and dealer_high_card > player_high_card:
                    print("Dealer wins!")
                    game_points = -100
                else:
                    print("Player wins!")
                    game_points = 100
            else:
                print("It's a draw!")
                game_points = 0
        else:
            if PokerHand.hand_rankings.index(dealer_result) < PokerHand.hand_rankings.index(player_result):
                print("Dealer wins!")
                game_points = -100
            else:
                print("Player wins!")
                game_points = 100
        
        if self.folded_round:
            fold_points = 100 - (self.folded_round - 1) * 25
            if game_points < 0: 
                game_points = fold_points
            else:  
                game_points = -fold_points

        print(f"Score for this round: {game_points}")
        return game_points

    def reset_game(self):
        self.dealer_hole = PokerHand()
        self.player_hole = PokerHand()
        self.table_cards = []
        self.deck = Deck()
        self.deck.shuffle()
        self.betting_round = 1
        self.folded_round = 0
        self.deal_initial_cards()

    def handle_button_click(self, button_name):
        if button_name in self.controls:
            self.controls[button_name]()


if __name__ == "__main__":
    game = PokerGame()
    game.draw_player_cards()
    game.draw_dealer_cards()
    game.draw_table_cards()
    while True:
        print("Round:", game.betting_round)
        print("Dealer's hole:",["??" for _ in game.dealer_hole.cards])
        print("Player's hole:", [f'{card.rank}{card.suit}' for card in game.player_hole.cards])
        print("Table cards:", [f'{card.rank}{card.suit}' for card in game.table_cards])
        action = input("Choose an action (STAY, FOLD, DEAL, QUIT): ")
        try:
            game.handle_button_click(action)
        except Exception as e:
            print(f"Invalid action: {e}. Try again.")