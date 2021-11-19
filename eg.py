from id3 import decTree
import pandas as pd

D = decTree()
df = pd.read_csv("Database Holiday Mate - Sheet1.csv")
D.fit(df)
print(D.getTree())

nodes = []
c = 0
while c == 0:
    c, nn = D.getNextNode(nodes)
    if c == 1:
        print("suggestion is: ", nn)
    else:
        print(nn, "?")
        response = int(input())
        nodes.append(response)
print("end")