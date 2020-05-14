import json
import os
import re
import pandas as pd
from indexer import stemInput
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment

# In order to run this you need 
# 1 pip install pandas
# 2 have docindex.csv and database.json in the same 
# folder as main.py
 
docIDPath = "docindex.csv"
df = pd.read_csv(docIDPath, delimiter =',')
docIDs = [list(row) for row in df.values]

filename = "database.json"
with open(filename, 'r') as f:
    datastore = json.load(f)

query = input("Enter your query : ")

res = stemInput(query)

for s in res: # print the stemmed input words
    print (s)
    c = input("break")


for s in res: # loop through stemmed input and find best docs
    result_list = datastore[s]
    result_list.sort(reverse=True)
    for i in range(0,5):
        index = result_list[i][1]#docid
        index -=1
        print (index)
        print (docIDs[index][1]) #URL
    c = input("break")


