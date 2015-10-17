# implementation of card game - Memory

import simplegui
import random

# constants
HEIGHT = 100
WIDTH = 50
CARDS = 8

# helper function to initialize globals
def new_game():
    global deck, exposed, state, card1, card2, turns
    
    # create the deck of 16 numbers
    deck = range(0,CARDS) + range(0,CARDS)
    
    # shuffle the deck
    random.shuffle(deck)
    
    # all the cards start face-down and unmatched
    exposed = [False] * CARDS * 2

    # state variable
    # 0 - start of game
    # 1 - single exposed unpaired card
    # 2 - end of turn
    state = 0
    
    # index of cards previously clicked
    card1 = None
    card2 = None
    
    # counter for the number of turns
    turns = 0
    
# define event handlers
def mouseclick(pos):
    global deck, exposed, state, card1, card2, turns
    card = pos[0] // WIDTH
    
    # ignore clicks on cards that are face-up
    if exposed[card]:
        return
    
    # turn the card face up
    exposed[card] = True

    # state transitions
    if state == 0:
        card1 = card
        turns += 1
        state = 1
    elif state == 1:
        card2 = card
        state = 2
    else:
        # check for a match
        if deck[card1] != deck[card2]:
            exposed[card1] = False
            exposed[card2] = False

        card1 = card
        card2 = None
        turns += 1
        state = 1
        
# helper function to draw a rectangle
def draw_rect(canvas, upper_left, width, height, *args, **kwargs):
    """
    draw a rectangle on the canvas
    upper_left: tuple specifying the upper-left corner
    width: width of the rectangle
    height: height of the rectangle
    additional arguments pass through to draw_polygon
    (i.e. line_width, line_color, fill_color)
    """
    (x, y) = upper_left
    canvas.draw_polygon([(x,         y),
                         (x,         y + height),
                         (x + width, y + height),
                         (x + width, y)],
                         *args,
                         **kwargs)

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck, exposed, turns
    for i, card in enumerate(deck):
        if exposed[i]:
            canvas.draw_text(str(card),
                             (WIDTH*i + WIDTH//4,
                              HEIGHT*3//4),
                             HEIGHT//2,
                             "White")
        else:
            draw_rect(canvas, (i*WIDTH, 0), WIDTH, HEIGHT, 1, "Black", "Green")

    label.set_text("Turns = " + str(turns))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CARDS * WIDTH * 2, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
# http://www.codeskulptor.org/#user40_sNVLIdVnZC_1.py
