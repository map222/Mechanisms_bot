'''
Functions to get Pubmed IDs and abstracts
'''

import requests
from xml.etree import ElementTree
import pdb
import time

def get_pubmed_ids(total_abstracts = 10000):
    '''
    Gets the pubmed id of articles containing the words mechanism, and understood
    
    total_abstracts: How many abstracts in total to get; you can go up to 100,000 I think
    
    Returns:
    a list of Pubmed IDs in string format
    '''
    
    ret_max = min(total_abstracts, 500)
    start_range = range(1,total_abstracts, ret_max)
    base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/e{}.fcgi'
    pubmed_ids = []
    for cur_start in start_range:
        pubmed_dict = {'db':'pubmed', 'retmode':'json', 'field':'abstract',
                       'retstart':cur_start, 'retmax':ret_max,
                      'term':'pathways OR mechanism OR mechanisms OR pathway OR underpinnings AND understood OR unclear OR unknown'}
        #pdb.set_trace()
        pubmed_json = requests.get(base_url.format('search'), params=pubmed_dict).json()
        pubmed_ids.extend( pubmed_json['esearchresult']['idlist'] )
        time.sleep(0.5)
    return pubmed_ids

def get_pubmed_abstracts( pubmed_ids):
    ''' Queries Pubmed to get the abstracts of articles, given a pubmed id
    
    pubmed_ids: a list of pubmed ids formatted as strings
    
    Returns:
    abstracts: a list of (long) strings containing abstracts for articles
    '''
    def flatten_abstract_text(article):
        #return ' '.join([x.text for x in article.findall('AbstractText') if x.text])
        return ' '.join(str([x.text for x in article.findall('AbstractText') ]) )
    
    base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/e{}.fcgi'
    chunk_size = 500
    abstracts = []
    for cur_ids in [pubmed_ids[i:i+chunk_size] for i in range(0, len(pubmed_ids), chunk_size)]:
        abstract_dict = {'db':'pubmed', 'retmode':'xml', # only return mode option is xml
                      'id':','.join(cur_ids)}
        pubmed_xml = requests.get(base_url.format('fetch'), params=abstract_dict)
        pubmed_tree = ElementTree.fromstring(pubmed_xml.text) 
        #pdb.set_trace()
        # each 'abstract' can have multiple AbstractText fields, so need to flatten it
        articles = [ x for x in pubmed_tree.findall('./PubmedArticle/MedlineCitation/Article/Abstract')]
        try:
            next_abstracts = list(map(flatten_abstract_text, articles))
            abstracts.extend( next_abstracts )
        except:
            print('Problem parsing abstract in range{0},{1}'.format(i, i+chunksize) )
            continue
        
        time.sleep(0.2)
    
    #abstracts = [x for x in abstracts if x] # skip the rare "None" abstracts
    return abstracts

'''
Pubmed returns an XML. It is structured PubmedArticleList / PubmedArticle / MedlineCitation. MedlineCitation has children: PMID, and Article

Article has children: Journal, ArticleTitle, and Abstract

Abstract has child: AbstractText
'''