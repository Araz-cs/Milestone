from nltk.stem import PorterStemmer
from datetime import datetime
#import json
import ujson as json
from math import log, pow, sqrt
import os
import string
from timeit import default_timer as timer
from collections import defaultdict

# def stemInput(query: str):
#     porter = PorterStemmer()
#     term = ""
#     ret = []
#     for i in range(len(query)):
#         if (query[i].isalnum()):
#             term += query[i].lower()
#         else:
#              # this is used to check if length of word is 3 or more
#             if (len(term)) >= 3:
#                 term = porter.stem(term)
#                 ret.append(term)
#                 term = ""
#             else: 
#                 term = ""
#     if term != "":
#         term = porter.stem(term)
#         ret.append(term)
#     return ret

def total_terms(d_dict:dict):
        #d_dict will be docDict in porterStem()
        counter = 0
        for value in d_dict.values():
            counter+=value
        return counter
    
def total_term_doc(index_list: list):
    counter = 0
    for value in index_list:
        counter += 1
    return counter

def tf(total_term: int, term_freq: int):
        #doc_term_dict is a dict of term frequencies for the doc in question with the token in question
        #as the key and frequency as the value
        #total_term is total number of terms in the individual doc
        #term is the token in question

        return term_freq/total_term
    
def idf(term_freq, Inverse_index_num):
    return 1+log(Inverse_index_num/term_freq)
    
def tf_idf (term_freq, inverse_doc_freq):
    return term_freq*inverse_doc_freq

def stemInput(query:str):
    start = timer()
    porter = PorterStemmer()
    queryDict= {}
    term = ""
    query = query + " "

    for i in range(len(query)):
        if (query[i].isalnum()):
            term += query[i].lower()
        else:
            if (len(term)) >= 3:
                term = porter.stem(term)
                     
                if term in queryDict:
                    queryDict[term] += 1
                else:
                    queryDict[term] = 1
                term = ""
            else:
                term = ""
    
    end = timer()
    print("stemInput: " + str(end - start))
    return queryDict

def porterstemQuery(query:str):
    start = timer()
    result_dict = defaultdict(list)

    queryDict =  stemInput(query)     
    total_words = len(queryDict.keys())
        
    for term, freq in queryDict.items():
        term_dict = get_word_dict(term)
        if term in term_dict:
            #tf-id stuff 
            term_freq = tf(total_words,freq)
            inverse_doc_freq = idf(55393, total_term_doc(term_dict[term]))
            term_freq_inverse_doc_freq = tf_idf(term_freq,inverse_doc_freq)
            queryDict[term] = (term_freq_inverse_doc_freq)

            #gather the resulting list of documents
            term_dict[term].sort(reverse=True)
            for doc in term_dict[term]:
                value_list = [doc[0],queryDict[term]]
                result_dict[doc[1]].append(value_list)   

    end = timer()
    print("porterstemQuery: " + str(end - start))
    return result_dict
   # return queryDict


def mergeQueries(results):
    start = timer()
    doc_dict = {}
    for result, tf_idfs in results.items(): 
        doc_distance = 0
        query_distance = 0
        dot_product = 0
        for num in tf_idfs:
            dot_product += (num[0]*num[1])
            doc_distance += pow(num[0],2)
            query_distance += pow(num[1],2)
        cosine_similarity = dot_product/(sqrt(query_distance)*sqrt(doc_distance))
#             if cosine_similarity > 1:
#                 pass
#             else:
        doc_dict[result] = cosine_similarity
    
    
    sorted_dict = sorted(doc_dict.items(), key = lambda x: x[1], reverse = True)

    end = timer()
    print("mergeQueries: " + str(end - start))
    return sorted_dict

def get_relevant_docs(stemmed_input: dict):
    start = timer()
    result_dict = defaultdict(list) # defaultdict to contain the results for dictionary[word]
                                    # for all words in the stemmed input. Each dict is 
                                    # sorted in descending order by tf-id                 
                                           
    for word in stemmed_input: # loop through stemmed input and find best docs
        # obtain the relevant database dictionary (i.e "apple" -> a.json, "2018" -> NUM.json)
        relevant_dict = get_word_dict(word) 
        
        if word in relevant_dict:
            result = relevant_dict[word]
            result.sort(reverse=True)
            for doc in result:
                value_list = [doc[0],stemmed_input[word]]
                result_dict[doc[1]].append(value_list)       
    
    end = timer()
    print("get_relevant_docs: " + str(end - start))     
    return result_dict

def get_word_dict(word : str):
    start = timer()
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
    end = timer()
    print("get_word_dict: " + str(end - start))   
    return filedata