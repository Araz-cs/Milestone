import json
import os
import re
from indexer import Index
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment


docId = 1
index = Index(55393)
path =path = os.path.dirname(os.path.realpath(__file__))  + '/DEV/aiclub_ics_uci_edu'

for subdir, dirs, files in os.walk(path):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith("8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json"):
            #print (filepath)
            files = open(filepath)
            for i in files:
                json_load = json.loads(i)
           
            soup = BeautifulSoup(json_load['content'], "lxml")

            for tag in soup(text=lambda text: isinstance(text,Comment)):
                tag.extract()

            for element in soup.findAll(['script', 'style']):
                element.extract()
    
            space_delemited_text = re.sub('\s+',' ',soup.get_text())
            print (space_delemited_text)