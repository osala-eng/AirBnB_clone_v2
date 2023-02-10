#!/usr/bin/python3
"""
Start a Flask application with routes
/, /hbnb, /c/<text>
"""

from flask import Flask, render_template
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


@app.route('/c/<text>')
def c_text(text):
    """display custom text given"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    '''Python route'''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def text_if_int(n):
    """display text only if int given"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def template_int(n):
    '''display a HTML page only if n is an integer'''
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>')
def odd_or_even(n):
    ''' display a HTML page only if n is an integer'''
    info = ''
    if n % 2 == 0:
        info = '{} is even'.format(n)
    else:
        info = '{} is odd'.format(n)
    return render_template('6-number_odd_or_even.html', info=info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
