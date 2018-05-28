#!/usr/bin/env python3

import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'
db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<Course(title={})>'.format(self.title)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Course(name={})>'.format(self.name)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    articles=File.query.all()
    return render_template('index.html', articles=articles)

@app.route('/files/<int:file_id>')
def file(file_id):
    article = File.query.get_or_404(file_id)
    return render_template('file.html', article=article)
