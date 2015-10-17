# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed
    
    # create the deck of 16 numbers
    deck = range(0,8) + range(0,8)
    
    # shuffle the deck
    random.shuffle(deck)
    
    # all the cards start face-down
    exposed = [False] * 16

     
# define event handlers
def mouseclick(pos):
    global deck
    card = pos[0] // 50
    exposed[card] = not exposed[card]


# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    for i, card in enumerate(deck):
        if exposed[i]:
            canvas.draw_text(str(card), (50*i + 25,50), 24, "Red")
        else:
            canvas.draw_polygon([(i*50,0),
                              (i*50,100),
                              (i*50+50,100),
                              (i*50+50,0)],
                             1, "Black", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric

# http://www.codeskulptor.org/#user40_sNVLIdVnZC_0.py
