from nltk.stem import PorterStemmer
from datetime import datetime
import json


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


    def total_terms(self,d_dict:dict):
        #d_dict will be docDict in porterStem()
        counter = 0
        for value in d_dict.values():
            counter+=value
        return counter
    
    def tf(self, total_term: int, term_freq: int):
        #doc_term_dict is a dict of term frequencies for the doc in question with the token in question
        #as the key and frequency as the value
        #total_term is total number of terms in the individual doc
        #term is the token in question

        return term_freq/total_term
      


    def porterStem(self, doc: str, docId: int, docName: str): # should docName be str?
        # function will tokenize and stem the document given, then call the tf function to calculate the
        # index
        # assuming all terms are lowercase.

        porter = PorterStemmer()
        docDict= {} # inverted index for individual document, where each term will be added to this dictionary in order to be added
                 # to the main inverted index after. This is also used to calculate tf-idf.
                 # Since this is for the indidivudal document, the structure will be a dictionary, with:
                 # key: term
                 # value: frequency

        # tokenize
        term = ""

        for i in range(len(doc)):
            if (doc[i].isalnum()):
                term += doc[i].lower()
            else:
                # this is used to check if length of word is 3 or more
                if (len(term)) >= 3:
                    term = porter.stem(term)

                    # stem value and append to docDict
                    if term in docDict:
                        docDict[term] += 1
                    else:
                        docDict[term] = 1
                    term = ""

                else:
                    term = ""

        # tf-id stuff here??
        total_words = self.total_terms(docDict) 
        #total_words is the total number of terms in the doc. It's used to calculate tf

        # Merge docDict to self.inverted.
        for term, freq in docDict.items():
            if term in self.inverted:
                self.inverted[term].append((self.tf(total_words,freq), docId))
            else:
                self.inverted[term] = [(self.tf(total_words,freq), docId)]


        # Add document info into docIndex
        self.docIndex[docId] = (docName, len(docDict.keys()), sum(docDict.values()))

        # Update self.maxTokens and self.maxWords
        if len(docDict.keys()) > self.maxTokens[1]:
            self.maxTokens = (docId, len(docDict.keys()))

        if sum(docDict.values()) > self.maxWords[1]:
            self.maxWords = (docId, sum(docDict.values()))


    def printIndex(self):
    # placeholder function for printing the index itself for info needed for the report
        # as stated by the document:

        # "A table with assorted numbers pertaining to your index. It should have, at least the number of documents,
        # the number of [unique] tokens, and the total size (in KB) of your index on disk."

        pass

    def toFile(self):
        # function to send the inverted index to a file. 
        with open("database.json", "w+") as write_file:
            json.dump(self.inverted, write_file)
        
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
        file.write("\nTotal unique keys:" + str(len(self.inverted)))
        file.close()

   # def fromFile(self):
        # funtion to retrieve a 
