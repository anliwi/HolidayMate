import random
from tkinter import *
import webbrowser
import io
import base64
from urllib.request import urlretrieve
from PIL import ImageTk, Image


from decision_algorithm import decTree
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

def callback(url):
    webbrowser.open_new(url)
 
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
        self.next = Button(window,text="Next",font=("Arial",14),command=self.Question) 
        self.lock = False
        self.response = None
        self.nodes = []
        self.Question()


    def Question(self): 
        self.next.grid(column=0,row=3,pady=5)    
        c, nn = D.getNextNode(self.nodes)
        if c == 0:
            self.lock = False
            questiontext = (str(Quest_HM[nn]))  
            question = Text(window, font=("Arial",14), width=40, height=2)
            question.insert(END,questiontext)
            question.grid(column=0, row=0, padx=80,pady=(75,0))
            self.next.configure(state= DISABLED)
            self.answ1.configure(bg="grey")
            self.answ2.configure(bg="grey")

            self.answ1.grid(column=0, row=1,pady=(8,5))
            self.answ2.grid(column=0, row=2,pady=5)


        else:
        
            for row in df.iterrows():
                if row[1][0] == nn:
                    url = row[1][-1]
                    imgUrl = row[1][-3]
                    desc = row[1][-2]
                    break
            
            #print(nn + "\n" + url + "\n" + imgUrl + "\n" + desc + "\n\n\n")
            
            
            
            
            clear()
            lb = Label(window, text="Our suggestion is: " + nn, font=("Arial",14), cursor = "hand2", fg = "blue")
            lb.bind("<Button-1>", lambda e: callback(url))
            lb.grid(column=0,row=0,padx=120,pady=(170,15))
            dc = Label(window, text = desc)
            dc.grid(column = 0, row = 1, padx = 120, pady = 120)
            
            try:
                urlretrieve(imgUrl, "img.gif")
                photo = ImageTk.PhotoImage(file = "img.gif")
                lbimg = Label(window, image = photo)
                lbimg.image = photo
            except:
                lbimg = Label(window, text="Image not found", font=("Arial",10), fg = "grey")
                
            lbimg.grid(row=2)
            
            toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=15, height=3)
            toMenu.grid(column=0,row=3, padx=218,pady=170)
        
    def SetResponse(self,value):
        if self.lock == False: 
            if value == 1:
   
                self.answ1.configure(bg="green")
                self.next.configure (state= NORMAL)
            else:
                self.answ2.configure(bg="green")  
                self.next.configure (state= NORMAL)

            self.response = value
            self.nodes.append(value)
            self.lock = True
            choice=None


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
