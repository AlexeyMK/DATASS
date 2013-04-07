#sentiment lexicon manager
from collections import defaultdict
import csv
import math

class SentimentLexiconManager ():

    #dict mapping words to the sentiments they contain
    word_sentiments = defaultdict(lambda: set())
        
    #dict mapping meme-types to their sentiment vectors (normalized)
    #sentiment_vectors = defaultdict(lambda: defaultdict(lambda: 0.0))
    #sentiment_vectors_top = defaultdict(lambda: defaultdict(lambda: 0.0))
    #sentiment_vectors_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
    
    # Function: constructor
    # ---------------------
    # this function will fill word_sentiments, sentiment_vectors (top|bottom)
    def __init__ (self, filename):
        self.get_word_sentiments (filename)
    

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
    def normalize_sentiment_vector (self, sentiment_vector):
        squared_total = 0.0
        for key, value in sentiment_vector.iteritems():
            squared_total += value*value
    
        squared_total = math.sqrt(squared_total)
        for key,value in sentiment_vector.iteritems():
            sentiment_vector[key] = value / squared_total


    # Function: add_word_occurence_to_sentiment_vector
    # ------------------------------------------------
    # given a word and the meme-type under which it occurs, this function will add it's represented
    # sentiments to the meme-type's sentiment vector. discards the word if it isn't in our sentiment corpus
    def add_word_occurence_to_sentiment_vector (self, word, sentiment_vector):
        
        word = word.lower()
        this_word_sentiments = self.word_sentiments[word]
        for sentiment in this_word_sentiments:
            sentiment_vector[sentiment] += 1
        

            
    
    # Function: get_sentiment_vector
    # ----------------------------------------------
    # given sentence (a list of words), returns a normalized vector represented as a dict
    # dict maps sentiments to their count in the sentence
    def get_sentiment_vector (self, sentence):

        sentiment_vector = defaultdict(lambda: 0.0)
        for word in sentence:
            self.add_word_occurence_to_sentiment_vector (word.lower(), sentiment_vector)
        self.normalize_sentiment_vector (sentiment_vector)
        return sentiment_vector











    # Function: calculate_memetype_sentiment_vector
    # ------------------------------------
    # enter in the filename of a meme, it will calculate the sentiment vector for it.
    def calculate_memetype_sentiment_vector (self, filename):
        f = open(filename, 'r')
        
        meme_type = ''
        contents = f.readlines()
        for entry in contents:
            
            fields = [s.strip() for s in entry.split("|")]
            meme_type = fields[0]
            top_text = fields[1]
            bottom_text = fields[2]

            for word in wordpunct_tokenize(top_text):
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors[meme_type])
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors_top[meme_type])

            for word in wordpunct_tokenize(bottom_text):
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors[meme_type])
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors_bottom[meme_type])
                    
        self.normalize_sentiment_vector (self.sentiment_vectors[meme_type])
        self.normalize_sentiment_vector (self.sentiment_vectors_top[meme_type])
        self.normalize_sentiment_vector (self.sentiment_vectors_bottom[meme_type])
        #print "\n\n###########", meme_type, ": #############\n", self.sentiment_vectors[meme_type]

