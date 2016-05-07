"""
Preprocess tweets by tokenizing and removing stopwords.
Create a language model that has unigram and bigram which returns word or pair of word that are most probable
in the corpus.

References:
marcobonzanini.com
stackoverflow.com
wiki.python.org
"""


# Import----------------------------------------------------------------------------------------------------
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
from MyNGram import mle

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
    #First preprocess the tweets:
    pre_data = tokenize("all_streaming_api_tweets.txt")
    data0 = preprocess(pre_data, False)
    data = removeHashtags(data0)

    #Create an Maximum Likelihood Estimate object
    my_mle = mle(data)

    #Make n-grams and count frequency of n-grams:
    unigram_freqMap = my_mle.countFrequency(1)
    bigram_freqMap = my_mle.countFrequency(2)
    trigram_freqMap = my_mle.countFrequency(3)

    print('Top 10 most frequent words in corpus') #These results exclude words with hashtags
    print(my_mle.topNgram(unigram_freqMap, 10))
    print('Top 10 bigrams in corpus')
    print(my_mle.topNgram(bigram_freqMap, 10))
    print('Top 10 trigrams in corpus')
    print(my_mle.topNgram(trigram_freqMap, 10))

    #Build language models to generate tweets
    bigram_langMod = my_mle.buildLanguageModel(bigram_freqMap, unigram_freqMap)
    print("Pseudo tweets using bigram")

    for i in range(3):
        print(my_mle.generateTweet_Bigram(bigram_langMod))

    trigram_langMod = my_mle.buildLanguageModel(trigram_freqMap, bigram_freqMap)
    print("Pseudo tweets using trigram")

    for i in range(3):
        print(my_mle.generateTweet_Trigram(trigram_langMod, bigram_langMod)) #To run trigram tweet generator, need both trigram and bigram language model





