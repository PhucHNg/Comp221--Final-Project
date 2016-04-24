"""Count term frequencies"""
# wiki.python.org

# Import----------------------------------------------------------------------------------------------------
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string


# Class definition------------------------------------------------------------------------------------------

# Don't know if this is still relevant... ???
class WordCount(object):
    def __init__(self, word, count):
        self.word = word
        self.count = count

    def getCount(wc):
        return wc.count

    def getWord(wc):
        return wc.word

    def __repr__(self):
        return repr((self.word, self.count))

        # def __cmp__(self, other):
        #     if hasattr(other, 'count'):
        #         return self.count.__cmp__(other.count)


# Function definition-------------------------------------------------------------------------------------

# Preprocess the tweets by tokenizing the tweets and removing stop words

def tokenize(file_name):
    """ Takes as input a file name. Tokenize the tweets separating them using nltk function. Return a list of tokens"""
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


# Count frequency of words in the data

def countFrequency(file_name):
    """ Takes in a file and count number of times a word appears. Return dictionary of count"""
    count = {}
    file = open(file_name, 'r')
    for w in file:
        w = str.strip(w, '\n')
        if w not in count:
            count[w] = 0
        cc = count[w]
        count[w] = cc + 1
    file.close()
    return count


def topTen(d):
    """Rank and returns top 10 topics"""
    word_list = []
    for key in d:
        word_list.append(WordCount(key, d[key]))

    sorted(word_list, key=lambda wordcount: wordcount.count, reverse=True)
    return word_list[-1]


# Run program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    pre_data = tokenize("all_streaming_api_tweets.txt")
    data = preprocess(pre_data)


    countDict = countFrequency('all_preprocessedTweets.txt')
    top_10 = topTen(countDict)
    print(top_10)
