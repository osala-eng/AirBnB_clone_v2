#!/usr/bin/python3
"""
Starts a flask web application
on 0.0.0.0:5000
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """display text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display text"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
