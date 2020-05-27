import json
import os
import re
from Milestone.indexer import Index
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment


docId = 1
index = Index(55393)
path =path = os.path.dirname(os.path.realpath(__file__))  + '/DEV'

for subdir, dirs, files in os.walk(path):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".json"):
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
           # print (space_delemited_text)
            index.porterStem(space_delemited_text,docId, json_load['url'])
            print(str(docId) + ":" + str(index.num_files_in_inverted))
            docId +=1
            #if docId == 50:
            #    index.toFile()


file = open("info.txt", "a+")
time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
file.write("Ran at: " + str(time) +"\n")
file.write("Total documents read: " +  str(docId) + "\n")
file.close()
index.dump_index()
index.mergeIndexes()

exit(0)