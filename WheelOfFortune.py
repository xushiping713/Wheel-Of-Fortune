# Shiping Xu & Alison Kaplon
# CS111 Final Project
# Wheel of Fortune

import Tkinter as tk
import animation
import random
import math
import os
import smiley

# wheel segments colors and corresponding money values
rainbow = ['red', 'cyan', 'orange', 'magenta', 'yellow', 
                                        'blue', 'green', 'purple']
money = [20, 50, 20, 25, 30, 30, 40, 45]
vowels = 'AEIOU'
consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
#spinVals indicies are: [generatedStopNum, ColorOfSection, CashValueOfSection]
spinVals = [[22,'Red', 20],[23, 'Cyan', 50], [24, 'Orange',20],
[25, 'Magenta',25],[26, 'Yellow',30],[27, 'Blue',30],
                        [28, 'Green',40],[29,'Purple',45]]

# Creates a class Wheelie that contains animated canvas 
class Wheelie(animation.AnimatedObject):       
    def __init__(self, canvas, app, xy, l):
        self.gameover = False
        self.counter = 0 # Sets a counter
        self.stopCounter = 0  # Sets a stop counter
        self.canvas = canvas 
        self.app= app
        self.NUM_SECTORS = 8    
        x,y = xy
        sectorsBB = (x-l, y-l, x+l, y+l) # Sets Sector Bounding Box
        sectorAngle = 360/self.NUM_SECTORS 
        self.ids = [] # Keeps track of the wheel sectors
        self.confetti = [] # Keeps track of the confetti smiley faces
        self.myTexts = [] # Keeps track of text on the wheel
        # Makes the wheel and text on the wheel
        pi = math.atan(1)*4 
        angle = (22*pi)/180.0         
        for i in range(self.NUM_SECTORS): # Beginning of a for loop
            # Creates and adds segments onto the wheel
            self.arc = self.canvas.create_arc(sectorsBB, start = i*sectorAngle, 
                extent = sectorAngle, fill = rainbow[i%len(rainbow)], outline = 'black')
            self.ids.append(self.arc)
            # Creates and adds text on each segment to the wheel               
            self.myText = tk.StringVar()
            self.myText.set(money[i]) 
            self.textLabel = tk.Label(self.canvas, textvariable = self.myText, 
                                fg='white', bg='black', font = 'verdana 16')
            self.canvas.create_window((225 + 120*math.cos(angle), 
                            260 - 120*math.sin(angle)), window = self.textLabel)
            angle += (2*pi)/self.NUM_SECTORS
            self.myTexts.append(self.myText)            
        # adds indicator on top of the wheel
        self.canvas.create_polygon((190,55), (210, 52), (205, 80),fill='black')
        
    def move(self): # Defines a move method that spins the wheel        
        if self.gameover == False:
            self.counter += 1 # Increments the counter by 1
            if self.stopCounter<15:
                if self.counter%10 == 3: 
                    self.helper()            
        # Slows down the wheel
            elif self.stopCounter>=15 and self.stopCounter<20:
                if self.counter%10 == 5:
                    self.helper()
        # Slows down the wheel
            elif self.stopCounter>=20 and self.stopCounter<self.app.stopNum:
                if self.counter%10 == 9:
                    self.helper() 
        # Stops the wheel from spinning
            elif self.stopCounter==self.app.stopNum:
                self.canvas.stop()
                self.spinVal= self.myTexts[2].get()
                
                self.app.statLabel['text']= ('You have landed on: $' + 
                str(self.spinVal) + '! \n Now guess a letter! \n \
                    Remember: Vowels cost $25!') # Prompts user to choose a letter
                self.counter = 0 # Resets the counter
                self.stopCounter=0 # Resets the stop counter           
                for el in self.app.letterButtons: # Beginning of a for loop
# if user has more than $25 and letters are not guessed,
# enable both vowels and consonants
                    if (int(self.app.moneyAmount.get())>=25 and 
                el.cget('text').lower() not in self.app.guessedLetters):
                        el.config(state='normal') 
# else, only enable consonants that have not been guessed before
                    else:
                        if (el.cget('text') in consonants and 
                            el.cget('text').lower() not in self.app.guessedLetters):
                            el.config(state='normal')                        
                  
    def helper(self): # Defines a helper function
            self.counter = 0 # Sets counter back to 0
            self.stopCounter +=1 # Increments stopCounter by 1
        # Takes out the last element in the list and append to the end
            rainbow.append(rainbow.pop(0)) 
            money.append(money.pop(0))
        # Beginning of a for loop that changes the color and text on the wheel
            for i in range(self.NUM_SECTORS): 
                self.myTexts[i].set(money[i]) # sets the text 
                sector = self.ids[i] # sets the fill color of the wheel sectors
                self.canvas.itemconfig(sector, fill = rainbow[i%len(rainbow)]) 

    # Adds a bunch of random smiley faces to the animation canvas
    def start_smiley(self):        
        for i in range(100): 
            oneSmiley = smiley.Smiley(self.canvas)
            self.confetti.append(oneSmiley)
            self.canvas.addItem(oneSmiley)          
        self.canvas.start()                  

# Defines a new class for wheel of fortune Game window
class StarterApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self) 
        self.w_app = None   
        root.title('Wheel of Fortune')
        self.grid()
        self.configure(bg='peachpuff2')
        self.createWidgets()
           
    def createWidgets(self):
        # Welcome Message 
        self.welcomeLabel = tk.Label(self, text = 'Welcome to THE Game!', 
                                bg = 'peachpuff2', font = 'Verdana 50 bold')
        self.welcomeLabel.grid(row=0, column=8, sticky=tk.N + tk.E + tk.W + tk.S)
        # adds some space on left side
        leftLabel = tk.Label(self, text='   ', bg='peachpuff2', 
                                            highlightbackground='peachpuff2')
        leftLabel.grid(row=0,column=3,sticky=tk.N+tk.E+tk.S+tk.W)
        # adds some space on left side
        rightLabel = tk.Label(self, text='   ', bg='peachpuff2', 
                                            highlightbackground='peachpuff2')
        rightLabel.grid(row=0,column=9,sticky=tk.N+tk.E+tk.S+tk.W)

        # Welcome Image
        welcomePic = tk.PhotoImage(file = 'welcome.gif')
        self.imageLabel = tk.Label(self, image = welcomePic, bg='peachpuff2',
                                                            borderwidth = 0)
        self.imageLabel.pic = welcomePic
        self.imageLabel.grid(row=1, column=8, sticky=tk.N+tk.E+tk.S+tk.W)
        
        # Start Game Button
        self.startButton = tk.Button(self, text = 'Start Game', 
                        bg = 'peachpuff2', command=self.onStartButtonClick)
        self.startButton.grid(row =2, column=8, sticky=tk.N+tk.E+tk.S+tk.W)
    
        # Instruction Button
        self.instructButton = tk.Button(self, text = 'Instructions', 
                        bg = 'peachpuff2', command=self.onInstructButtonClick)
        self.instructButton.grid(row=3, column=8, sticky=tk.N+tk.E+tk.S+tk.W)

        # Quit Button        
        self.quitButton = tk.Button(self, text='I\'m not ready for this', 
                                bg='PeachPuff2',command=self.onQuitButtonClick)
        self.quitButton.grid(row=4,column=8, sticky=tk.N+tk.E+tk.S+tk.W)
    
    # Starts a new game in a new window
    def onStartButtonClick(self):
        if self.w_app!=None: self.w_app.destroy()
        self.w_app = WheelOfFortuneApp((225, 225), 200, 80)
        self.w_app.mainloop()

# When user clicks on Instructions, Games instructions show up, user can
# start the game from there
    def onInstructButtonClick(self):
        self.welcomeLabel.grid(row=0,column = 0, sticky=tk.N+tk.E+tk.S+tk.W) 
        self.imageLabel.destroy() # Closes the image
        self.quitButton.grid(row=22, column = 0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.startButton.grid(row=21, column = 0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.instructButton.grid(row=23, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.instructButton['state']='disabled'
        filename = 'instructions.txt' #opening the instructions
        instruct = open(filename, 'r') #reading the file
        lines = [] 
        for line in instruct: #getting the lines
            lines.append(line.rstrip())
        counter = 1 # Sets a counter
        for line in lines:
            label = tk.Label(self, text = line, bg = 'peachpuff2', 
                    font = 'Verdana 14', justify = 'center', anchor = tk.N)
            label.grid(row = counter, column = 0, sticky=tk.N+tk.E+tk.S+tk.W)
            counter+=1  # Increments the counter by 1
    
    # On quit, closes the game
    def onQuitButtonClick(self):
        root.destroy()

class WheelOfFortuneApp(tk.Toplevel):
    def __init__(self, xy, length_of_sector, width_of_sectors):
        tk.Toplevel.__init__(self)
        self.title('Game starts!') # Sets the title of the new window

        # There are 4 frames
        # f1 = top left (Holds the wheel)
        # f2 = middle left (Holds the keyboard)
        # f3 = bottom left (Holds submission details)
        # f3 is on the right, and spans three rows (Holds other game related etails)

        # Diagram: 
        # f1 f3
        # f2 f3
        # f4 f3

        #### ------------ FRAME 1 TOP LEFT ------------
        # Creates the frame
        self.frame1 = tk.Frame(self, width= 500, height = 400, bg= 'peachpuff2', 
                                            highlightbackground='peachpuff2')
        self.frame1.grid(row=0,column=0, rowspan =2, sticky=tk.N+tk.E+tk.S+tk.W)
        # Create animation canvas for the wheel  
        self.canvas = animation.AnimationCanvas(self.frame1, width=470, 
        height=470, background="peachpuff2",  highlightbackground='peachpuff2')
        # Create wheel
        self.ourWheel = Wheelie(self.canvas,self, (225,260),200)
        # Add the wheel to the canvas
        self.canvas.addItem(self.ourWheel)
        # Place the canvas on the frame
        self.canvas.grid(row=1, column=0)  
        #### ---------------------------------


        #### ------------ FRAME 2 MIDDLE LEFT ------------
        # Create the frame
        self.frame2 = tk.Frame(self, width=200, height = 100, bg='peachpuff2', 
                                            highlightbackground='peachpuff2')
        self.frame2.grid(row=2,column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        # Creates the keyboard
        keyboard = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        i = 0
        self.letterButtons = []
        self.guessedLetters = []
        for l in keyboard:    
            self.letterButton = tk.Button(self.frame2, text = l,
bg='light slate gray', command=lambda letter=l: self.onLetterButtonClick(letter)
                                                        , state = 'disabled')
            self.letterButton.grid(row=int(i/13.0), column = (i%13), 
                                                sticky=tk.E+tk.W + tk.N + tk.S)
            self.letterButtons.append(self.letterButton)
            i +=1 
        #### ---------------------------------


        #### ------------ FRAME 3 TOP RIGHT ------------
        # Create the frame       
        self.frame3 = tk.Frame(self, width=400, height = 600, bg = 'peachpuff2', 
                                            highlightbackground='peachpuff2')
        self.frame3.grid(row = 0, rowspan = 5,column = 1, sticky=tk.N+tk.E+tk.S+tk.W)
        
        # Key
        self.keyTop = tk.Label(self.frame3, text = 'Color to Cash Key', 
                            font = 'Verdana 15', bg = 'black', fg = 'white')
        self.keyTop.grid(row=2, column=0,sticky = tk.E+tk.W)
        for i in range(len(spinVals)):
            self.keyItem = tk.Label(self.frame3, 
            text = str(spinVals[i][1]) + ' = $' + str(spinVals[i][2]), 
                        font = 'Verdana 14', bg = 'black', fg = spinVals[i][1])
            self.keyItem.grid(row = i+3, column= 0, sticky = tk.E+tk.W)
                            
        # Phrase reveal 
        self.phraseIntro = tk.Label(self.frame3, text = 'Theme: "Thing" \n Your Phrase:', 
            font = 'Verdana 15', bg = 'LightBlue1')
        self.phraseIntro.grid(row = 13, column = 0, sticky = tk.E+ tk.W)
        self.phraseReveal = tk.Label(self.frame3, 
            text = '', bg = 'LightBlue1', font = 'Verdana 15')  
        self.phraseReveal.grid(row =14, column = 0, sticky = tk.E+tk.W)
        
        # Spin button
        self.spinButton = tk.Button(self.frame3, 
            text = 'Spin That Wheel!!!', bg = 'peachpuff2', 
    font='Verdana 18 bold', command=self.onSpinButtonClick, state='disabled')
        self.spinButton.grid(row = 11, column=0, sticky = tk.E+tk.W)      

        # Wallet label
        self.walletLabel = tk.Label(self.frame3, text = 'You have $', 
                        font= 'Verdana 15', fg = 'black', bg = 'peachpuff2')
        self.walletLabel.grid(row=12, column = 0, sticky = tk.W)
        self.moneyAmount = tk.StringVar()
        self.moneyLabel = tk.Label(self.frame3, textvariable = self.moneyAmount, 
                            font= 'Verdana 15', fg = 'black', bg = 'peachpuff2')
        self.moneyLabel.grid(row=12, column = 0, sticky = tk.E)
        self.moneyAmount.set('0')
        
        # Quit button
        spaceLabel = tk.Label(self.frame3, bg='peachpuff2', font='Monaco 180')
        spaceLabel.grid(row=98, column =0)
        self.quitButton = tk.Button(self.frame3, text = 'Quit Game' , 
                        bg= 'LightBlue1', command = self.onQuitButtonClick1)
        self.quitButton.grid(row=100, column = 0, sticky = tk.E + tk.S)

        # New game button
        self.restartButton = tk.Button(self.frame3, text = 'New Game' , 
                            bg = 'LightBlue1', command = self.onRestartClick)
        self.restartButton.grid(row=99, column = 0, sticky = tk.E+tk.S)     
        
        # difficulty levels
        self.easyButton = tk.Button(self.frame3, text = 'Draw an Easy Phrase', 
                             bg = 'LightBlue1', command = self.onEasyClick)
        self.easyButton.grid(row=15, column = 0, sticky = tk.E+tk.S+tk.W+tk.N)
        
        self.mediumButton = tk.Button(self.frame3, text = 'Draw a Medium Phrase',
                 bg = 'LightBlue1', command = self.onMediumClick)   
        self.mediumButton.grid(row=16, column = 0, sticky = tk.E+tk.S+tk.W+tk.N)
        
        self.hardButton = tk.Button(self.frame3, text = 'Draw a Hard Phrase',
                 bg = 'LightBlue1', command = self.onHardClick)   
        self.hardButton.grid(row=17, column = 0, sticky = tk.E+tk.S+tk.W+tk.N)
        #### ---------------------------------


        #### ------------ FRAME 4 BOTTOM LEFT ------------
        # Create the frame
        self.frame4 = tk.Frame(self, width = 400, height = 200, bg = 'peachpuff2', 
                                            highlightbackground='peachpuff2')
        self.frame4.grid(row=3, rowspan=3, column = 0, sticky=tk.N+tk.E+tk.S+tk.W)         
        # Add the status label - Left Side, below the animation canvas and keyboard 
        self.statLabel = tk.Label(self.frame4, text = '\n Pick a Difficulty Level to the Right!! \n', 
            bg = 'peachpuff2', font = 'Verdana 18 bold', fg = 'red')
        self.statLabel.grid(row=0, column=0, columnspan=2)           
        # Phrase label 
        self.phraseLabel = tk.Label(self.frame4,
    text = 'The Secret Phrase is: ', bg = 'peachpuff2', font = 'Verdana 16')
        self.phraseLabel.grid(row=1, column=0, sticky=tk.E)
        self.phraseEntry = tk.Entry(self.frame4) #adds entry box to frame4
        self.phraseEntry.grid(row=1,column=1,sticky=tk.W)            
        # Submit button 
        self.submitButton = tk.Button(self.frame4,
        text = 'Submit', bg = 'peachpuff2', command=self.onSubmitButtonClick, state='disabled')
        self.submitButton.grid(row=1, column=2, sticky=tk.E)
        #### ---------------------------------

# Defines a method that reveal the phrase
    def getReveal(self): # Reveal the phrase
        self.answer =  self.genPhrase()
        self.reveal = ''
        for i in range(len(str(self.answer))):
            if str(self.answer)[i] == ' ':
                self.reveal+=' '
            else:
                self.reveal+='_'
        return self.revealFormat(self.reveal.upper())

# Define a helper function for getReveal to determine the reveal format as '_ _ _ _ _ '       
    def revealFormat(self, string): 
    #hello --> _____ --> _ _ _ _ _
        finalRev = ''
        for char in string:
            finalRev+=char + ' '
        return finalRev    

# Generates a random phrase from a text file depending on the difficulty
# level that user chooses         
    def genPhrase(self):  
        self.filename = self.diffLevel+ '.txt' #opening the instructions
        phrases = open(self.filename, 'r') #reading the file
        self.phraseList = [] 
        for phrase in phrases: #getting the lines
            self.phraseList.append(phrase.rstrip())
        phraseNum = random.randint(0,len(self.phraseList)-1)
        for i in range(len(self.phraseList)):
            if i == phraseNum:
                return self.phraseList[i]

# Defines a helper method that changes the status label, enable the spinButton,
# disble difficulty level buttons and enable submit button when user chooses
# a difficulty level
    def difficulty(self):
        self.statLabel.config(text = 'Its Time to Spin That Wheel!!')
        self.spinButton.config(state = 'normal')
        self.phraseReveal.config(text = self.getReveal())
        self.submitButton.config(state ='normal')
        self.easyButton.config(state='disabled')
        self.mediumButton.config(state='disabled')
        self.hardButton.config(state='disabled')        

# When user clicks on easy phrase, genPhrase will generates a phrase from 
# easy.txt file                 
    def onEasyClick(self):
        self.diffLevel = 'easy'
        self.difficulty()

# When user clicks on easy phrase, genPhrase will generates a phrase from 
# medium.txt file   
    def onMediumClick(self):
        self.diffLevel = 'medium'
        self.difficulty()

# When user clicks on easy phrase, genPhrase will generates a phrase from 
# hard.txt file             
    def onHardClick(self):
        self.diffLevel = 'hard'
        self.difficulty()
                        
    # Closes the window
    def onQuitButtonClick1(self):
        root.destroy()
        
# When user enters a phrase and clicks on submit...     
    def onSubmitButtonClick(self):  
        entry = self.phraseEntry.get() # gets the phrase user enters
        if  entry == self.answer: # compares the phrase to the answer  
# if the answer is correct, player wins $100 in addition to what the player has
# in the wallet          
            self.statLabel.config(text='YOU WIN \n You have won ' + 
                        str(int(self.moneyAmount.get()) + 100) + ' dollars!') 
            # Reveals the answer
            self.phraseReveal.config(text = self.answer.upper())
            self.submitButton.config(state = 'disabled') #Disable submit button
            self.ourWheel.gameover = True 

            self.ourWheel.start_smiley() #starts the animation 
# If the player doesnt' enter anynthing, prompts the player an invalid phrase
        elif entry == '': 
            self.statLabel.config(text = 'Not a valid phrase! \n Either re-enter\
 a phrase and submit again \n or \n Spin That Wheel!')
 
# If the player guesses an incorrect answer
# The players loses game and lost all money in wallet, game ends
        else: 
            self.statLabel.config(text = entry + ' is not the answer! \
You Lose :( \nEither Quit the window\nOr Start a New Game\nusing \
the buttons on the side')
            self.submitButton.config(state = 'disabled')
            self.moneyAmount.set('0') # Resets wallet back to 0
            self.phraseReveal.config(text=str(self.answer).upper())
            self.spinButton.config(state='disabled')
            
    # Starts a new game on a new window and closes the old game
    def onRestartClick(self):
        self.destroy()
        self.newGame = WheelOfFortuneApp((225, 225), 200, 80)
        self.newGame.mainloop()
        
# Defines a method tells what to do when user selects a letter from the keyboard         
    def onLetterButtonClick(self,letter):
        for button in self.letterButtons:
            button.config(state = 'disabled') #disabling all of the buttons
        checkLet = letter.lower() 
        newReveal = ''
        self.guessedLetters.append(checkLet) #so we will only reactivate unpressed buttons
        
        self.freqOfLet = 0 #times the letter appears
        
        if checkLet in str(self.answer): #if the letter is in the answer
            for a in range(len(str(self.answer))): #going throuh the answer
                    if str(self.answer)[a]==checkLet:
                        newReveal+=checkLet #adding the letter to our new reveal phrase
                        self.freqOfLet +=1 #adding one each time the checkLet is in the answer
                    else: newReveal+=str(self.reveal)[a] #else just adding what was there before
            self.phraseReveal['text'] = self.reveal.upper() #maling everytihng uppercase
        else:
            newReveal = str(self.reveal)
                  
        #updating the wallet
        if letter in vowels:
            self.moneyAmount.set(int(self.moneyAmount.get())-25)
        elif letter in consonants:  
            spinVal = int(self.ourWheel.spinVal)
            self.moneyAmount.set(int(self.moneyAmount.get())+ (spinVal * self.freqOfLet))
#making our old reveal phrase the new one
        self.reveal=newReveal.upper() 
#reassigning the text of the revealphrase        
        self.phraseReveal['text'] = self.revealFormat(self.reveal) 
#reassigning the stat label       
        if checkLet.upper() in vowels:
            self.statLabel.config(text = str(self.freqOfLet)+ ' ' + 
                str(checkLet).upper() + ' \'s found \n Now Spin That Wheel!')
            self.spinButton.config(state='normal')        
        else:
            spinVal = int(self.ourWheel.spinVal)
            self.statLabel.config(text = 'The letter: ' + letter + 
            ' was in the secret phrase ' + str(self.freqOfLet) + 
            ' times \n You made: $' + str(spinVal*self.freqOfLet) + '! \n Now Spin That Wheel!')        
            self.spinButton.config(state = 'normal', command=self.onSpinButtonClick)
# If the user guesses all the letters in the secrect phrase              
        if newReveal.lower() == str(self.answer):
            self.statLabel.config(text='WINNER! \n You have won ' + 
            str(self.moneyAmount.get()) + ' dollars! \nNow either Quit Game \n\
or Start a New Game \nby pressing the buttons on the side')
            self.ourWheel.gameover = True            
            self.ourWheel.start_smiley()
                
# When user clicks on spin, animation start, status label changes to 'spinning...'
# and spin button is disabled
    def onSpinButtonClick(self):
        self.stopNum = random.randint(22,29)
        self.canvas.start()
        self.statLabel['text']= '\n   Spinning...          \n'
        self.spinButton.config(state='disabled')

    

###################
root = tk.Tk()
app = StarterApp(root)
# For Macs only: Bring root window to the front
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
root.mainloop()
##################