import json
import os
import re
import pandas as pd
from indexer import stemInput, mergeQueries
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

query = ""
while True:

    query = input("Enter your query : ")
    if query == "":
        print ("Exiting...")
        break
    res = stemInput(query)

    result_list = []
    for s in res: # loop through stemmed input and find best docs
        if s in datastore:
            result = datastore[s]
            result.sort(reverse=True)
            result_list.append(result)

    final = mergeQueries(result_list)[:5]

    for item in final:
        print(docIDs[item[0] -1][1][1:]) #removes preceeding '(' from result
        


