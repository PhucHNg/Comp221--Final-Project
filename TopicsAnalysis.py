"""
Preprocess tweets by tokenizing and removing stopwords
Create a language model that has unigram and bigram which returns word or pair of word that are most probable
in the corpus.
"""
# wiki.python.org

# Import----------------------------------------------------------------------------------------------------
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string

# Function definition-------------------------------------------------------------------------------------

# Preprocess the tweets by tokenizing the tweets and removing stop words

def tokenize(file_name):
    """ Takes as input a file name. Tokenize the tweets separating them using nltk function.
    Return a list of tokens"""
    tokenizer = TweetTokenizer(strip_handles=True)
    tokens = []
    file = open(file_name, 'r')
    for line in file:
        tokens.append(tokenizer.tokenize(line))
    file.close()
    return tokens


def preprocess(data):
    """ Takes in a list of lists of words.
    Removes stop words and punctuations.
    Stem the words.
    Returns a new list of lists of stemmed words"""
    PUNCTUATION = list(string.punctuation)
    STOPWORDS = set(list(stopwords.words('english')) + PUNCTUATION + ['rt'] + ['...'])  # 'rt' for retweet
    #stemmer = PorterStemmer() #Didn't make much sense to stem the words
    newData = []
    for sentence in data:
        newSen = []
        for word in sentence:
            if word.lower() not in STOPWORDS:
                #w = stemmer.stem(word)
                newSen.append(word)
        newData.append(newSen)
    return newData


# Run program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    pre_data = tokenize("all_streaming_api_tweets.txt")
    data = preprocess(pre_data)
