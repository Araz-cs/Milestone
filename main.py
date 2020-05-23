import json
import os
import re
import pandas as pd
from search_engine import stemInput, mergeQueries, get_relevant_docs
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment

# In order to run this you need 
# 1 pip install pandas
# 2 have docindex.csv and a populated database folder in the
# folder as main.py
 
docIDPath = "docindex.csv"
df = pd.read_csv(docIDPath, delimiter =',')
docIDs = [list(row) for row in df.values]

#filename = "database.json"
#with open(filename, 'r') as f:
#    datastore = json.load(f)

query = ""
while True:

    query = input("Enter your query : ")
    if query == "":
        print ("Exiting...")
        break
    res = stemInput(query)

<<<<<<< HEAD
    for s in res: # print the stemmed input words
        print (s)

    # Obtain a list of all docs related to the search
    result_list = get_relevant_docs(res)
=======
    result_list = []
    for s in res: # loop through stemmed input and find best docs
        if s in datastore:
            result = datastore[s]
            result.sort(reverse=True)
            result_list.append(result)
>>>>>>> 02ddb73190bcfb0a65103cabe6c3638dd798f6c1

    # Obtain a list of the top 5 URL's relevant to the search
    final = mergeQueries(result_list)[:5]

    # Print top 5 URLS
    for item in final:
        print(docIDs[item[0] -1][1][1:]) #removes preceeding '(' from result
        


