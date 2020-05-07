class Index:
    def __init__(self):
        self.inverted = {}


    def tf(doc_term_dict: dict, totalTerm: int, term: str):
        #doc_term_dict is a dict of term frequencies for the doc in question with the token in question
        #as the key and frequency as the value
        #total_term is total number of terms in the individual doc
        #term is the token in question

        if term in doc_term_dict.keys():
            return doc_term_dict[term]/total_term
        else:
            pass

    def porterStem(self):
        pass

        
