import random
from tkinter import *
from PIL import ImageTk, Image

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
window.geometry("1000x600")
window.configure(bg="#f4e8d9")
photo = Image.open("HolidayMate.png")
photo1 = photo.resize((300, 300), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(photo1)



def clear():
    list = window.grid_slaves()
    for n in list:
        n.destroy()
 



class Quiz:
    def __init__(self): 
        clear()
        self.Logo = Label(window, image=logo,bd=0, highlightthickness=0, relief='ridge')
        self.Logo.grid(column=0,row=0, columnspan=2,padx=50)

        self.QuestionTag = Text(window, height=2, width=80, bd=0, highlightthickness=0, relief='ridge')
        self.QuestionTag.grid(column=0,row=1,columnspan=2,pady=10,sticky=N)
        self.QuestionTag.config(font=("Arial", 20), bg="#f4e8d9", fg="#b28761")
        self.QuestionTag.insert(END,"Tell us about your holiday preferences:")
        self.QuestionTag.config(state=DISABLED)
        self.QuestionTag.tag_configure("tag_name", justify='center')
        self.QuestionTag.tag_add("tag_name", "1.0", "end")

        self.a1="yes"
        self.a2="no"
        self.answ1 = Button(window, text="yes",font=("Arial",14), command=lambda: self.SetResponse(1),width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.answ2 = Button(window, text="no",font=("Arial",14), command=lambda: self.SetResponse(0),width=10, height=2,bd=0, highlightthickness=0, relief='ridge') 
        self.next = Button(window,text="Next",font=("Arial",14),command=self.Question,width=10, height=2,bd=0, highlightthickness=0, relief='ridge') # STILL OPEN: adjust to: only works if a button was clicked
        self.toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.lock=False
        self.response = None
        self.nodes = []
        self.Question()


    def Question(self): 
        self.next.grid(column=1,row=5,pady=(20,0),ipadx=2,sticky=SW)    
        c, nn = D.getNextNode(self.nodes)
        if c == 0:
            self.lock = False
            questiontext = (str(Quest_HM[nn])) 
            question = Text(window, font=("Arial",20), width=60, height=1,bg="#f1f1f1",fg="#0F401B",highlightbackground="#0F401B")
            question.insert(END,questiontext)
            question.config(state=DISABLED)
            question.grid(column=0, row=2,columnspan=2,padx=200,sticky=N)
            question.tag_configure("tag_name", justify='center')
            question.tag_add("tag_name", "1.0", "end")


            self.answ1.grid(column=0, row=4,pady=(8,5), sticky=SE)
            self.answ2.grid(column=1, row=4,pady=5, sticky=SW)
            self.toMenu.grid(column=0,row=5,pady=(20,0),sticky=SE)

        else:
            clear()
            lb = Label(window, text="Our suggestion is: " + nn, font=("Arial",14))
            lb.grid(column=0,row=0,padx=120,pady=(170,15))
            toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=15, height=3)
            toMenu.grid(column=0,row=1, padx=218,pady=170)
        
    def SetResponse(self,value):
        if self.lock == False: 
            if value == 1:
                self.antw1.configure(bg="green")
            else:
                self.antw2.configure(bg="green")     
            self.response = value
            self.nodes.append(value)
            self.lock = True


class Menu:
    def __init__(self):
        clear()
        self.Quiz = Button(window, text="Get your holiday recommendation!", font="arial 14 bold", bg='white',fg="#0F401B", command=quizCreator, width=30, height=3,bd=0, highlightthickness=0, relief='ridge')
        self.Quiz.grid(column=1,row=5)
        
        self.Logo = Label(window, image=logo,bd=0, highlightthickness=0, relief='ridge')
        self.Logo.grid(column=1,row=0,padx=50)
        
        self.Description1 = Text(window, height=2, width=80, bd=0, highlightthickness=0, relief='ridge')
        self.Description1.grid(column=0,row=2,columnspan=3,pady=10)
        self.Description1.config(font=("Arial", 16), bg="#f4e8d9", fg="#0F401B")
        self.Description1.insert(END,"Ever wondered where to go on holiday during the corona pandemic? \nFound yourself trying to understand German websites about local destinations?")
        self.Description1.config(state=DISABLED)
        self.Description1.tag_configure("tag_name", justify='center')
        self.Description1.tag_add("tag_name", "1.0", "end")

        self.Description2 = Text(window, height=1, width=80,bd=0, highlightthickness=0, relief='ridge')
        self.Description2.grid(column=0,row=3,columnspan=3,pady=10)
        self.Description2.config(font='arial 16 bold', bg="#f4e8d9", fg="#0F401B")
        self.Description2.insert(END,"Well, we got a little something for you: HolidayMate.")
        self.Description2.config(state=DISABLED)
        self.Description2.tag_configure("tag_name", justify='center')
        self.Description2.tag_add("tag_name", "1.0", "end")

        self.Description3 = Text(window, height=2, width=80,bd=0, highlightthickness=0, relief='ridge')
        self.Description3.grid(column=0,row=4,columnspan=3,pady=10)
        self.Description3.config(font=("Arial", 16), bg="#f4e8d9", fg="#0F401B")
        self.Description3.insert(END,"Take our interactive quiz to tell us about your preferences with regards to holidays \nand we will give you a customized recommendation suited for your individual needs and wishes!")
        self.Description3.config(state=DISABLED)
        self.Description3.tag_configure("tag_name", justify='center')
        self.Description3.tag_add("tag_name", "1.0", "end")


        self.Tag1 = Label(window, text = "Eco Friendly", font=("Arial",18,"bold"),bg="#0F401B",fg="white", width= 20, height=2)
        self.Tag1.grid(column=0,row=1,padx=15)

        self.Tag2 = Label(window, text = "Regional", font=("Arial",18,"bold"),bg="#0F401B",fg="white", width= 20, height=2)
        self.Tag2.grid(column=1,row=1)

        self.Tag3 = Label(window, text = "Interactive & accessible", font=("Arial",18,"bold"),bg="#0F401B",fg="white", width= 20, height=2)
        self.Tag3.grid(column=2,row=1)
 

def menuCreator():
    m = Menu()
 

def quizCreator():
    q = Quiz()
 

menuCreator()
window.mainloop()
