# "Database code" for the DB Forum.

import datetime 
import psycopg2
import bleach

def get_posts():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("select content, time from posts order by time;")
    posts = [(bleach.clean(content), time) for content, time in c.fetchall()]
    db.close()
    return posts

def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("insert into posts values (%s, %s);" , (bleach.clean(content), datetime.datetime.now()))
    db.commit()
    db.close()