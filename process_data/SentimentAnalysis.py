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
    
        data_filenames = [
            "../data/Foul-Bachelor-Frog data.txt",
            "../data/Futurama-Fry data.txt",
            "../data/Good-Guy-Greg- data.txt",
            "../data/Insanity-Wolf data.txt",
            "../data/Philosoraptor data.txt",
            "../data/Scumbag-Steve data.txt",
            "../data/Socially-Awkward-Penguin data.txt",
            "../data/Success-Kid data.txt",
            "../data/Paranoid-Parrot data.txt"
        ]
            
    
    
        #dict mapping words to the sentiments they contain
        self.word_sentiments = defaultdict(lambda: set())
        
        #dict mapping meme-types to their sentiment vectors (normalized)
        self.sentiment_vectors = defaultdict(lambda: defaultdict(lambda: 0.0))
        
        # Get the sentiment vectors for each meme
        self.get_word_sentiments('../data/inquirerbasic.csv')
        for filename in data_filenames:
            self.calculate_memetype_sentiment_vector (filename)
        
        
        #sv = self.calculate_sentence_sentiment_vector(['I', 'Went', 'to', 'the', 'store', 'and', 'saw', 'a', 'cute', 'girl', 'but', 'i', 'was', 'too', 'shy', 'too', 'even', 'say', 'hi'])
        sv = self.calculate_sentence_sentiment_vector(['awkward', 'shy', 'help', 'sad', 'fuck', 'awkward', 'awkward'])

    
        cs = []
        for v in self.sentiment_vectors:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors[v], sv)
            print v, " : ", cosine
        
        
        pass



    ###########################################################################################################################
    ############################################[ GETTING SENTIMENT VECTORS ]##################################################
    ###########################################################################################################################    

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
        

    # Function: calculate_memetype_sentiment_vector
    # ------------------------------------
    # enter in the filename of a meme, it will calculate the sentiment vector for it.
    def calculate_memetype_sentiment_vector (self, filename):
        f = open(filename, 'r')
        
        contents = f.readlines()
        for entry in contents:
            
            fields = [s.strip() for s in entry.split("|")]
            meme_type = fields[0]
            top_text = fields[1]
            bottom_text = fields[2]

            for word in wordpunct_tokenize(top_text):
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors[meme_type])

            for word in wordpunct_tokenize(bottom_text):
                self.add_word_occurence_to_sentiment_vector (word, self.sentiment_vectors[meme_type])
    
        self.normalize_sentiment_vector (self.sentiment_vectors[meme_type])
        print "\n\n###########", meme_type, ": #############\n", self.sentiment_vectors[meme_type]
            

    # Function: calculate_sentence_sentiment_vectors
    # ----------------------------------------------
    # given a list of words that make up a sentence, this function will return a sentiment vector
    def calculate_sentence_sentiment_vector (self, sentence):

        sentiment_vector = defaultdict(lambda: 0.0)
        for word in sentence:
            self.add_word_occurence_to_sentiment_vector (word.lower(), sentiment_vector)
        self.normalize_sentiment_vector (sentiment_vector)
        print "############## sentence vector: ###############\n"
        print sentiment_vector
        return sentiment_vector

    

    # Function: calculate_cosine_similarity
    # -------------------------------------
    # basically take the dot-product between two vectors in order to find the theta between them
    def calculate_cosine_similarity (self, sentence_vector, meme_type_vector):

        sum = 0.0
        for key, value in sentence_vector.iteritems ():
            sum += sentence_vector[key] * meme_type_vector[key]
        return sum
            
        

        





if __name__ == "__main__":
    sa = SentimentAnalysis()
    

        
