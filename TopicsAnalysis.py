"""
Preprocess tweets by tokenizing and removing stopwords.
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
from MyNGram import mle
from MyNGram import ngram
import heapq

# Function definition-------------------------------------------------------------------------------------

# Preprocess the tweets by tokenizing the tweets and removing stop words

PUNCTUATION = list(string.punctuation)
FULL_STOPWORDS = set(list(stopwords.words('english')) + PUNCTUATION + ['rt'] + ['...'])  # 'rt' for retweet
PARTIAL_STOPWORDS = set(PUNCTUATION + ['rt'] + ['...'])  # 'rt' for retweet

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


def preprocess(data, remove_all):
    """
    Takes in a list of lists of words.
    Add symbols <s> to the start of tweet and <e> to the end of tweet.
    Removes stop words, punctuations, retweet (RT) character and links.
    If remove_all is TRUE, then remove all English stopwords (e.g: a, the, to, etc.).
    Otherwise keep English stopwords which will make generated pseudo tweets more semantically coherent
    :param data: list of lists of words
    :param remove_all: boolean
    :return: a new list of lists of processed words.
    """
    newData = []
    for sentence in data:
        newSen = ['<s>']
        for word in sentence:
            if isStopword(word, remove_all): #delete all links
                newSen.append(word)
        newSen.append('<e>')
        newData.append(newSen)
    return newData


def isStopword(w, remove_all):
    """
    Check if a word is a stopword to be removed.
    If remove_all is TRUE, then remove all English stopwords (e.g: a, the, to, etc.).
    Otherwise only exclude English stopwords which will make generated pseudo tweets more semantically coherent
    :param w: word
    :param remove_all: boolean
    :return: TRUE if w is to be remove. FALSE otherwise.
    """
    if remove_all:
        remove = FULL_STOPWORDS
    else:
        remove = PARTIAL_STOPWORDS
    return w.lower() not in remove and w.lower()[:4] != 'http' #remove all links


def removeHashtags(data):
    """
    Takes in a list of lists of words.
    Remove all hashtags from the data by removing all words that start with character '#'
    :param data: list of lists of words
    :return: new list of lists of words without hashtags
    """
    newData = []
    for sentence in data:
        newSen = []
        for word in sentence:
            if word[0] != '#':
                newSen.append(word)
        newData.append(newSen)
    return newData


# Run program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    pre_data = tokenize("all_streaming_api_tweets.txt")
    data0 = preprocess(pre_data, False)
    data = removeHashtags(data0)

    my_mle = mle(data)
    unigram = my_mle.makeNgram(1)
    bigram = my_mle.makeNgram(2)
    trigram = my_mle.makeNgram(3)

    # print(topNgram(unigram))
    # print(topNgram(bigram))
    # print(topNgram(trigram))
    fm_unigram = my_mle.countFrequency(unigram)
    fm_bigram = my_mle.countFrequency(bigram)
    fm_trigram = my_mle.countFrequency(trigram)
    #pq1 = my_mle.mle(fm_unigram)
    #pq2 = my_mle.calculateMLE(fm_bigram,fm_unigram)
    #pq3 = my_mle.calculateMLE(fm_trigram, fm_bigram)
    # # print('Top 10 most frequent words in corpus')
    # # print(my_mle.topNgram(pq1, 10))
    # # print('Top 10 bigrams in corpus')
    # # print(my_mle.topNgram(pq2, 10))
    # # print('Top 10 trigrams in corpus')
    # # print(my_mle.topNgram(pq3, 10))
    #
    #
    # #Second round of test:
    bi_langMap = my_mle.buildLanguageModel(fm_bigram, fm_unigram)
    # print(my_mle.topAssociatedWords('Syrian', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('nation', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('faces', bi_langMap, 6))
    print("Pseudo tweets using bigram")
    for i in range(3):
        print(my_mle.generateTweet_Bigram(bi_langMap))

    print("Pseudo tweets using trigram")
    tri_langMap = my_mle.buildLanguageModel(fm_trigram,fm_bigram)
    # print(my_mle.topAssociatedWords('Arab League', tri_langMap, 3))
    # print(my_mle.topAssociatedWords('League killing', tri_langMap, 3))
    # print(my_mle.topAssociatedWords('killing us', tri_langMap, 5))
    # print(my_mle.topAssociatedWords('security forces', tri_langMap, 5))
    # print(my_mle.topAssociatedWords('forces Reminiscent', tri_langMap, 5))
    for i in range(3):
        print(my_mle.generateTweet_Trigram(tri_langMap,bi_langMap))





