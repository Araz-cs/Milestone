'''
Created on May 6, 2020

@author: Matthew Nguyen
'''
def tf(doc_term_dict: dict, total_term: int, term: str):
    if term in doc_term_dict.keys():
        return doc_term_dict[term]/total_term
    else:
        pass

if __name__ == '__main__':
    pass