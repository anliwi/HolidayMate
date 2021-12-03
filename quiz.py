import random
from tkinter import *


from id3 import decTree
import pandas as pd
import QuestDictionaryHolidayMate 

Quest_HM = QuestDictionaryHolidayMate.Quest_HM

D = decTree()
df = pd.read_csv("Database Holiday Mate - Sheet1.csv")
D.fit(df, maxDepth = 6)
print(D.getTree())
print("\n\n\n\n\n\n")



window = Tk()
window.title("Holiday_Mate")
window.geometry("600x450")
 

 
def clear():
    list = window.grid_slaves()
    for n in list:
        n.destroy()
 



class Quiz:
    def __init__(self): 
        clear()
        self.a1="yes"
        self.a2="no"
        self.answ1 = Button(window, text="Yes",font=("Arial",14), command=lambda: self.SetResponse(1))
        self.answ2 = Button(window, text="No",font=("Arial",14), command=lambda: self.SetResponse(0)) 
        self.next = Button(window,text="Next",font=("Arial",14),command=self.Question) # STILL OPEN: adjust to: only works if a button was clicked
        self.lock = False
        self.response = None
        self.nodes = []
        self.Question()


    def Question(self): 
        self.next.grid(column=0,row=3,pady=5)    
        c, nn = D.getNextNode(self.nodes)
        if c == 0:
            self.lock = False
            questiontext = (Quest_HM[nn], "?") # here we still need a nice display for the question 
            question = Text(window, font=("Arial",14), width=40, height=2)
            question.insert(END,questiontext)
            question.grid(column=0, row=0, padx=80,pady=(75,0))


            self.answ1.grid(column=0, row=1,pady=(8,5))
            self.answ2.grid(column=0, row=2,pady=5)


        else:
            clear()
            lb = Label(window, text="Our suggestion is: " + nn, font=("Arial",14))
            lb.grid(column=0,row=0,padx=120,pady=(170,15))
            toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=15, height=3)
            toMenu.grid(column=0,row=1, padx=218,pady=170)
        
    def SetResponse(self,value):
        if self.lock == False: 
            if value == 1:
                self.answ1.configure(bg="green")
            else:
                self.answ2.configure(bg="green")     
            self.response = value
            self.nodes.append(value)
            self.lock = True


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
