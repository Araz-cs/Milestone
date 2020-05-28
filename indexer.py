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

# def mergeQueries(results: list):
#     doc_dict = {}
#     for result in results:
#         for document in result:
#             if document[1] in doc_dict:
#                 doc_dict[document[1]] += document[0]
#             else:
#                 doc_dict[document[1]] = document[0]
#
#     return sorted(doc_dict.items(), key=lambda x: x[1], reverse=True)

def mergeQueries(results: list):
    doc_dict = {}
    for result in results:
        for document in result:
            if document[1] in doc_dict:
                doc_dict[document[1]] += document[0]
            else:
                doc_dict[document[1]] = document[0]

    return sorted(doc_dict.items(), key=lambda x: x[1], reverse=True)


class Index:
    def __init__(self, numFiles: int):
        self.inverted = {} # dictionary of inverted index. structure would be term as key,
                           # list of two tuples as value e.g [(freq1,docID1),(freq2,docID2)]

        self.docIndex = {} # dictionary to map doc-ids to the document in question & the number of terms
                           # key will be doc-id, value will be three-tuple of (document name/ reference, number of word sin total, number of tokens)

        self.numFiles = numFiles # this will be a constant value for the number of files.

        # in an effort to prevent having less info than we might need, here are some variables we can consider using

        self.maxTokens = (0,0) # maxTokens for a singular document. This will be a two-tuple where: (doc-id, number of tokens)

        self.maxWords = (0,0) # similarly, maxWords for a singular document. This will again be a two-tuple where: (doc-id, number of total words)

        self.folder_name = ""

        self.initialize_files()

        self.num_files_in_inverted = 0

    # def initialize_files(self):
    # Purpose: Initializes the environment for the database to be created.
    # Errors: if the database already exists the program will exit.
    def initialize_files(self):

        # obtain path to database folder which should be (cwd)\database
        cwd = os.getcwd()
        self.folder_name = os.path.join(cwd, "database")
        if os.path.exists(self.folder_name):
            print("ERROR:" + self.folder_name + "\nalready exists, remove or move it to generate a new database.")
            exit(0)

        # Create the database folder
        os.mkdir(self.folder_name)

        # Create (cwd)\database\[a-z].json files
        letters = string.ascii_lowercase
        for letter in letters:
            filename = self.folder_name + "\\" + letter + ".json"
            f = open(filename, "w+")
            f.close()

        # Create (cwd)\database\NUM.json file
        f = open(self.folder_name + "\\" + "NUM.json", "w+")
        f.close()

        # Create (cwd)\database\nonascii.json file
        f = open(self.folder_name + "\\" + "nonascii.json", "w+")
        f.close()

    def total_terms(self,d_dict:dict):
        #d_dict will be docDict in porterStem()
        counter = 0
        for value in d_dict.values():
            counter+=value
        return counter

    def total_term_doc(self, index_list: list):
        counter = 0
        for value in index_list:
            counter += 1
        return counter

    def tf(self, total_term: int, term_freq: int):
        #doc_term_dict is a dict of term frequencies for the doc in question with the token in question
        #as the key and frequency as the value
        #total_term is total number of terms in the individual doc
        #term is the token in question

        return term_freq/total_term

    def idf(self, term_freq, Inverse_index_num):
        return 1+log(Inverse_index_num/term_freq)

    def tf_idf (self, tf, idf):
        return tf*idf

    def porterstemQuery(self, query:str):
        porter = PorterStemmer()
        queryDict= {}
        term = ""

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

        total_words = self.total_terms(queryDict)

        for term, freq in queryDict.items():
           if term in self.inverted:
               tf = self.tf(total_words,freq)
               idf = self.idf(total_words,self.numFiles)
               tf_idf = self.tf_idf(tf,idf)
               queryDict[term].append(tf_idf)

    # def porterStem
    # Purpose: function will tokenize and stem the document given,
    #           then call the tf function to calculate the index
    # Assumptions:  all terms are lowercase.
    def porterStem(self, doc: list, docId: int, docName: str): # should docName be str?


        porter = PorterStemmer()
        docDict= {} # inverted index for individual document, where each term will be added to this dictionary in order to be added
                 # to the main inverted index after. This is also used to calculate tf-idf.
                 # Since this is for the indidivudal document, the structure will be a dictionary, with:
                 # key: term
                 # value: frequency

        # tokenize
        term = ""

        for i in range(len(doc)):
            for j in range(len(doc[i])):
                if (doc[i][j].isalnum()):
                    term += doc[i][j].lower()
                else:
                    # this is used to check if length of word is 3 or more
                    if (len(term)) >= 3:
                        term = porter.stem(term)

                        # stem value and append to docDict
                        if term in docDict:
                            if i == 0: # title
                                docDict[term] += 19
                            elif i == 1: # header
                                docDict[term] += 9
                            else: # i == 2
                                docDict[term] += 1
                        else:
                            if i == 0: # title
                                docDict[term] = 19
                            elif i == 1: # header
                                docDict[term] = 9
                            else: # i == 2
                                docDict[term] = 1
                        term = ""

                    else:
                        term = ""

        total_words = self.total_terms(docDict)
        #total_words is the total number of terms in the doc. It's used to calculate tf


       # Merge docDict to self.inverted.
        for term, freq in docDict.items():
           if term in self.inverted:
               tf = self.tf(total_words,freq)
               #idf = self.idf(self.numFiles, self.total_term_doc(self.docIndex[term]))
               #tf_idf = self.tf_idf(tf,idf)
               self.inverted[term].append((tf, docId))
           else:
               tf = self.tf(total_words,freq)
               #idf = self.idf(self.numFiles,self.total_term_doc(self.docIndex[term]))
               #tf_idf = self.tf_idf(tf,idf)
               self.inverted[term] = [(tf, docId)]

        # Add document info into docIndex
        # DocName, Number of unique terms in doc
        self.docIndex[docId] = (docName, len(docDict.keys()))#, sum(docDict.values()))

        # Update self.maxTokens and self.maxWords
        if len(docDict.keys()) > self.maxTokens[1]:
            self.maxTokens = (docId, len(docDict.keys()))

        if sum(docDict.values()) > self.maxWords[1]:
            self.maxWords = (docId, sum(docDict.values()))

        # Increment the number of files currently in memory
        # dump if it exceeds 10,000
        self.num_files_in_inverted +=1
        if self.num_files_in_inverted > 10000:
            self.dump_index()
            self.num_files_in_inverted = 0


    def printIndex(self):
    # placeholder function for printing the index itself for info needed for the report
        # as stated by the document:

        # "A table with assorted numbers pertaining to your index. It should have, at least the number of documents,
        # the number of [unique] tokens, and the total size (in KB) of your index on disk."

        pass

    def toFile(self):

        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        #print docfile to docindex.csv
        docfile = open("docindex.csv", "a+")
        docfile.write("Ran at: ," + str(time) + "\n")
        docfile.write("ID,URL,Keys, Values\n")
        for id, res in self.docIndex.items():
            docfile.write(str(id) + "," + str(res) + "\n")
        docfile.close()

        #print max token/word information to info.txt
        file = open("info.txt", "a+")
        file.write("Ran at:" + str(time) + "\n")
        file.write("Max Tokens\nDocument: " + str(self.maxTokens[0]) +  "\nfrom URL: " + str(self.docIndex[self.maxTokens[0]]) +  "\nTotal Tokens: " + str(self.maxTokens[1]))
        file.write("\n\n")
        file.write("Max words\nDocument: " +  str(self.maxWords[0]) + "\nfrom URL: " + str(self.docIndex[self.maxWords[0]]) + "\nTotal Tokens: " + str(self.maxWords[1]))
        #file.write("\nTotal unique keys:" + str(len(self.inverted)))
        file.close()

    def update_tfidfs(self, datastore):
        # Calculate tf-idf's
        for term in datastore:
            num_files_with_key = len(datastore[term])
            for pair in datastore[term]:
                tf = pair[0]
                idf = self.idf(num_files_with_key,55393)
                #print (str(tf) + "-" + str(idf))
                tf_idf = self.tf_idf(tf,idf)
                pair[0] = tf_idf

    # def mergeIndexes(self):
    # Function to merge [a-z].json and NUM.json
    # into a final database.json (to meet specification only)
    # ALSO: Calculates TF-IDF for documents throughout each json file.
    def mergeIndexes(self):
        letters = string.ascii_lowercase
        write_file = open("database.json", "w+")

        # Dump [a-z].json
        for letter in letters:
            filename = self.folder_name + "\\" + letter + ".json"

            datastore = self.get_dict_from_filename(filename)
            # Update tf-idfs
            self.update_tfidfs(datastore)
            # Put the json file back with updated tf-idf's
            self.dump_dict_to_json_file(datastore, filename)
            # Merge current dictionary with global dictionary file.
            json.dump(datastore,write_file)

        # Dump NUM.json
        filename = self.folder_name + "\\NUM.json"

        datastore = self.get_dict_from_filename(filename)
        # Update tf-idfs
        self.update_tfidfs(datastore)
        # Put the json file back with updated tf-idf's
        self.dump_dict_to_json_file(datastore, filename)
        # Merge current dictionary with global dictionary file.
        json.dump(datastore,write_file)

        # Dump nonascii.json
        filename = self.folder_name + "\\" + "nonascii.json"

        datastore = self.get_dict_from_filename(filename)
        # Update tf-idfs
        self.update_tfidfs(datastore)
        # Put the json file back with updated tf-idf's
        self.dump_dict_to_json_file(datastore, filename)
        # Merge current dictionary with global dictionary file.
        json.dump(datastore,write_file)


        # Close global dict
        write_file.close()

    # def get_dict_from_filename(...):
    # Function: To open a json file, load the data from it, then close the file
    # and return the dictionary of the file contents
    # (or empty dictionary if the file was empty)
    # WARNING: DELETE JSON FILE, CALL dump_dict_to_json_file()
    #   AFTER THIS IS CALLED
    # Helper function for dump_index
    def get_dict_from_filename(self, filename:str):
        if os.path.getsize(filename) > 0:
            file = open(filename, 'r')
            filedata = json.load(file)
            file.close()
            os.remove(filename)
        else:
            filedata = {}

        return filedata

    # def dump_dict_to_json_file(...):
    # Function: To open a json file, dump data to it, then close the file
    # Helper function for dump_index
    def dump_dict_to_json_file(self, dict_to_dump, filename):
        file = open(filename, "w")
        json.dump(dict_to_dump,file)
        file.close()

    # def dump_index(self):
    # Function: To dump the temporary index into its associated
    # database file [a-z, NUM, nonascii].json
    def dump_index(self):
        letters = string.ascii_lowercase
        numbers = ['0','1','2','3','4','5','6','7','8','9']

        for letter in letters:
            filename = self.folder_name + "\\" + letter + ".json"

            # Load the associated json file as a dictionary "filedata"
            filedata = self.get_dict_from_filename(filename)

            # Find all keys in self.inverted that start with [letter]
            # put them in filedata to store in the json file.
            for term, res in self.inverted.items():
                if term[0] == letter:
                    if term in filedata:
                        filedata[term].extend(self.inverted[term])
                    else:
                        filedata[term] = self.inverted[term]

            # Dump fildata to the same json file we got the data from
            # initially
            self.dump_dict_to_json_file(filedata, filename)

        # Get all keys that start with a digit, do the same as above
        filename = self.folder_name + "\\NUM.json"
        filedata = self.get_dict_from_filename(filename)

        for term, res in self.inverted.items():
            if term[0].isdigit():
                if term in filedata:
                    filedata[term].extend(self.inverted[term])
                else:
                    filedata[term] = self.inverted[term]

        self.dump_dict_to_json_file(filedata, filename)

        # Get all other keys
        filename = self.folder_name + "\\nonascii.json"
        filedata = self.get_dict_from_filename(filename)

        for term, res in self.inverted.items():
            if  ((term[0] not in numbers) and (term[0] not in letters)):
                if term in filedata:
                    filedata[term].extend(self.inverted[term])
                else:
                    filedata[term] = self.inverted[term]

        self.dump_dict_to_json_file(filedata, filename)
        self.inverted.clear()
