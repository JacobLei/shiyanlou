#!/usr/bin/env python3

import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    articles = []
    os.chdir('../files')
    files = os.listdir(os.getcwd())
    for f in files:
        with open(f) as file:
            articles.append(json.loads(file.read()))
    return render_template('index.html', articles=articles)

@app.route('/files/<filename>')
def file(filename):
    filename = filename + '.json'
    os.chdir('../files')
    files = os.listdir(os.getcwd())
    if filename in files:
        with open(filename) as file:
            return render_template('file.html', article=json.loads(file.read()))
    else:
        abort(404)
