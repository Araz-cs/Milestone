import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

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
            print (space_delemited_text)
            x = input()