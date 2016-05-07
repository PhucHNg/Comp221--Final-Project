"""
References:
Assignment 3 -- N-gram. (n.d.). Retrieved May 07, 2016, from http://www.dhgarrette.com/nlpclass/assignments/a3ngrams.html
Jurafsky, D., & Manning, C. (n.d.). Natural Language Processing: Language Modeling. Retrieved May 07, 2016, from https://class.coursera.org/nlp/lecture
Jurafsky, D., & MartinSpeech, J. H. Speech and Language Processing. Draft of September 1, 2014. Retrieved May 07, 2016, from http://lagunita.stanford.edu/c4x/Engineering/CS-224N/asset/slp4.pdf
Lab 3: Language Modeling Fever. (n.d.). Retrieved May 07, 2016, from http://www.ee.columbia.edu/~stanchen/e6884/labs/lab3/x43.html
Triglia, S. (2013, January 20). Elegent N-gram Generation in Python. Retrieved May 07, 2016, from http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
"""

# Import----------------------------------------------------------------------------------------------------------------
from functools import total_ordering
import heapq
import math
import random

# Function defintion----------------------------------------------------------------------------------------------------

@total_ordering
class ngram(object):
    """
     Class to create an ngram object which contains a description: word or sequence of words (ngram)
     and a priority: ngram's probability calculated from the corpus
    """
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        return

    def getPriority(self):
        return self.priority

    def getDescription(self):
        return self.description

    def __repr__(self):
        return repr((self.description, self.priority))

    def __lt__(self, other):
        return (self.priority > other.priority) #reverse to turn priority queue into a max heap

    def __eq__(self, other): #Is this just priority equals or two ngram object equals...???
        return (other and self.priority == other.priority and self.description == other.description)


class mle(object):
    """
    Class to create the n-gram model. This class can create and count any n-gram, but can only generate tweets from
    bigram model and trigram model.
    """
    def __init__(self, corpus):
        self.N = 0  # count of the total number of words in the corpus NOTES: hmmm what is this used for??
        self.corpus = corpus #the data: a list of lists of words
        return


    def makeNgram(self, n):
        """
        Takes n as number of words in a unit of words.
        Each unit of words is represented by a tuple
        Create ngram and returns a list of all ngram in the data
        :param n: the number of words in n-gram (e.g: 2 for bigram, 3 for trigram, etc.)
        :return: list of all n-gram in tuple
        """
        result = []
        for sentence in self.corpus:
            if len(sentence) > 3:
                self.N += len(sentence)
                for i in range(len(sentence)- (n-1)):
                    t = []
                    for j in range(n):
                        t.append(sentence[i + j])
                    result.append(tuple(t))
        return result


    def countFrequency(self,n):
        """
        Takes in a list of tuples each of which represents an n-gram.
        Counts each item's frequency and stores in a dictionary.
        :param n: the number of words in n-gram (e.g: 2 for bigram, 3 for trigram, etc.)
        :return: the dictionary of ngrams and count
        """
        alist = self.makeNgram(n)
        freqMap = {}
        for i in alist:
            if i not in freqMap:
                freqMap[i] = 0
            cc = freqMap[i]
            freqMap[i] = cc + 1
        return freqMap


    def topNgram(self, freqMap, x):
        """
        Provide the most frequent words in the corpus to help identify important topics in corpus
        :param freqMap: the dictionary of ngrams and count
        :param x: number of words to return
        :return: top x number of ngrams that have the highest frequency count
        """
        result = []
        for key in freqMap:
            if '<s>' not in key and '<e>' not in key:
                result.append(ngram(freqMap[key], key))
        result = sorted(result)
        return result[:x]


    def calculateMLE(self, current, preceding):
        """
        Calculate the probability of each ngram using maximum likelihood estimates.
        The formula for the calculation is count(current n-gram)/count(preceding n-gram)
        :param map1: frequency map of n-grams to have probability calculated (the numerator)
        :param map2: frequency map of preceeding words (the denominator)
        :return: sorted list of ngram objects: description is the n-gram, sorted in non-increasing order based on the probability
        """
        result = []
        for key in current:
            ngram_count = current[key]
            preceding_word = self.getPrecedingWord(key)
            preceding_word_count = preceding[preceding_word]
            p = math.log(ngram_count/preceding_word_count)
            result.append(ngram(p, key))
        return sorted(result)


    def getPrecedingWord(self,t):
        """
        Get the preceeding words part in an n-gram
        :param t: a tuple representing an n-gram
        :return: a tuple representing an n-1-gram or preceeding word(s)
        """
        result =[]
        for i in range(len(t)-1):
            result.append(t[i])
        return tuple(result)


    def buildLanguageModel(self, current, preceding):
        """
        Build a language model by mapping each ngram to a list of words ordered by their probabilities of following the key ngram
        :param map1: frequency map of current n-grams to have probability calculated
        :param map2: frequency map of preceding words
        :return: a dictionary, mapping a string to a list of words ordered based on their probabilities of following key ngram
        """
        mle_ngram = self.calculateMLE(current,preceding)

        langMap = {}
        for i in mle_ngram:
            t = i.getDescription()
            pw = ' '.join(self.getPrecedingWord(t)) #turn tuple into string
            if pw not in langMap:
                langMap[pw] = [t[-1]]
            else:
                l = langMap[pw]
                l.append(t[-1])
                langMap[pw] = l

        return langMap


    def topAssociatedWords(self, word, langMap, x):
        """
        :param word: a word to look up following word
        :param langMap: language model output graph
        :param x: number of words to return
        :return: Return top x words that have the highest probability of following word
        """
        associated_words_list = langMap[word]
        return associated_words_list[:x]


    def generateTweet_Bigram(self, bigram_model):
        """
        Takes a dictionary representing a Bigram language model.
        Construct some pseudo tweets based on the vocabulary in the language model.
        The function does not always append the most probable following word,
        but choose a random word in the top 30 percentile, to append to sentence to create more variety of pseudo tweets.
        :param bigram_model: bigram language model
        :return: a string of pseudo tweets
        """
        result = ''
        nxt_word = '<s>'
        while nxt_word != '<e>':
            result += nxt_word + ' '
            nxt_word_list = bigram_model[nxt_word]
            i = random.randint(0, math.ceil((len(nxt_word_list)-1)/3))
            nxt_word = nxt_word_list[i]
        return result


    def generateTweet_Trigram(self, trigram_model, bigram_model):
        """
        Takes a dictionary representing a Trigram language model.
        Construct some pseudo tweets based on the vocabulary in the language model.
        The function uses the bigram model to initialize the function.
        The function does not always append the most probable following word,
        but choose a random word in the top 30 percentile, to append to sentence to create more variety of pseudo tweets.
        :param trigram_model: trigram language model
        :param bigram_model: bigram language model
        :return: a string of pseudo tweets
        """
        i = random.randint(0, 6)
        nxt_word = "<s> " + bigram_model['<s>'][i]
        result = nxt_word
        while '<e>' not in nxt_word:
            try:
                nxt_word_list = trigram_model[nxt_word]
                i = random.randint(0, math.ceil((len(nxt_word_list) - 1) /3))
                result += ' ' + nxt_word_list[0]
                nxt_word = str.split(nxt_word)[-1] + ' ' + nxt_word_list[0]
            except KeyError:
                print("key error")
                print(nxt_word)
                break
        return result


# Run program-----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    #Test ngram class:
    a = ngram(0.5, 3)
    b = ngram(0.25, 2)
    d = ngram(0.1, 1)
    print(a==b)
    print(a < b)
    print(a > b)
    pq = [a, b, d]
    heapq.heapify(pq)
    for i in pq:
        print(i)

    #Test mle class
    dat = [['<s>', 'I', 'am', '<e>'], ['<s>', 'I', 'am', 'hungry', 'and', 'want', '<e>'], ['<s>', 'I', 'want', 'some', 'orange', 'juice', '<e>']]
    my_mle = mle(dat)
    unigram_fm = my_mle.countFrequency(1)
    bigram_fm = my_mle.countFrequency(2)
    trigram_fm = my_mle.countFrequency(3)
    print(my_mle.topNgram(unigram_fm,3))
    print(my_mle.topNgram(bigram_fm,3))
    print(my_mle.topNgram(trigram_fm,3))

    bigram_lm = my_mle.buildLanguageModel(bigram_fm,unigram_fm)
    trigram_lm = my_mle.buildLanguageModel(trigram_fm,bigram_fm)
    print(bigram_lm)
    print(trigram_lm)
    #Not testing generating tweets here because of index out of range error





