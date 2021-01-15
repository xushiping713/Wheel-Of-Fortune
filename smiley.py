# Shiping Xu & Alison Kaplon 
# End of Game Celebration -- Smily faces

# smiley.py contains Smiley class

import Tkinter as tk
import animation
import random

# Creates a Smiley class that create a smiley face which drops down when 
# user wins the game
class Smiley(animation.AnimatedObject):
    def __init__(self, canvas):
        x = random.randint(0, 730) # draws the smiley face at random xy
        y = random.randint(0, 20)
        self.canvas=canvas
        # Draws the smiley face
        self.head = canvas.create_oval(x, y, x+15, y+15, fill = 'yellow')
        # adds eyes
        self.leftEye = canvas.create_oval(x+4.5, y+4.5, x+5.5, y+5.5, fill = 'black')
        self.rightEye = canvas.create_oval(x+9.5, y+4.5, x+10.5, y+5.5, fill = 'black')
        # adds mouth
        self.mouth = canvas.create_arc(x+5,y+8, x+10, y+12, fill= 'white', start=180.0, extent= 180.0)
        # put it all together to make the smiley face
        self.parts = [self.head, self.leftEye, self.rightEye, self.mouth]
        
    def move(self):  
        v = random.randint(0,20)  # the speed of smiley faces is a random integer  
        for part in self.parts: 
                                #  x   y    --> increment value
            self.canvas.move(part, 0, v) # the smiley face drops down
      
