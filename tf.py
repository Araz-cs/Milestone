'''
Created on May 6, 2020

@author: Matthew Nguyen
'''
def tf(doc_term_dict: dict, total_term: int, term: str):
    #doc_term_dict is a dict of term frequencies for the doc in question with the token in question 
    #as the key and frequency as the value
    #total_term is total number of terms in the doc
    #term is the token in question
    
    if term in doc_term_dict.keys():
        return doc_term_dict[term]/total_term
    else:
        pass

if __name__ == '__main__':
    pass