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
df = pd.read_csv("Database Holiday Mate.csv")
D.fit(df, maxDepth = 6)

window = Tk()
window.title("Holiday_Mate")
window.geometry("1000x800")
window.configure(bg="#f4e8d9")
photo = Image.open("HolidayMate.png")
photo1 = photo.resize((300, 300), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(photo1)


def callback(url):
    webbrowser.open_new(url)

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
        self.answ1 = Button(window, text="Yes",font=("Arial",14), command=lambda: self.SetResponse(1),width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.answ2 = Button(window, text="No",font=("Arial",14), command=lambda: self.SetResponse(0),width=10, height=2,bd=0, highlightthickness=0, relief='ridge') 
        self.clearing = Button(window,text="Clear",font=("Arial",14), command=lambda: self.QuestionClearer(),width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.next = Button(window,text="Next",font=("Arial",14),command=self.Question,width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=10, height=2,bd=0, highlightthickness=0, relief='ridge')
        self.lock = False
        self.response = None
        self.nodes = []
        self.Question()


    def Question(self): 
        self.next.grid(column=1,row=5,pady=(20,0),ipadx=2,sticky=SW)    
        self.answ1.grid(column=0, row=4,pady=(8,5), sticky=SE)
        self.answ2.grid(column=1, row=4,pady=5, sticky=SW)
        self.clearing.grid(column=1, row=6,pady=5, sticky=SW)
        self.toMenu.grid(column=0,row=5,pady=(20,0),sticky=SE)
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
            self.next.configure(state= DISABLED)
            self.answ1.configure(bg="grey")
            self.answ2.configure(bg="grey")

        else:
        
            for row in df.iterrows():
                if row[1][0] == nn:
                    url = row[1][-1]
                    imgUrl = row[1][-3]
                    desc = row[1][-2]
                    break
            
            #print(nn + "\n" + url + "\n" + imgUrl + "\n" + desc + "\n\n\n")
            
            clear()

            self.Logo = Label(window, image=logo,bd=0, highlightthickness=0, relief='ridge')
            self.Logo.grid(column=0,row=0, columnspan=2,padx=50)


            lb = Label(window, text="Our suggestion is: " + nn, font=("arial 20 bold"), cursor = "hand2", fg = "#0F401B",bg="#f4e8d9")
            lb.bind("<Button-1>", lambda e: callback(url))
            lb.grid(column=0,row=1,columnspan=2, padx=20)

            self.Destination = Text(window, height=25, width=50, bd=0, highlightthickness=0, relief='ridge')
            self.Destination.grid(column=1,row=2,sticky=NE)
            self.Destination.config(font=("Arial", 12), bg="#f4e8d9", fg="#0F401B")
            self.Destination.insert(END,desc)
            self.Destination.config(state=DISABLED)
            self.Destination.tag_configure("tag_name", justify='center')
            self.Destination.tag_add("tag_name", "1.0", "end")

            
            try:
                urlretrieve(imgUrl, "img.gif")
                photo2 = Image.open("img.gif")
                photoDest = photo2.resize((500,300), Image.ANTIALIAS)
                photoD = ImageTk.PhotoImage(photoDest)
                lbimg = Label(window, image = photoD,bd=0, highlightthickness=0, relief='ridge')
                lbimg.image = photoD

            except:
                lbimg = Label(window, text="Image not found", font=("Arial",10), fg = "grey",bd=0, highlightthickness=0, relief='ridge')
                
            lbimg.grid(column=0,row=2,padx=10,sticky=NW)
            
            toMenu = Button(window, text="Back to Menu",font=("Arial",14),command=menuCreator, width=15, height=3)
            toMenu.grid(column=0,row=3,sticky=NE)
        
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

    def QuestionClearer(self):
        if self.lock == True: 
            self.answ1.configure(bg="grey")
            self.answ2.configure(bg="grey")     
            self.nodes.pop(-1)
            self.next.configure(state= DISABLED)
            self.lock = False

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
