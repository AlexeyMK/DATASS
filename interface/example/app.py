"""
Server-side application for handling AJAX requests.
"""

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


if __name__ == "__main__":
    # Run the server
    app.run()
