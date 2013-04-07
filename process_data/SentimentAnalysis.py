#file to analyze sentiment
import csv
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from collections import defaultdict



class SentimentAnalysis:
    
    # Function: constructor
    # ---------------------
    # initializes data structures
    def __init__ (self):
        self.word_sentiments = defaultdict(lambda: set())
        self.get_word_sentiments('../data/inquirerbasic.csv')
        pass


    # Function: get_word_sentiments
    # -----------------------------
    # fills self.word_sentiments with a dict that maps each word to a set of sentiments.
    def get_word_sentiments (self, filename):

        f = csv.reader(open(filename, 'r'))
        
        #emotions will map index to word name
        emotions = f.next ()

        line = f.next ()
        prevword = 'x'
        while line:
            word = line[0].split('#')[0]
            sentiments = {emotions[i] for i in range(2, len(line)) if line[i]}
            self.word_sentiments[word] = self.word_sentiments[word] | sentiments
            line = f.next ()


    # Function: 




if __name__ == "__main__":
    sa = SentimentAnalysis()
    

        
