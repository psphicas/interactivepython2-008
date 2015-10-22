# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        """create Hand object"""
        self.cards = []

    def __str__(self):
        """return a string representation of a hand"""
        return " ".join([str(x) for x in self.cards])

    def add_card(self, card):
        """add a card object to a hand"""
        self.cards.append(card)

    def get_value(self):
        """
        compute the value of the hand.
        count aces as 1, if the hand has an ace,
        then add 10 to hand value if it doesn't bust
        """
        value = sum([VALUES[x.rank] for x in self.cards])
        
        if (value + 10 <= 21) and "A" in [x.rank for x in self.cards]:
            value += 10

        return value
   
    def draw(self, canvas, pos):
        """
        draw a hand on the canvas, use the draw method for cards
        """
        (x, y) = pos
        
        for i, card in enumerate(self.cards):
            card.draw(canvas, (x + i*100, y))
 
        
# define deck class 
class Deck:
    def __init__(self):
        """Create a Deck object"""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """shuffle the deck"""
        random.shuffle(self.cards)

    def deal_card(self):
        """deal a card object from the deck"""
        return self.cards.pop()
    
    def __str__(self):
        """return a string representing the deck"""
        return " ".join([str(x) for x in self.cards])
        

# helper function to print hands with score
def print_hand(whose_hand):
    if whose_hand == "player":
        print "Player Hand [%2d]: %s" % (player_hand.get_value(),
                                         player_hand)
    elif whose_hand == "dealer":
        print "Dealer Hand [%2d]: %s" % (dealer_hand.get_value(),
                                         dealer_hand)

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score

    
    # lose a point if we were already in play
    if in_play:
        score -= 1
        print "Hand aborted."
        print "Score:", score
        
    print
    print "DEAL"
    print "(Score: %d)" % score
    
    # create and shuffle a fresh deck
    deck = Deck()
    deck.shuffle()
    
    # create hands for player and dealer
    player_hand = Hand()
    dealer_hand = Hand()
    
    # deal two cards to the player
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    # deal two cards to the dealer
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Display the hands at the console
    print_hand("dealer")
    print_hand("player")
    
    # clear any previous outcome
    outcome = ""
    
    # the hand is now in play
    in_play = True

def hit():
    """
    if the hand is in play, hit the player
    if busted, assign a message to outcome,
    update in_play and score
    """
    global in_play, deck, player_hand, score, outcome

    # ignore clicks to the "Hit" button if the hand is not in play
    if not in_play: return
    
    print "HIT"

    # deal a card to the player and display the new hand
    player_hand.add_card(deck.deal_card())
    print_hand("player")

    # check if the player busts
    if player_hand.get_value() > 21:
        outcome = "You went bust and lose."
        in_play = False
        score -= 1
        print outcome
        print "Score:",score

       
def stand():
    """
    if hand is in play, repeatedly hit dealer until his
    hand has value 17 or more
    assign a message to outcome, update in_play and score
    """
    global in_play, deck, dealer_hand, score, outcome

    # ignore clicks to the "Stand" button if the hand is not in play
    if not in_play: return

    print "STAND"
    
    # deal cards to the dealer as necessary
    # display the new dealer hand with each card
    while (dealer_hand.get_value() < 17):
        dealer_hand.add_card(deck.deal_card())
        print_hand("dealer")

    # check to see who wins
    if dealer_hand.get_value() > 21:
        outcome = "Dealer went bust. You win."
        score += 1
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You lose."
        score -= 1
    else:
        outcome = "You win."
        score += 1

    print outcome
    print "Score:",score
    in_play = False
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text("Blackjack", (100, 100), 36, "Aqua", "sans-serif")

    canvas.draw_text("Dealer", (75, 175), 24, "Black", "sans-serif")
    dealer_hand.draw(canvas, (75, 200))
    
    canvas.draw_text("Player", (75, 375), 24, "Black", "sans-serif")
    player_hand.draw(canvas, (75, 400))

    # cover Dealer's hole card
    if in_play:
        canvas.draw_image(card_back,
                          CARD_BACK_CENTER,
                          CARD_BACK_SIZE,
                          [75 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)

        prompt = "Hit or stand?"
    else:
        prompt = "New deal?"

    # display the score
    canvas.draw_text("Score "+str(score), (400, 100), 24, "Black", "sans-serif")

    # display the outcome
    canvas.draw_text(outcome, (225, 175), 24, "Black", "sans-serif")
    
    # display a prompt
    canvas.draw_text(prompt, (225, 375), 24, "Black", "sans-serif")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
