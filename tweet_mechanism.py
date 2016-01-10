from Mechanisms_bot.src import abstract_parser
from Mechanisms_bot.src import pubmed_io
from Mechanisms_bot.src import twitter_io
import pickle
import logging
import pdb

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('mechanisms_bot.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def get_recent_mech_sentences():
    '''
    Queries Pubmed for recent papers using mechanisms understood syntax. Then get the abstracts. 
    Then does some NLP to get the sentences out, and returns them.
    
    Returns:
    good_sents: a list of dictionaries containing mechanisms sentences and PMIDs'''
    logger.info('Getting recent papers')
    recent_pmids = pubmed_io.get_pubmed_ids(100)
    logger.info('Got {} recent PubMed IDs'.format(len(recent_pmids)))
    logger.info('Getting abstracts')
    recent_abstracts = pubmed_io.get_pubmed_abstracts( recent_pmids)
    logger.info('Downloaded {} abstracts'.format( len(recent_abstracts) ) )

    # get the sentences and ids
    good_sents = list(map(abstract_parser.get_mech_sent, recent_abstracts, recent_pmids) )
    good_sents = [x for x in good_sents if x['mech_sent']] # delete empty abstracts
    logger.info('Found {} mechanisms sentences\n'.format(len(good_sents)) )
    return good_sents

def main():
    # load tweeted abstracts
    with open('tweeted_sentences.pickle', 'rb') as pickle_file:
        tweeted_sentences = pickle.load(pickle_file)
        
    # get new abstracts
    new_sentences = get_recent_mech_sentences()
    tweeted_sentences = twitter_io.tweet_new_sentence( new_sentences, tweeted_sentences)
    
    # save the new tweeted_
    with open('tweeted_sentences.pickle', 'wb') as pickle_file:
        pickle.dump(tweeted_sentences, pickle_file )
    
    return new_sentences, tweeted_sentences

if __name__ == '__main__':
    main()