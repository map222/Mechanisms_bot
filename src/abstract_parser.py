'''
Parse abstracts for sentences that contain both a mechanism, and an understanding.

Notes on Pubmed objects:
Pubmed returns an XML. It is structured PubmedArticleList / PubmedArticle / MedlineCitation. MedlineCitation has children: PMID, and Article

Article has children: Journal, ArticleTitle, and Abstract

Abstract has child: AbstractText
'''

from nltk.tokenize import sent_tokenize, word_tokenize
def get_mech_sent(cur_abstract, cur_pmid):
    ''' Identify sentences which have mechanisms and understood
    
    Parameters: (These come from pubmed_io)
    cur_abstract: a string containing text of an abstract
    cur_pmid: Pubmed ID for the abstract
    
    Returns: a dictionary containing:
    mech_sent: mechanisms understood sentence
    PMID
    '''
    
    mech_words = {'mechanism', 'mechanisms', 'pathway', 'pathways', 'underpinnings'}
    understood_words = {'understood', 'unknown', 'unclear'}
    cur_sents = sent_tokenize(cur_abstract)
    mech_sent = [sent for sent in cur_sents if mech_words.intersection(set(  word_tokenize(sent) ))]
    understood_sent = [sent for sent in mech_sent if understood_words.intersection(set(  word_tokenize(sent) ))]
    if len(understood_sent) >0: # de-nest the list if it exists
        understood_sent = understood_sent[0] 
    #understood_sent = [x for x in understood_sent if x] # not sure why I had this
    return {'mech_sent':understood_sent, 'PMID': cur_pmid}