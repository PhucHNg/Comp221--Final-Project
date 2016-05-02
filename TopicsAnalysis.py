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
from MyNGram import mle

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
    Returns a new list of lists of words"""
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

def removeHashtags(data):
    """
    Remove hashtags from the data
    :param data:
    :return:
    """
    newData = []
    for sentence in data:
        newSen = []
        for word in sentence:
            if word[0] != '#':
                # w = stemmer.stem(word)
                newSen.append(word)
        newData.append(newSen)
    return newData

# Run program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    pre_data = tokenize("all_streaming_api_tweets.txt")
    data = preprocess(pre_data)
    my_mle = mle(data)
    unigram = my_mle.makeNgram(1)
    bigram = my_mle.makeNgram(2)
    trigram = my_mle.makeNgram(3)
    fm_unigram = my_mle.countFrequency(unigram)
    fm_bigram = my_mle.countFrequency(bigram)
    fm_trigram = my_mle.countFrequency(trigram)
    pq1 = my_mle.mle(fm_unigram)
    pq2 = my_mle.mle(fm_bigram,fm_unigram)
    pq3 = my_mle.mle(fm_trigram, fm_bigram)
    print('Top 10 most frequent words in corpus')
    print(my_mle.topNgram(pq1, 10))
    print('Top 10 bigrams in corpus')
    print(my_mle.topNgram(pq2, 10))
    print('Top 10 trigrams in corpus')
    print(my_mle.topNgram(pq3, 10))


    #Second round of test:
    # bi_langMap = my_mle.buildLanguageModel(pq2)
    # print(my_mle.topAssociatedWords('#Syria', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('Syrian', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('killed', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('#Assad', bi_langMap, 6))
    # print(my_mle.topAssociatedWords('forces', bi_langMap, 6))





