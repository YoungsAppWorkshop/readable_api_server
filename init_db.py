#!/usr/bin/env python3

"""
    Python script to create database schema and add dummy data
"""
import datetime
from app import app, db
from app.models import Category, Comment, Post

# Create Database tables
db.create_all()

# Add Category data
category1 = Category(name="react", path="react")
db.session.add(category1)
db.session.commit()

category2 = Category(name="redux", path="redux")
db.session.add(category2)
db.session.commit()

category3 = Category(name="udacity", path="udacity")
db.session.add(category3)
db.session.commit()

# Add Post data
post1 = Post(id='0d154a66-2b39-4276-9e77-5651f6a17444',
             timestamp=datetime.datetime.fromtimestamp(1467166872634 / 1000.0),
             title='Udacity is the best place to learn React',
             body='Everyone says so after all.',
             author='thingtwo',
             category_path='react',
             vote_score=6,
             deleted=False,
             comment_count=2)
db.session.add(post1)
db.session.commit()

post2 = Post(id='2008fab6-78a4-4242-bad2-71249814ae84',
             timestamp=datetime.datetime.fromtimestamp(1468479767190 / 1000.0),
             title='Learn Redux in 10 minutes!',
             body='Just kidding. It takes more than 10 minutes to learn technology.',  # noqa
             author='thingone',
             category_path='redux',
             vote_score=-5,
             deleted=False,
             comment_count=0)
db.session.add(post2)
db.session.commit()

post3 = Post(id='ac54c88d-121a-48db-88e5-b0a68f053a71',
             timestamp=datetime.datetime.fromtimestamp(1513320276285 / 1000.0),
             title='Testing Adding Posts !',
             body='Testing is important.',
             author='thingone',
             category_path='react',
             vote_score=4,
             deleted=False,
             comment_count=0)
db.session.add(post3)
db.session.commit()

# Add Comment data
comment1 = Comment(id='322b4b0c-0bd5-4ea9-9342-c735ceae3326',
                   parent_id='0d154a66-2b39-4276-9e77-5651f6a17444',
                   timestamp=datetime.datetime.fromtimestamp(1468166872634 / 1000.0),  # noqa
                   body='Hi there! I am a COMMENT.',
                   author='thingtwo',
                   vote_score=6,
                   deleted=False,
                   parent_deleted=False)
db.session.add(comment1)
db.session.commit()

comment2 = Comment(id='465e554e-8ba3-48f1-8346-4511e3502bd0',
                   parent_id='0d154a66-2b39-4276-9e77-5651f6a17444',
                   timestamp=datetime.datetime.fromtimestamp(1469479767190 / 1000.0),  # noqa
                   body='Comments. Are. Cool.',
                   author='thingone',
                   vote_score=-2,
                   deleted=False,
                   parent_deleted=False)
db.session.add(comment2)
db.session.commit()
