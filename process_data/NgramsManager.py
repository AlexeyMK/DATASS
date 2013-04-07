#manages ngrams
from nltk import ngrams
from nltk.classify import MaxentClassifier
from collections import defaultdict


class NgramsManager ():


    #dict mapping meme types to lists of 'vectors' representing each meme instance
    #note: these vectors are actually dicts to keep it sparse
    maxent_memes_top = []
    maxent_memes_bottom = defaultdict (lambda: [])
    maxent_memes_all = []

    #dict mapping memetypes to dicts mapping unigrams to their frequency
    unigrams_top = defaultdict(lambda: defaultdict(lambda: 0.0))
    unigrams_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
    unigrams_all = defaultdict(lambda: defaultdict(lambda: 0.0))
    
    bigrams_top = defaultdict(lambda: defaultdict(lambda: 0.0))
    bigrams_bottom = defaultdict(lambda: defaultdict(lambda: 0.0))
    bigrams_all = defaultdict(lambda: defaultdict(lambda: 0.0))


    def __init__ (self, memes):
        #memes: a dict from a memetype to a list of (top,bottom) tuples
    
    
        self.fill_maxent_memes (memes)
        self.maxent_train ()
        
        #fills all of the unigrams/bigrams dicts
        #self.extract_ngram_vectors (memes)
    



    
    #########################################################################################################################
    ################################[ MAXENT ]###############################################################################
    #########################################################################################################################


    # Function: extract_features
    # --------------------------
    # given a list of words (that form a sentence), return a dict of words mapping to true that occur in the example.
    # (i.e. we are treating it as a bag of words. this is for straight unigrams.)
    # its like a compressed version of the entire vector of features, which are boolean values for the presence/absence of certain words.
    def extract_features (self, sentence):
        return dict([(token, True) for token in sentence])
    
    
    # Function: fill_maxent_memes
    # ---------------------------
    # fills maxent_memes_(top|bottom|all) with sparse vector versions of their bag of words
    def fill_maxent_memes (self, memes):
        for meme_type, instances in memes.iteritems():
            for instance in instances:
    
                self.maxent_memes_all.append ((self.extract_features(instance[0] + instance[1]), meme_type))
        
        #for meme_type in memes:
        #    for instance in memes[meme_type]:
        #        self.maxent_memes_top[meme_type].append(self.extract_features(instance[0]))
        #        self.maxent_memes_bottom[meme_type].append(self.extract_features(instance[1]))
        #        self.maxent_memes_all[meme_type].append(self.extract_features(instance[0] + instance[1]))
    


    def maxent_train (self):
    
        self.classifier_all = MaxentClassifier.train (self.maxent_memes_all, trace=100, max_iter=5)
        #classifier_bottom = MaxentClassifier.train (maxent_memes_bottom, trace=100, max_iter=250)
        #classifier_all = MaxentClassifier.train (maxent_memes_all, trace=100, max_iter=250)
        weights = self.classifier_all.weights()
        f = open ("lambdas.txt", "w")
        for weight in weights:
            f.write("weight = %f" % weight)
            f.write ("\n")
    
    
        

    # Function: maxent_classify
    # -------------------------
    # assumes that the sentence is a list of words. returns a probability dist over the classes
    def maxent_classify (sentence):
        
        features = extract_features(sentence)
        probdist = MaxentClassifier.classify(self, features)
        print probdist
        return probdist
        
        
        
            


    #########################################################################################################################
    ###########################[ COSINE SIMILARITY ]#########################################################################
    #########################################################################################################################

    # Function: add_ngrams
    # --------------------
    # will add in the ngrams to the memetype_(uni|bi)grams dicts
    def add_ngrams(self, key, top_unigrams, bottom_unigrams, all_unigrams, top_bigrams, bottom_bigrams, all_bigrams):
    
        for unigram in top_unigrams:
            self.unigrams_top[key][unigram] += 1
            self.unigrams_all[key][unigram] += 1
        for unigram in bottom_unigrams:
            self.unigrams_bottom[key][unigram] += 1
            self.unigrams_all[key][unigram] += 1

        for bigram in top_bigrams:
            self.bigrams_top[key][bigram] += 1
            self.bigrams_all[key][bigram] += 1
        for bigram in bottom_bigrams:
            self.bigrams_bottom[key][bigram] += 1
            self.bigrams_all[key][bigram] += 1


    # Function: extract_ngrams
    # -----------------------------
    # fills uni/bigrams_top/bottom/all with counts of how many times they occur in all meme instances for each meme type
    def extract_ngrams (self, memes):
        for meme_type in memes:
            for meme in memes[meme_type]:
                top_unigrams = meme[0]
                bottom_unigrams = meme[1]
                all_unigrams = top_unigrams + bottom_unigrams

                top_bigrams = ngrams (meme[0], 2)
                bottom_bigrams = ngrams (meme[1], 2)
                all_bigrams = top_bigrams + bottom_bigrams

                self.add_ngrams(key, top_unigrams, bottom_unigrams, all_unigrams, top_bigrams, bottom_bigrams, all_bigrams)



    # Function: get_noramlized_vectors
    # --------------------------------
    # normalizes the vectors of ngrams for computing cosine similarity
    def get_normalized_vectors (self):
    
        self.normalize_vector (self.unigrams_top[meme_type])
        self.normalize_vector (self.bigrams_top[meme_type])
        self.normalize_vector (self.unigrams_bottom[meme_type])
        self.normalize_vector (self.bigrams_bottom[meme_type])
        self.normalize_vector (self.unigrams_all[meme_type])
        self.normalize_vector (self.bigrams_all[meme_type])


    # Function: get_ngrams_normalized_vector
    # -----------------------------
    # will modify the uni/bigrams_top/bottom/all counts with normalized versions of themselves
    def get_ngrams_normalized_vector (self, sentence):

        unigram_vector = defaultdict(lambda: 0.0)
        bigram_vector = defaultdict(lambda: 0.0)
        sentence = [word.lower() for word in sentence]
        unigrams = sentence
        bigrams = ngrams(sentence, 2)
        for unigram in unigrams:
            unigram_vector[unigram] += 1
        for bigram in bigrams:
            bigram_vector[bigram] += 1
            
        self.normalize_vector (unigram_vector)
        self.normalize_vector (bigram_vector)
        
        return (unigram_vector, bigram_vector)