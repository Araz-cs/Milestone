import json
import os
import re
from indexer import Index
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, Comment


def parse_table(table):
    head_body = {'head':[], 'body':[]}
    for tr in table.select('tr'):
        if all(t.name == 'th' for t in tr.find_all(recursive=False)):
            head_body['head'] += [tr]
        else:
            head_body['body'] += [tr]
    return head_body


space_delemited_header=""
space_delemited_title = ""
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
            #table = soup.head
            #able_rows = parse_table(table)
            #print(soup.prettify())
            #print(table_rows )
            for tag in soup(text=lambda text: isinstance(text,Comment)):
                tag.extract()

            # for element in soup.find_all(re.compile('^h[1-6]$')):
            #     element.extract()


            for element in soup.findAll(['script', 'style']):
                element.extract()

            for i in soup.find_all(['title']):
                space_delemited_title += re.sub('\s+',' ',i.get_text()) + " "
            # print(space_delemited_title)

            for i in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5','b','strong']):
                space_delemited_header += re.sub('\s+',' ',i.get_text()) + " "
            # print(space_delemited_header)

            # headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
            # h_text = re.sub('\s+',' ',headers.get_text())
            # #text= soup.get_text()
            # #space_delemited_text = re.sub('\s+',' ',soup.ge())
            # print(h_text)
