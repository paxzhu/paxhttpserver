from flask import Flask, render_template, send_file, redirect
import os

app = Flask(__name__)

def preprocess(url_path):
    pass

def handle_directory(url_path):
    pass

def handle_file(url_path):
    pass

@app.route('/', defaults = {'url_path':''})
@app.route('/<path:url_path>')
def direct(url_path):
    """
    There may be a problem with user input, which will cause an exception, so preprocessing is required
    """
    preprocess(url_path) 

    """Now, url_path is the normal path"""
    if url_path.endswith('/'):
        return handle_directory(url_path)
    return handle_file(url_path)

if __name__ == "__main__":
    app.run(debug = True, port=9000)