# Import----------------------------------------------------------------------------------------------------------------
from functools import total_ordering
import heapq
import math
import random

# Function defintion----------------------------------------------------------------------------------------------------

@total_ordering
class ngram(object):
    """
     An ngram object contains a word or sequence of words and its probability calculated from the corpus
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
    A maximum likelihood estimate model...
    """
    def __init__(self, corpus):
        # self.vocab = {} #a dictionary of distinct words and their mapping to a distinct integer
        # self.lookup_vocab = {}
        #NOTES: Don't need the vocabulary anymore since this is a small corpus, I'll just use words directly.
        #When things work well I'll try to encode words.

        self.n = 0  # count of the total number of words in the corpus NOTES: hmmm what is this used for??
        self.corpus = corpus #the data: a list of lists of words

        #NOTES: I can make these local variables (???)
        #self.wordfreq = {}
        # self.unigram = []
        # self.bigram = []
        return

    # NOTES: Maybe will add this back in when I have time to encode the words
    # def initialize(self, lst):
    #     """
    #     Takes a list of lists of word.
    #     Construct a vocabulary for n-gram and maps each word to an integer.
    #     Create a corpus with each word represented by the integer instead.
    #     Count the frequency of each word.
    #     """
    #     i = 1
    #     for sentence in lst:
    #         newSen = []
    #         for word in sentence:
    #             self.n += 1
    #             if word not in self.vocab :
    #                 self.vocab[word] = i
    #                 self.lookup_vocab[i] = word
    #                 i += 1
    #             newSen.append(self.vocab[word])
    #         self.corpus.append(newSen)
    #
    #     self.countFrequency()
    #     return

    def makeNgram(self, n):
        """
        Takes in a list of lists of words and n as number of words in a unit of words.
        Each unit of words is represented by a tuple
        Create ngram and returns a list of all ngram in the data
        :param n: the number of words in n-gram
        :return: list of all n-gram in tuple
        """
        result = []
        for sentence in self.corpus:
            if len(sentence) > 3:
                self.n += len(sentence)
                for i in range(len(sentence) - (n - 1)):
                    t = []
                    for j in range(n):
                        t.append(sentence[i + j])
                    result.append(tuple(t))
        return result


    def countFrequency(self,l):
        """
        Takes in a list of tuples each of which represents an n-gram.
        Counts each item's frequency and stores in a dictionary.
        :param l: list of tuples
        :return: the dictionary of item and count
        """
        fregMap = {}
        for i in l:
            if i not in fregMap:
                fregMap[i] = 0
            cc = fregMap[i]
            fregMap[i] = cc + 1
        return fregMap


    def mle(self, numerator, denominator):
        """
        Calculate the probability of each ngram using maximum likelihood estimates.
        The formula for the calculation is ______________________
        :param map1: frequency map of n-grams to have probability calculated (the numerator)
        :param map2: frequency map of preceeding words (the denominator)
        :return: priority queue of ngram objects: description is the n-gram, priority is the probability
        """
        result = []
        for key in numerator:
            ngram_count = numerator[key]
            preceeding_word = self.getPreceedingWord(key)
            preceeding_word_count = denominator[preceeding_word]
            p = math.log(ngram_count/preceeding_word_count)
            heapq.heappush(result, ngram(p, key))
        return result


    def mle(self, numerator, denominator=None):
        """
        Same as mle() but calculate the probability of each ngram using maximum likelihood estimates for unigram.
        Does not use the denominator parameter
        :return: priority queue of unigram objects: description is a word, priority is its probability
        """
        result = []
        for key in numerator:
            ngram_count = numerator[key]
            p = math.log(ngram_count/self.n)
            #heapq.heappush(result,ngram(p, key))
            result.append(ngram(p,key))
        return result


    def getPreceedingWord(self,t):
        """
        Get the preceeding words part in an n-gram
        :param t: a tuple representing an n-gram
        :return: a tuple representing an n-1-gram or preceeding word(s)
        """
        result =[]
        for i in range(len(t)-1):
            result.append(t[i])
        return tuple(result)


## This operation is not super informative however
    def topNgram(self, alist, x):
        """
        Takes in a priority queue of n-gram items.
        Return the first x items with the highest priority
        :return: a list of top x items
        """
        result = sorted(alist)
        # for i in range(x):
        #     o = heapq.heappop(alist)
        #     result.append(o.getDescription())
        return result[:x]


    def buildLanguageModel(self, alist):
        """
        Make a language model
        :param alist: list of all n-grams
        :return:
        """
        alist = sorted(alist)
        langMap = {}
        for i in alist:
            t = i.getDescription()
            pw = ' '.join(self.getPreceedingWord(t)) #turn tuple into string
            if pw not in langMap:
                langMap[pw] = [t[-1]]
            else:
                l = langMap[pw]
                l.append(t[-1])
                langMap[pw] = l
        return langMap


    def topAssociatedWords(self, word, langMap, x):
        associated_words_list = langMap[word]
        # for i in range(x):
        #     t = heapq.hea(associated_words_list).getDescription()
        #     t = t[-1]
        #     result.append(t)
        return associated_words_list[:x]

    def generatePseudoTweet(self, langMap):
        """

        :param langMap: language map: key an n-gram, value a list of unigrams that follows this n-gram, ordered by mle probabilities
        :return: a string of pseudo tweets
        """
        result = ''
        nxt_word = '<s>'
        while nxt_word != '<e>':
            result += nxt_word + ' '
            nxt_word_list = langMap[nxt_word]
            i = random.randint(0, math.ceil((len(nxt_word_list)-1)/2))
            nxt_word = nxt_word_list[i]
        return result


    def generateTrigramPseudoTweet(self, tri_langMap, bi_langMap):
        """

        :type bi_langMap: object
        """
        i = random.randint(0, 6)
        nxt_word = "<s> " + bi_langMap['<s>'][i]
        pre_word = ''
        result = nxt_word
        while '<e>' not in nxt_word:
            try:
                nxt_word_list = tri_langMap[nxt_word]
                i = random.randint(0, math.ceil((len(nxt_word_list) - 1) / 2))
                pre_word = nxt_word
                result += ' ' + nxt_word_list[i]
                nxt_word = str.split(nxt_word)[-1] + ' ' + nxt_word_list[i]
            except KeyError:
                print("key error")
                print(nxt_word)
                break
        return result






# Run program-----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    """Test"""
    # a = ngram(0.5, 3)  #the ngram class working
    # b = ngram(0.25, 2)
    # d = ngram(0.1, 1)
    # print(a==b)
    # print(a < b)
    # print(a > b)
    # pq = [a, b, d]
    # heapq.heapify(pq) #cannot see the last item
    # for i in pq:
    #     print(i)

    # dat = [['I','am'],['I','am','hungry','and','want'],['I','want','some','orange','juice']]
    # lm = mls()
    # lm.initialize(dat)
    # print(lm.n)          the mls (mazimum likelihood estimate) working...
    # for k in lm.vocab.keys():
    #     print(k, lm.vocab[k])
    # for i in lm.corpus:
    #     print(i)
    # for k in lm.wordfreq.keys():
    #     print(k, lm.wordfreq[k])

    # topUni = lm.topUnigram()  #top uni working...
    # for w in topUni:
    #     print(w)

    """New test"""
    dat = [['<s>', 'I', 'am', '<e>'], ['<s>', 'I', 'am', 'hungry', 'and', 'want', '<e>'], ['<s>', 'I', 'want', 'some', 'orange', 'juice', '<e>']]
    my_mle = mle(dat)
    unigram = my_mle.makeNgram(1)
    bigram = my_mle.makeNgram(2)
    fm = my_mle.countFrequency(unigram)
    fm2 = my_mle.countFrequency(bigram)
    pq1 = my_mle.mle(fm)
    pq2 = my_mle.mle(fm2, fm)
    top3 = my_mle.topNgram(pq1, 3)
    top3_2 = my_mle.topNgram(pq2, 3)
    print(unigram)
    print(bigram)
    print(fm)
    print(fm2)
    print(top3)
    print(top3_2)


    #Cool so makeNGram and countFrequency are both working! Yay!
    #I think mle is working..??

    bi_langMap = my_mle.buildLanguageModel(pq2)
    print(bi_langMap['I'])
    print(my_mle.generatePseudoTweet(bi_langMap))






