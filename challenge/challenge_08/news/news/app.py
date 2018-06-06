#!/usr/bin/env python3

import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'
db = SQLAlchemy(app)
mongo = MongoClient('localhost', 27017).shiyanlou

class File(db.Model):
    __tablename__ = 'files'
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

    def add_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id' : self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags: 
                tags.append(tag_name)
            mongo.files.update({'file_id' : self.id}, {'$set':{'tags' : tags}})
        else:
            tags = [tag_name]
            mongo.files.insert({'file_id' : self.id, 'tags' : tags})
        return tags

    def remove_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id' : self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name in tags:
                tags.remove[tag_name]
            mongo.files.update({'file_id' : self.id}, {'$set':{'tags' : tags}})
            return tags
        else:
            return []


    @property
    def tags(self):
        file_item = mongo.files.find_one({'file_id' : self.id})
        if file_item:
            tags = file_item['tags']
            return tags
        else:
            return []

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

def insert():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is Cool')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - python is Cool')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

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
