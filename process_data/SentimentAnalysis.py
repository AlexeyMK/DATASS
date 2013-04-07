#file to analyze sentiment
import csv
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import ngrams
from collections import defaultdict
import operator
import math



class SentimentAnalysis:
    
    
    
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
                self.memetype_lists[meme_type].append ((top_text, bottom_text))
    




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
        
        
        #test_sentence = ['I', 'Went', 'to', 'the', 'store', 'and', 'saw', 'a', 'cute', 'girl', 'but', 'i', 'was', 'too', 'shy', 'too', 'even', 'say', 'hi']
        #test_sentence = ['awkward', 'shy', 'help', 'sad', 'fuck', 'awkward', 'awkward']
        #test_sentence = ['my', 'girlfriend', 'gave', 'me', 'mouth', 'sex', 'and', 'it', 'was', 'awesome', 'because', 'she', 'has', 'huge', 'breasts']
        test_sentence = ['I', 'won', 'cash', 'success']
    
    
        ###########################################################################################################################
        ###################################################[ NGRAMS VECTORS ]###################################################
        ########################################################################################################################### 
    
        #dict mapping memes (meme_type strings) to their text in (top, bottom) tuples
        self.memetype_lists = defaultdict(lambda: [])
        self.load_memes (data_filenames)
        self.get_ngrams_memetype ()
        
        
        (test_unigram_vector, test_bigram_vector) = self.get_ngrams_sentence(test_sentence)
        print test_unigram_vector
        print test_bigram_vector
        
        matches_all_uni = {}
        matches_top_uni = {}
        matches_bottom_uni = {}
        for v in self.memetype_unigrams_top:
            cosine = self.calculate_cosine_similarity (test_unigram_vector, self.memetype_unigrams_top[v])
            matches_top_uni[v] = cosine
        sorted_top_uni = sorted(matches_top_uni.iteritems(), key=operator.itemgetter(1))
        
        for v in self.memetype_unigrams_bottom:
            cosine = self.calculate_cosine_similarity (test_unigram_vector, self.memetype_unigrams_bottom[v])
            matches_bottom_uni[v] = cosine
        sorted_bottom_uni = sorted(matches_bottom_uni.iteritems(), key=operator.itemgetter(1))
    
        for v in self.memetype_unigrams_all:
            cosine = self.calculate_cosine_similarity (test_unigram_vector, self.memetype_unigrams_all[v])
            matches_all_uni[v] = cosine
        sorted_all_uni = sorted(matches_all_uni.iteritems(), key=operator.itemgetter(1))
    
    
        print "########## UNIGRAM COSINE SIMILARITY ###########\n"
        print "#### TOP ALL:"
        for v in sorted_all_uni:
            print v[0], ": ", v[1]
        
        print "#### TOP TOP:"
        for v in sorted_top_uni:
            print v[0], ": ", v[1]
            
        print "#### TOP BOTTOM:"
        for v in sorted_bottom_uni:
            print v[0], ": ", v[1]
    
    
        
        ###########################################################################################################################
        ###################################################[ SENTIMENT VECTORS ]###################################################
        ###########################################################################################################################         

        #dict mapping words to the sentiments they contain
        self.word_sentiments = defaultdict(lambda: set())
        
        #dict mapping meme-types to their sentiment vectors (normalized)
        self.sentiment_vectors = defaultdict(lambda: defaultdict(lambda: 0.0))
        self.sentiment_vectors_top = defaultdict(lambda: defaultdict(lambda: 0.0))
        self.sentiment_vectors_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
        
        # Get the sentiment vectors for each meme
        self.get_word_sentiments('../data/inquirerbasic.csv')
        for filename in data_filenames:
            self.calculate_memetype_sentiment_vector (filename)
        
        test_sentiment_vector = self.calculate_sentence_sentiment_vector(test_sentence)


        matches_all = {}
        matches_top = {}
        matches_bottom = {}
        
        
        for v in self.sentiment_vectors:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors[v], test_sentiment_vector)
            matches_all[v] = cosine
        sorted_all = sorted(matches_all.iteritems(), key=operator.itemgetter(1))
        
        for v in self.sentiment_vectors_top:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors_top[v], test_sentiment_vector)
            matches_top[v] = cosine
        sorted_top = sorted(matches_top.iteritems(), key=operator.itemgetter(1))
        
        for v in self.sentiment_vectors_bottom:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors_bottom[v], test_sentiment_vector)
            matches_bottom[v] = cosine
        sorted_bottom = sorted(matches_bottom.iteritems(), key=operator.itemgetter(1))
        
    
    
        for v in self.sentiment_vectors:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors[v], test_sentiment_vector)
            matches_all[v] = cosine
        sorted_all = sorted(matches_all.iteritems(), key=operator.itemgetter(1))

        for v in self.sentiment_vectors_top:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors_top[v], test_sentiment_vector)
            matches_top[v] = cosine
        sorted_top = sorted(matches_top.iteritems(), key=operator.itemgetter(1))
       
        for v in self.sentiment_vectors_bottom:
            cosine = self.calculate_cosine_similarity (self.sentiment_vectors_bottom[v], test_sentiment_vector)
            matches_bottom[v] = cosine
        sorted_bottom = sorted(matches_bottom.iteritems(), key=operator.itemgetter(1))
            
        print "########## SENTIMENT VECTOR COSINE SIMILARITY ###########\n"
        print "#### TOP ALL:"
        for v in sorted_all:
            print v[0], ": ", v[1]
        
        print "#### TOP TOP:"
        for v in sorted_top:
            print v[0], ": ", v[1]
            
        print "#### TOP BOTTOM:"
        for v in sorted_bottom:
            print v[0], ": ", v[1]




    ###########################################################################################################################
    ###################################################[ SENTIMENT VECTORS ]###################################################
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
            
            
    
    # Function: calculate_sentence_sentiment_vectors
    # ----------------------------------------------
    # given a list of words that make up a sentence, this function will return a sentiment vector
    def calculate_sentence_sentiment_vector (self, sentence):

        sentiment_vector = defaultdict(lambda: 0.0)
        for word in sentence:
            self.add_word_occurence_to_sentiment_vector (word.lower(), sentiment_vector)
        self.normalize_sentiment_vector (sentiment_vector)
        #print "############## sentence vector: ###############\n"
        return sentiment_vector
    

    # Function: calculate_cosine_similarity
    # -------------------------------------
    # basically take the dot-product between two vectors in order to find the theta between them
    def calculate_cosine_similarity (self, sentence_vector, meme_type_vector):

        sum = 0.0
        for key, value in sentence_vector.iteritems ():
            sum += sentence_vector[key] * meme_type_vector[key]
        return sum
            


    ###########################################################################################################################
    ###################################################[ NGRAMS ]##############################################################
    ###########################################################################################################################
    
    #dict mapping memetypes to dicts that map unigrams to their frequency
    memetype_unigrams_top = defaultdict(lambda: defaultdict(lambda: 0.0))
    memetype_unigrams_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
    memetype_unigrams_all = defaultdict(lambda: defaultdict(lambda: 0.0))
    
    memetype_bigrams_top = defaultdict(lambda: defaultdict(lambda: 0.0))
    memetype_bigrams_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
    memetype_bigrams_all = defaultdict(lambda: defaultdict(lambda: 0.0))


    # Function: add_ngrams
    # --------------------
    # will add in the ngrams to the memetype_(uni|bi)grams dicts
    def add_ngrams(self, key, top_unigrams, bottom_unigrams, all_unigrams, top_bigrams, bottom_bigrams, all_bigrams):
    
        for unigram in top_unigrams:
            self.memetype_unigrams_top[key][unigram] += 1
            self.memetype_unigrams_all[key][unigram] += 1
        for unigram in bottom_unigrams:
            self.memetype_unigrams_bottom[key][unigram] += 1
            self.memetype_unigrams_all[key][unigram] += 1

        for bigram in top_bigrams:
            self.memetype_bigrams_top[key][bigram] += 1
            self.memetype_bigrams_all[key][bigram] += 1
        for bigram in bottom_bigrams:
            self.memetype_bigrams_bottom[key][bigram] += 1
            self.memetype_bigrams_all[key][bigram] += 1
    

    # Function: get_ngrams_memetype
    # -----------------------------
    # given a memetype filename, this function will extract all uni- and bigrams and their counts.
    def get_ngrams_memetype (self):
        for key in self.memetype_lists:
            for meme in self.memetype_lists[key]:

                top_unigrams = meme[0]
                bottom_unigrams = meme[1]
                all_unigrams = top_unigrams + bottom_unigrams

                top_bigrams = ngrams (meme[0], 2)
                bottom_bigrams = ngrams (meme[1], 2)
                all_bigrams = top_bigrams + bottom_bigrams

                self.add_ngrams(key, top_unigrams, bottom_unigrams, all_unigrams, top_bigrams, bottom_bigrams, all_bigrams)

            self.normalize_sentiment_vector (self.memetype_unigrams_top[key])
            self.normalize_sentiment_vector (self.memetype_bigrams_top[key])
            self.normalize_sentiment_vector (self.memetype_unigrams_bottom[key])
            self.normalize_sentiment_vector (self.memetype_bigrams_bottom[key])
            self.normalize_sentiment_vector (self.memetype_unigrams_all[key])
            self.normalize_sentiment_vector (self.memetype_bigrams_all[key])


    # Function: get_ngrams_sentence
    # -----------------------------
    # computes unigrams and bigrams for a sentence
    def get_ngrams_sentence (self, sentence):

        unigram_vector = defaultdict(lambda: 0.0)
        bigram_vector = defaultdict(lambda: 0.0)
        unigrams = sentence
        bigrams = ngrams(sentence, 2)
        for unigram in unigrams:
            unigram_vector[unigram] += 1
        for bigram in bigrams:
            bigram_vector[bigram] += 1
            
        self.normalize_sentiment_vector (unigram_vector)
        self.normalize_sentiment_vector (bigram_vector)
    
        
        return (unigram_vector, bigram_vector)





if __name__ == "__main__":
    sa = SentimentAnalysis()
    

        
