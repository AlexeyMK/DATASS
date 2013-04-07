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


image_locations = {}


sa = SentimentAnalysis ('../process_data/Trained_Classifier.obj')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


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

    packed_rankings = json.dumps (r)

    return jsonify(result=packed_rankings)

if __name__ == '__main__':

    app.debug = True
    app.run()
