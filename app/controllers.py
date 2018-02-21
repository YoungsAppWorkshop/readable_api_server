#!/usr/bin/env python3
from flask import Blueprint, jsonify, abort

# Import the database object from the main app module
from . import db
from .models import Category, Comment, Post


# Define the blueprint: 'api', set its url prefix: app.url/api
api = Blueprint('api', __name__)


# Routes for JSON endpoints
@api.route('/categories/')
def jsonify_all_categories():
    """Return all categories information in JSON"""
    try:
        categories = db.session.query(Category).order_by(Category.path)
        return jsonify(categories=[category.serialize for category in categories])  # noqa
    except Exception as e:
        abort(500)


@api.route('/posts/')
def jsonify_all_posts():
    """Return all posts information in JSON"""
    try:
        posts = db.session.query(Post).order_by(Post.timestamp)
        return jsonify(posts=[post.serialize for post in posts])  # noqa
    except Exception as e:
        abort(500)


@api.route('/comments/')
def jsonify_all_comments():
    """Return all comments information in JSON"""
    try:
        comments = db.session.query(Comment).order_by(Comment.timestamp)
        return jsonify(comments=[comment.serialize for comment in comments])  # noqa
    except Exception as e:
        abort(500)
