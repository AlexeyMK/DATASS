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
    def __init__ (self, filename_all=None, filename_top=None, filename_bottom=None):
    
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
    
        #test1 = ['gay', 'friend', 'took', 'me', 'with', 'him', 'to', 'a', 'gay', 'bar', 'unbuttoned', 'an', 'extra', 'button', 'on', 'my', 'shirt', 'and', 'drank', 'for', 'free', 'all', 'night']
        #test2 = ['this', 'hand', 'sanitizer', 'makes', 'my', 'two-carat', 'diamond', 'ring', 'dirty']
        #test3 = ['ran', 'into', 'my', 'ex', 'at', 'a', 'bar', 'did', "n't", 'feel', 'a', 'goddamn', 'thing']
        #test_sentence = ['I', 'Went', 'to', 'the', 'store', 'and', 'saw', 'a', 'cute', 'girl', 'but', 'i', 'was', 'too', 'shy', 'too', 'even', 'say', 'hi']
        #test_sentence = ['awkward', 'shy', 'help', 'sad', 'fuck', 'awkward', 'awkward']
        #test_sentence = ['my', 'girlfriend', 'gave', 'me', 'mouth', 'sex', 'and', 'it', 'was', 'awesome', 'because', 'she', 'has', 'huge', 'breasts']
        #test_sentence = ['I', 'won', 'cash', 'success']
    
    
        self.load_memes (data_filenames)
        self.sentiment_lexicon_manager = SentimentLexiconManager ('../data/inquirerbasic.csv')
        
        #get the features
        self.get_maxent_training_data ()
        
        #encoding = MaxentFeatureEncodingI.encode (self.maxent_training_data)
        
        if filename_all and filename_top and filename_bottom:
            #load weighst from a user-specified file
            self.maxent_load (filename_all, filename_top, filename_bottom)
        else:
            #train the maxent model
            self.maxent_train (self.maxent_training_data)
        


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
        
                bottom_text = instance[0]
                
                bag_of_words = self.extract_ngram_features(bottom_text)
                sentiment_vector = self.sentiment_lexicon_manager.get_sentiment_vector (bottom_text)
    
                features = dict(bag_of_words.items () + sentiment_vector.items())
                self.maxent_training_data.append( (features, meme_type))
        return


    # Function: maxent_train
    # ----------------------
    # will train the maxent classifier.
    def maxent_train (self, training_data):
    
        self.classifier = MaxentClassifier.train (training_data, trace=100, max_iter=4)
        weights = self.classifier.weights()
        f = open ("Trained_Classifier_Bottom.obj", "w")
        pickle.dump (self.classifier, f)
        f.close ()


    # Function: maxent_load
    # ---------------------
    # will load parameters from a file, stores them in self.lambdas
    def maxent_load (self, filename_all, filename_top, filename_bottom):

        
        print filename_all
        print filename_top
        print filename_bottom
        f_all = open(filename_all, 'r')
        self.classifier_all = pickle.load(f_all)
        print "loaded all..."
        
        f_top = open(filename_top, 'r')
        self.classifier_top = pickle.load(f_top)
        print "loaded top..."
        
        f_bottom = open(filename_all, 'r')
        self.classifier_bottom = pickle.load(f_bottom)
        print "loaded bottom..."
    
        f_all.close ()
        f_top.close ()
        f_bottom.close ()
    

    # Function: maxent_classify
    # -------------------------
    # given a sentence, this function will classify it
    def maxent_classify (self, sentence):

        bag_of_words = self.extract_ngram_features(sentence)
        sentiment_vector = self.sentiment_lexicon_manager.get_sentiment_vector (sentence)
        features = dict(bag_of_words.items () + sentiment_vector.items())
        
	prob_all = self.classifier_all.prob_classify(features)
	prob_top = self.classifier_top.prob_classify(features)
	prob_bottom = self.classifier_bottom.prob_classify(features)
	#for p in prob_all.samples ():
		#prob_all.prob[p] = prob_top.prob(p) + 3*prob_bottom.prob(p)
		#print prob_all(p)

        #return self.classifier_all.prob_classify(features)
        #return self.classifier_top.prob_classify (features)
        #return self.classifier_bottom.prob_classify (features)
	return [prob_all, prob_top, prob_bottom]


    # Function: maxent_classify_raw
    # -----------------------------
    # given a raw sentence, this will tokenize it then classify it.
    def maxent_classify_raw (self, sentence_raw):
        
        sentence = wordpunct_tokenize(sentence_raw)
        return self.maxent_classify(sentence)
        
        pass
            


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if (sys.argv[1] == 'load'):
            print "Using Pretrained Classifiers: "
            filename_all = 'Trained_Classifier.obj'
            filename_top = 'Trained_Classifier_Top.obj'
            filename_bottom = 'Trained_Classifier_Bottom.obj'
            sa = SentimentAnalysis (filename_all, filename_top, filename_bottom)
    else:
        sa = SentimentAnalysis()
    

        
