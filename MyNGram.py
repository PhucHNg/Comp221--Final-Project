# Import----------------------------------------------------------------------------------------------------------------
from functools import total_ordering
import heapq
import math

# Function defintion----------------------------------------------------------------------------------------------------
@total_ordering
class ngram(object):
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


class mls(object):
    def __init__(self):
        self.n = 0 #count of the total number of words in the corpus
        self.vocab = {} #a dictionary of distinct words and their mapping to a distinct integer
        self.lookup_vocab = {}
        self.corpus = [] #the data represented by integers.
        self.wordfreq = {}
        return

    def initialize(self, lst):
        """
        Takes a list of lists of word.
        Construct a vocabulary for n-gram and maps each word to an integer.
        Create a corpus with each word represented by the integer instead.
        Count the frequency of each word.
        """
        i = 1
        for sentence in lst:
            newSen = []
            for word in sentence:
                self.n += 1
                if word not in self.vocab :
                    self.vocab[word] = i
                    self.lookup_vocab[i] = word
                    i += 1
                newSen.append(self.vocab[word])
            self.corpus.append(newSen)

        self.countFrequency()
        return


    def countFrequency(self):
        """
        Takes in a list of lists of words.
        Counts each word frequency and stores in a dictionary countfreq.
        """
        for sentence in self.corpus:
            for word in sentence:
                if word not in self.wordfreq:
                    self.wordfreq[word] = 0
                cc = self.wordfreq[word]
                self.wordfreq[word] = cc + 1


    def topUnigram(self):
        """
        Calculate the unigram probability for each word.
        Return 10 words with the highest probability (or frequency in the corpus)
        :return: list of top 10 most probable words
        """
        top = []
        pq = []
        for key in self.wordfreq.keys():
            des = key
            pri = math.log(self.wordfreq[key]/self.n)
            heapq.heappush(pq, ngram(pri, des))
        for i in range(0, 3): #Change range to 10 for real corpus
            id = heapq.heappop(pq)
            w = self.lookup_vocab[id.getDescription()]
            top.append(w)
        return top


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





