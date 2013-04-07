# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
sys.path.append (os.path.abspath ('../process_data/'))
from SentimentAnalysis import SentimentAnalysis
import pickle
import itertools
import json
from operator import itemgetter
from flask import Flask, request, render_template, jsonify

image_locations = {

    'Annoying Facebook Girl': 'http://i.imgflip.com/1bhi.jpg',
    'First World Problems': 'http://i.imgflip.com/1bhf.jpg',
    'Forever Alone': 'http://i.imgflip.com/1bh4.jpg',
    'Foul Bachelor Frog': 'http://i.imgflip.com/1bgv.jpg',
    'Futurama Fry': 'http://i.imgflip.com/1bgw.jpg',
    'Good Guy Greg': 'http://i.imgflip.com/1bgx.jpg',
    'Insanity Wolf': 'http://i.imgflip.com/1bgu.jpg',
    'Paranoid Parrot': 'http://i.imgflip.com/1bi4.jpg',
    'Philosoraptor': 'http://i.imgflip.com/1bgs.jpg',
    'Scumbag Steve': 'http://i.imgflip.com/1bgy.jpg',
    'Socially Awkward Penguin': 'http://i.imgflip.com/1bh0.jpg',
    'Success Kid': 'http://i.imgflip.com/1bhk.jpg',
    'The Most Interesting Man In The World': 'http://i.imgflip.com/1bh8.jpg',
    'Socially Awesome Penguin': 'http://i.imgflip.com/1bgz.jpg'
    
}

sa = SentimentAnalysis ('../process_data/Trained_Classifier.obj')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_clean.html')


@app.route("/_classify_sentiment")
def classify_sentiment ():
    sentence = request.args.get('a', 0, type=str)
    
    prob_dist = sa.maxent_classify_raw (sentence)
    
    probabilities = {}
    for type in prob_dist.samples ():
        probabilities[type] = prob_dist.prob(type)
    
    rankings = []
    for key, value in probabilities.iteritems ():
        rankings.append ((key, value))
    sorted_rankings = sorted(rankings, key=itemgetter(1), reverse=True)

    r = [s[0] + (" - %f" % s[1]) for s in sorted_rankings]
    urls = [[s[0], image_locations[s[0]]] for s in sorted_rankings]

    packed_rankings = json.dumps (urls)

    return jsonify(result=packed_rankings)

if __name__ == '__main__':

    app.debug = True
    app.run()
