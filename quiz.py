import random
from tkinter import *


from id3 import decTree
import pandas as pd
import QuestDictionaryHolidayMate 

Quest_HM = QuestDictionaryHolidayMate.Quest_HM

D = decTree()
df = pd.read_csv("Database Holiday Mate - Sheet1.csv")
D.fit(df, maxDepth = 2)
print(D.getTree())
print("\n\n\n\n\n\n")


nodes = []
c = 0 # what is c?


window = Tk()
window.title("Holiday_Mate")
window.geometry("600x450")
 

 
def clear():
    list = window.grid_slaves()
    for n in list:
        n.destroy()
 

# self.lock = False - could be used to make sure that as soon as one button is clicked you cant't click another one

class Quiz:
    def __init__(self): # does this maybe need to take in something from the tree?
        clear()
        self.a1="yes"
        self.a2="no"
        self.antw1 = Button(window, text="yes",font=("Arial",14), command=lambda: SetResponse(1)) # set the response
        self.antw2 = Button(window, text="no",font=("Arial",14), command=lambda: SetResponse(0)) # set the response
        self.naechste = Button(window,text="Next",font=("Arial",14),command=self.Question) # lambda with if (don't go next until the Response is not set)
        self.Question()


    def Question(self): # does this maybe also needs to take nodes? # the loop is not yet working # also the setting of the response
        self.naechste.grid(column=0,row=3,pady=5)    
        nodes = [] 
        c = 0 # what is that c ? 
        while c == 0:
            c, nn = D.getNextNode(nodes)
            if c == 0:
                questiontext = (Quest_HM[nn], "?")
                question = Text(window, font=("Arial",14), width=40, height=2)
                question.insert(END,questiontext)
                question.grid(column=0, row=0, padx=80,pady=(75,0))

                self.antw1 = Button(window, text="yes",font=("Arial",14), width=39, command=lambda: SetResponse(1))
                self.antw2 = Button(window, text="no",font=("Arial",14), width=39,  command=lambda: SetResponse(0))

                self.antw1.grid(column=0, row=1,pady=(8,5))
                self.antw2.grid(column=0, row=2,pady=5)

                if self.response == 0: # here i want it to take the value from the button that is changing the global
                    nodes.append(0)
                else:
                    nodes.append(1)

            else:
                clear()
                lb = Label(window, text="Our suggestion is: " + nn, font=("Arial",14))
                lb.grid(column=0,row=0,padx=120,pady=(170,15))
                toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator)
                toMenu.grid(column=0,row=1)
        
    def SetResponse(self,value):
        self.response = value


class Menu:
    def __init__(self):
        clear()
        self.Quiz = Button(window, text="Quiz", font=("Arial", 14), command=quizCreator, width=15, height=3)
        self.Quiz.grid(column=0,row=0,padx=218,pady=170)
 


def menuCreator():
    m = Menu()
 

def quizCreator():
    q = Quiz()
 

menuCreator()
window.mainloop()
