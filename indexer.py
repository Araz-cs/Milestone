from nltk.stem import PorterStemmer
from nltk import ____


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


    def tf(doc_term_dict: dict, totalTerm: int, term: str):
        #doc_term_dict is a dict of term frequencies for the doc in question with the token in question
        #as the key and frequency as the value
        #total_term is total number of terms in the individual doc
        #term is the token in question

        if term in doc_term_dict.keys():
            return doc_term_dict[term]/total_term
        else:
            pass





    def porterStem(self, doc: str, docId: int, docName: str): # shoudl docName be str?
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

        # Merge docDict to self.inverted.
        for term, freq in docDict.items():
            if term in self.inverted:
                self.inverted[term].append((freq, docId))
            else:
                self.inverted[term] = [(freq, docId)]


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
