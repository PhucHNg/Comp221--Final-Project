"""Tokenize words preserving the hashtags and websites
Count term frequencies
Term co-occurence"""

#Import----------------------------------------------------------------------------------------------------
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string


#Function definition---------------------------------------------------------------------------------------
def tokenize(file_name): ##Could impliment an algorithm for this
    """ Takes as input a file name. Tokenize the tweets separating them using nltk function. Return a list of tokens"""
    tokenizer = TweetTokenizer(strip_handles=True)
    tokens = []
    file = open(file_name, 'r')
    for line in file:
        tokens.extend(tokenizer.tokenize(line))
    file.close()
    return tokens

def preprocess(lst):
    """ Takes in a list of words. Removes stop words and punctuations. Stem the words. Returns a new list"""
    PUNCTUATION = set(string.punctuation)
    STOPWORDS = set(stopwords.words('english')) + PUNCTUATION + set('RT')  # RT for retweet
    stemmer = PorterStemmer()
    newList = []
    for w in lst:
        if w.lower() not in STOPWORDS:
            newList.append(stemmer.stem(w))
    return newList


def stem(word): ## Or impliment an algorithm for this
    """Converting a word to its stem"""


def countFrequency(list):
    """ Takes in a list of words and count number of times a word appears"""


#Main program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unprocessed_tokens = tokenize('1218_6_tweets.txt')
    tokens = preprocess(unprocessed_tokens)
    print(tokens[0:6])
