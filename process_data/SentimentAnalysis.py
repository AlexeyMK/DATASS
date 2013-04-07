#file to analyze sentiment
import csv
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import ngrams
from nltk import *
from collections import defaultdict
import operator
import math
import sys
from nltk.classify import *
import pickle
from SentimentLexiconManager import SentimentLexiconManager



class SentimentAnalysis:
    
    #a dict mapping meme_type to list of instances, all in lower case
    memes = defaultdict(lambda: [])
    
    
    # Function: load_memes
    # --------------------
    # loads all of the memes into self.memetype_lists as tuples of top/bottom
    def load_memes (self, filenames):
    
        for filename in filenames:
            f = open(filename, 'r')
            contents = f.readlines()
            for entry in contents:
                fields = [s.strip() for s in entry.split("|")]
                meme_type = fields[0]
                top_text = wordpunct_tokenize(fields[1].lower())
                bottom_text = wordpunct_tokenize(fields[2].lower())
                self.memes[meme_type].append ((top_text, bottom_text))
    


    # Function: constructor
    # ---------------------
    # initializes data structures
    def __init__ (self, weights_filename=None):
    
        data_filenames = [
            "../data/Foul-Bachelor-Frog data.txt",
            "../data/Futurama-Fry data.txt",
            "../data/Good-Guy-Greg- data.txt",
            "../data/Insanity-Wolf data.txt",
            "../data/Philosoraptor data.txt",
            "../data/Scumbag-Steve data.txt",
            "../data/Socially-Awkward-Penguin data.txt",
            "../data/Success-Kid data.txt",
            "../data/Paranoid-Parrot data.txt",
            "../data/Annoying-Facebook-Girl data.txt",
            "../data/First-World-Problems data.txt",
            "../data/Forever-Alone data.txt",
            "../data/The-Most-Interesting-Man-In-The-World data.txt"
        ]
        
        data_filenames_test = [
            "../data/test_data/data.txt",
            "../data/test_data/data2.txt"
        ]
    
        test1 = ['gay', 'friend', 'took', 'me', 'with', 'him', 'to', 'a', 'gay', 'bar', 'unbuttoned', 'an', 'extra', 'button', 'on', 'my', 'shirt', 'and', 'drank', 'for', 'free', 'all', 'night']
        test2 = ['this', 'hand', 'sanitizer', 'makes', 'my', 'two-carat', 'diamond', 'ring', 'dirty']
        test3 = ['ran', 'into', 'my', 'ex', 'at', 'a', 'bar', 'did', "n't", 'feel', 'a', 'goddamn', 'thing']
        test_sentence = ['I', 'Went', 'to', 'the', 'store', 'and', 'saw', 'a', 'cute', 'girl', 'but', 'i', 'was', 'too', 'shy', 'too', 'even', 'say', 'hi']
        
        #test_sentence = ['awkward', 'shy', 'help', 'sad', 'fuck', 'awkward', 'awkward']
        #test_sentence = ['my', 'girlfriend', 'gave', 'me', 'mouth', 'sex', 'and', 'it', 'was', 'awesome', 'because', 'she', 'has', 'huge', 'breasts']
        #test_sentence = ['I', 'won', 'cash', 'success']
    
    
        self.load_memes (data_filenames)
        self.sentiment_lexicon_manager = SentimentLexiconManager ('../data/inquirerbasic.csv')
        
        #get the features
        self.get_maxent_training_data ()
        
        
        #encoding = MaxentFeatureEncodingI.encode (self.maxent_training_data)
        
        if weights_filename:
            #load weighst from a user-specified file
            self.maxent_load (weights_filename)
        else:
            #train the maxent model
            self.maxent_train (self.maxent_training_data)
    
            
        #test classification
        print "### test_sentence: ", test_sentence
        probdist = self.maxent_classify (test_sentence)
        for c in probdist.samples ():
            print "     ", c, ": ", probdist.prob(c)
        
        print "### test1: ", test1,
        probdist = self.maxent_classify (test1)
        for c in probdist.samples ():
            print "     ", c, ": ", probdist.prob(c)

        print "### test2: ", test2,
        probdist = self.maxent_classify (test2)
        for c in probdist.samples ():
            print "     ", c, ": ", probdist.prob(c)
    
        print "### test3: ", test3,
        probdist = self.maxent_classify (test3)
        for c in probdist.samples ():
            print "     ", c, ": ", probdist.prob(c)



        #print "test2: ", self.maxent_classify (test2).samples (), "\n\n"
        #print "test3: ", self.maxent_classify (test3).samples (), "\n\n"
        #self.sentiment_lexicon_manager = SentimentLexiconManager (self.memes)
        


    # Function: extract_ngram_features
    # --------------------------
    # given a list of words (that form a sentence), return a dict of words mapping to true that occur in the example.
    # (i.e. we are treating it as a bag of words. this is for straight unigrams.)
    # its like a compressed version of the entire vector of features, which are boolean values for the presence/absence of certain words.
    def extract_ngram_features (self, sentence):
        return dict([(token, True) for token in sentence])
    

    # Function: get_maxent_training_data
    # ----------------------------------
    # fills self.maxent_training_data with the appropriate values
    def get_maxent_training_data (self):
        self.maxent_training_data = []
        for meme_type, instances in self.memes.iteritems ():
            for instance in instances:
        
                total = instance[0] + instance[1]
                bag_of_words = self.extract_ngram_features(total)
                sentiment_vector = self.sentiment_lexicon_manager.get_sentiment_vector (total)
    
                features = dict(bag_of_words.items () + sentiment_vector.items())
                self.maxent_training_data.append( (features, meme_type))
        return


    # Function: maxent_train
    # ----------------------
    # will train the maxent classifier.
    def maxent_train (self, training_data):
    
        self.classifier = MaxentClassifier.train (training_data, trace=100, max_iter=2)
        weights = self.classifier.weights()
        f = open ("Trained_Classifier.obj", "w")
        pickle.dump (self.classifier, f)
        f.close ()


    # Function: maxent_load
    # ---------------------
    # will load parameters from a file, stores them in self.lambdas
    def maxent_load (self, filename):
        f = open(filename, 'r')
        self.classifier = pickle.load(f)
        f.close ()

    # Function: maxent_classify
    # -------------------------
    # given a sentence, this function will classify it
    def maxent_classify (self, sentence):

        bag_of_words = self.extract_ngram_features(sentence)
        sentiment_vector = self.sentiment_lexicon_manager.get_sentiment_vector (sentence)
        features = dict(bag_of_words.items () + sentiment_vector.items())
        

        return self.classifier.prob_classify(features)
            


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "Weights Filename: ", sys.argv[1]
        sa = SentimentAnalysis (sys.argv[1])
    else:
        sa = SentimentAnalysis()
    

        
