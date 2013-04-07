"""
Server-side application for handling AJAX requests.
"""

import sys
import os
sys.path.append (os.path.abspath ('../process_data/'))
from SentimentAnalysis import SentimentAnalysis
import pickle
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """
    The index page.
    
    :return: The rendered index.html template.
    """
    return render_template("index.html")
    

@app.route("/add")
def add():
    """
    Adds two numbers together and returns the result, via AJAX.
    
    :return: Some JSON containing the resulting number.
    """
    # Retrieve the data from the request, defaulting to 0 if not given.
    a = request.args.get("a", 0, type=int)
    b = request.args.get("b", 0, type=int)
    
    # The resultant addition
    result = a + b
    
    return jsonify(result=result)

@app.route("/_classify_sentiment")
def classify_sentiment ():
    print "### classify_sentiment ###"
    return jsonify(result="hello, world!")

if __name__ == "__main__":

    sa = SentimentAnalysis ('../process_data/Trained_Classifier.obj')

    app.run()








