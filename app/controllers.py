from flask import Blueprint, jsonify, abort
from sqlalchemy.orm.exc import NoResultFound

# Import the database object and models
from . import db
from .models import Category, Comment, Post


# Define the blueprint: 'api'
api = Blueprint('api', __name__)


# Routes for JSON endpoints
@api.route('/categories/', methods=['GET'])
def jsonify_all_categories():
    """ Return all categories information in JSON """
    try:
        categories = db.session.query(Category).order_by(Category.path)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(categories=[category.serialize for category in categories])  # noqa


@api.route('/<category>/posts/', methods=['GET'])
def jsonify_posts_for_category(category):
    """ Return all posts information for a category in JSON """
    try:
        posts = db.session.query(Post).filter(Post.category_path == category)\
            .order_by(Post.timestamp)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


@api.route('/posts/', methods=['GET'])
def jsonify_all_posts():
    """ Return all posts information in JSON """
    try:
        posts = db.session.query(Post).order_by(Post.timestamp)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


@api.route('/posts/<post_id>', methods=['GET'])
def jsonify_post(post_id):
    """ Return a post information in JSON """
    try:
        post = db.session.query(Post).filter(Post.id == post_id).one()
    except NoResultFound as e:
        return jsonify({'error': 'No Result Found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(post.serialize)


@api.route('/posts/<post_id>/comments/', methods=['GET'])
def jsonify_comments_for_post(post_id):
    """ Return all comments for a post in JSON """
    try:
        comments = db.session.query(Comment)\
            .filter(Comment.parent_id == post_id).order_by(Comment.timestamp)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([comment.serialize for comment in comments])
