#file to analyze sentiment
import csv
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from collections import defaultdict
import pprint


class SentimentAnalysis:
    
    # Function: constructor
    # ---------------------
    # initializes data structures
    def __init__ (self):
    
        #dict mapping words to the sentiments they contain
        self.word_sentiments = defaultdict(lambda: set())
        
        #dict mapping meme-types to their sentiment vectors (normalized)
        self.sentiment_vectors = defaultdict(lambda: defaultdict(lambda: 0))
        
        self.get_word_sentiments('../data/inquirerbasic.csv')
        self.calculate_sentiment_vector ('../data/Socially-Awkward-Penguin data.txt')
        
        pass


    # Function: get_word_sentiments
    # -----------------------------
    # fills self.word_sentiments with a dict that maps each word to a set of sentiments.
    def get_word_sentiments (self, filename):

        reader = csv.reader(open(filename, 'r'))
        
        #emotions will map index to word name
        emotions = reader.next ()

        i = 0
        for line in reader:
            if i > 0:
                word = line[0].split('#')[0].lower()
                sentiments = {emotions[i] for i in range(2, len(line)) if line[i]}
                self.word_sentiments[word] = self.word_sentiments[word] | sentiments
            i += 1



    # Function: normalize_sentiment_vector
    # ------------------------------------
    # makes sure the sentiment vector has a length of 1
    def normalize_sentiment_vector (sentiment_vector):
        squared_total = 0
        for (key, value) in sentiment_vector:
            total += value^2

    # Function: add_word_occurence_to_sentiment_vector
    # ------------------------------------------------
    # given a word and the meme-type under which it occurs, this function will add it's represented
    # sentiments to the meme-type's sentiment vector. discards the word if it isn't in our sentiment corpus
    def add_word_occurence_to_sentiment_vector (self, word, meme_type):
        
        word = word.lower()
        this_word_sentiments = self.word_sentiments[word]
        for sentiment in this_word_sentiments:
            self.sentiment_vectors[meme_type][sentiment] += 1
        


    # Function: calculate_sentiment_vector
    # ------------------------------------
    # enter in the filename of a meme, it will calculate the sentiment vector for it.
    def calculate_sentiment_vector (self, filename):
        f = open(filename, 'r')
        
        contents = f.readlines()
        for entry in contents:
            
            fields = [s.strip() for s in entry.split("|")]
            meme_type = fields[0]
            top_text = fields[1]
            bottom_text = fields[2]

            for word in wordpunct_tokenize(top_text):
                self.add_word_occurence_to_sentiment_vector (word, meme_type)

            for word in wordpunct_tokenize(bottom_text):
                self.add_word_occurence_to_sentiment_vector (word, meme_type)

        print pprint.pprint(self.sentiment_vectors[meme_type])
            

            
        

        





if __name__ == "__main__":
    sa = SentimentAnalysis()
    

        
