"""Count term frequencies"""
#wiki.python.org

#Import----------------------------------------------------------------------------------------------------
import nltk
import operator

#Function definition---------------------------------------------------------------------------------------

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
        word_list.append(WordCount(key,d[key]))

    sorted(word_list, key=lambda wordcount: wordcount.count, reverse = True)
    return word_list[-1]



#Main program----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    countDict = countFrequency('all_preprocessedTweets.txt')
    top_10 = topTen(countDict)
    print(top_10)
