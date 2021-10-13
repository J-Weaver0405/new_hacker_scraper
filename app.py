# app.py
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import sqlite3

load_dotenv()
app = Flask(__name__)
"""
API Specification: 

# generate your API specs here

"""
DB = os.getenv('DB')

@app.get('/')
def index():
    msg = """
    <h2>Welcome to the home page!</h2> </br>
    
    Navigate to <strong>/headlines</strong> to see headlines  </br>
    
    or <strong> /authors </strong> to see authors </br>

    <h4> Some more queries </h4>
    
    i.e. </br>
    
    /headlines/<date> (date can be 2021, 2021-10-12.. etc) </br>
    
    /authors/<first_initials> (first_initials can be a-z) </br>
    """
    return msg

@app.get('/headlines')
@app.get("/headlines/<date>")
def get_headlines(date=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if date:
        headlines = c.execute(
            "select title from hacker_news_posts where timestamp like '%' || ? || '%'", (date,)).fetchall()
    else:
        headlines = c.execute("select title from hacker_news_posts").fetchall()

    if len(headlines) > 0:
        return jsonify(headlines)
    return "no headlines found", 415


@app.get('/authors')
@app.get("/authors/<first_letters>")
def get_authors(first_letters=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if first_letters:
        authors = c.execute(
            "select author from hacker_news_posts where author like '%' || ? || '%'", (first_letters,)).fetchall()
    else:
        authors = c.execute("select author from hacker_news_posts").fetchall()

    if len(authors) > 0:
        return jsonify(authors)
    return "no authors found", 415


@app.get('/posts')
@app.get('/posts/<score>')
def get_posts(score=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if score:
        posts = c.execute(
            "select * from hacker_news_posts where cast(score as INTEGER) >= ?", (score, )).fetchall()
    else:
        posts = c.execute("select * from hacker_news_posts").fetchall()
    if len(posts) > 0:
        return jsonify(posts)
    return "no posts found", 415


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
