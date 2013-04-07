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
from flask import Flask, request, render_template, jsonify

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

    topfour_tuples = itertools.islice(probabilities.iteritems(), 4)
    topfour = [m[0] + ("%f - " % m[1]) for m in topfour_tuples]

    topfour_send = json.dumps (topfour)
    return jsonify(result=topfour_send)

if __name__ == '__main__':

    app.debug = True
    app.run()
