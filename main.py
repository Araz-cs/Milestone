import json
import os
import re
import pandas as pd
from search_engine import porterstemQuery, mergeQueries, get_relevant_docs
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
    result_list = porterstemQuery(query)

    # Obtain a list of the top 5 URL's relevant to the search
    final = mergeQueries(result_list)[:5]

    # Print top 5 URLS
    for item in final:
        print(docIDs[item[0] -1][1][1:]) #removes preceeding '(' from result
        


