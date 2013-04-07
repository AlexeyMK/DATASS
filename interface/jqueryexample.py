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
from flask import Flask, jsonify, render_template, request

import pickle
app = Flask(__name__)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_classify_text')
def classify_text ():
    sentence = request.args.get('sentence', 0, type=str)
    print sentence
    pass
    
    


if __name__ == '__main__':
    f = open ('../process_data/Trained_Classifier.obj', 'r')
    classifier = pickle.load(f)
    
    
    app.run()
