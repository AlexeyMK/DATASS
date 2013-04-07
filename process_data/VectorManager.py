#vector manager class
import math

class VectorManager:

    def __init__ (self):
        pass

    # Function: normalize_vector
    # ------------------------------------
    # takes in a dict with real # keys, normalizes it
    def normalize_vector (self, vector):
        squared_total = 0.0
        for key, value in vector.iteritems():
            squared_total += value*value
    
        squared_total = math.sqrt(squared_total)
        for key,value in sentiment_vector.iteritems():
            vector[key] = value / squared_total


    # Function: cosine_similarity
    # ---------------------------
    # takes in two dicts with real # keys, normalized, finds their cosine similarity.
    def cosine_similarity (self, v1, v2):
        sum = 0.0
        for key, value in sentence_vector.iteritems ():
            sum += sentence_vector[key] * meme_type_vector[key]
        return sum
