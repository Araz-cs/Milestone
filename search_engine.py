from nltk.stem import PorterStemmer
from datetime import datetime
import json
from math import log
import os
import string
import time

def stemInput(query: str):
    porter = PorterStemmer()
    term = ""
    ret = []
    for i in range(len(query)):
        if (query[i].isalnum()):
            term += query[i].lower()
        else:
             # this is used to check if length of word is 3 or more
            if (len(term)) >= 3:
                term = porter.stem(term)
                ret.append(term)
                term = ""
            else: 
                term = ""
    if term != "":
        term = porter.stem(term)
        ret.append(term)
    return ret

def mergeQueries(results):
    doc_dict = {}
    for result in results: 
        for document in result:
            if document[1] in doc_dict:
                doc_dict[document[1]] += document[0]
            else:
                doc_dict[document[1]] = document[0]
    
    return sorted(doc_dict.items(), key=lambda x: x[1], reverse=True)

def get_relevant_docs(stemmed_input :list):

    result_list = [] # list to contain the results for dictionary[word]
                     # for all words in the stemmed input. Each list is 
                     # sorted in descending order by tf-id
                     #  
    for word in stemmed_input: # loop through stemmed input and find best docs
        
        # obtain the relevant database dictionary (i.e "apple" -> a.json, "2018" -> NUM.json)
        relevant_dict = get_word_dict(word) 
        
        if word in relevant_dict:
            result = relevant_dict[word]
            result.sort(reverse=True)
            result_list.append(result)

    return result_list



def get_word_dict(word : str):
    # Get location of database
    folder_name = os.path.join(os.getcwd(), "database")
    letters = string.ascii_lowercase

    # Verify that the database exists
    if not os.path.exists(folder_name):
            print("ERROR: database not found at" + folder_name + "\nmove an existing one there or generate a new database.")
            exit(0)
    
    # Get database file relevant to query
    if word[0] in letters: # first letter of "word" is [a-z]
        filename = folder_name + "\\" + word[0] + ".json"
    elif word[0].isdigit(): # first letter of "word" is [0-9]
        filename = folder_name + "\\NUM.json"
    else:  # first letter of "word" is neither [a-z] or [0-9]
        filename = folder_name + "\\" + "nonascii.json"
    
    # check if the file exists and has data
    if os.path.exists(filename) and os.path.getsize(filename) > 0: 
            file = open(filename, 'r')
            filedata = json.load(file)
            file.close()
    else:
        filedata = {"", (0,0)}

    return filedata