from id3 import decTree
import pandas as pd
import QuestDictionaryHolidayMate

Quest_HM = QuestDictionaryHolidayMate.Quest_HM

D = decTree()
df = pd.read_csv("Database Holiday Mate - Sheet1.csv")
D.fit(df, maxDepth = 3)
print(D.getTree())
print("\n\n\n\n\n\n")

nodes = []
c = 0
while c == 0:
    c, nn = D.getNextNode(nodes)
    if c == 1:
        print("suggestion is: ", nn)
    else:
        print(Quest_HM[nn], "?")
        response = input()
        if response == "Yes":
            r = 1
        else:
            r = 0
        nodes.append(r)
print("end")


