    import json
import os
import re
from timeit import default_timer as timer
from indexer import Index
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment

space_delemited_header=""
space_delemited_title = ""
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

            start = timer()
            soup = BeautifulSoup(json_load['content'], "lxml")

            for tag in soup(text=lambda text: isinstance(text,Comment)):
                tag.extract()

            for element in soup.findAll(['script', 'style']):
                element.extract()

            # for i in soup.find_all(['title']):
            #     space_delemited_title += re.sub('\s+',' ',i.get_text()) + " "
            # # print(space_delemited_title)
            #
            # for i in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5','b','strong']):
            #     space_delemited_header += re.sub('\s+',' ',i.get_text()) + " "

            space_delemited_text = re.sub('\s+',' ',soup.get_text())
            
            #print (space_delemited_text)

<<<<<<< HEAD
            # grouped_texts will be a 3 element array (list) with the order of [title, header, text] as shown above
            grouped_texts = [space_delemited_title, space_delemited_header, space_delemited_text]
=======
           # grouped_texts will be a 3 element array (list) with the order of [title, header, text] as shown above
           # grouped_texts = [space_delemited_title, space_delemited_header, space_delemited_text]
           grouped_texts = [space_delemited_text]

           # this will then be used to call into porterStem.
>>>>>>> 56ee00224b4e33ac16117ed52a457c362a682d5c

            # this will then be used to call into porterStem.
            end = timer()
            print("Total Beautiful Soup Time: " + str(end - start))
            index.porterStem(grouped_texts,docId, json_load['url'])

            
            end2 = timer()
            print("Total Index Time: " + str(end2 - start))
            print(str(docId) + ":" + str(index.num_files_in_inverted))
            docId +=1
            #if docId == 50:
                #index.mergeIndexes()


file = open("info.txt", "a+")
time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
file.write("Ran at: " + str(time) +"\n")
file.write("Total documents read: " +  str(docId) + "\n")
file.close()
index.dump_index()
index.mergeIndexes()

exit(0)
