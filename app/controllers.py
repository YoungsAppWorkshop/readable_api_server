from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound

# Import the database object and models
from . import db
from .models import Category, Comment, Post


# Define the blueprint: 'api'
api = Blueprint('api', __name__)


# For API Endpoint:     /categories
@api.route('/categories/', methods=['GET'])
def jsonify_all_categories():
    """ Return all categories in JSON on GET request """
    try:
        categories = db.session.query(Category).order_by(Category.path)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(categories=[category.serialize for category in categories])  # noqa


# For API Endpoint:     /:category/posts
@api.route('/<category>/posts/', methods=['GET'])
def jsonify_posts_for_category(category):
    """ Return all posts for a category in JSON on GET request """
    try:
        posts = db.session.query(Post).filter(Post.category_path == category)\
            .order_by(Post.timestamp)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


# For API Endpoint:     /posts
def jsonify_all_posts():
    """ Return all posts in JSON on GET request"""
    try:
        posts = db.session.query(Post).order_by(Post.timestamp)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


def add_post(request):
    """ Add a new Post and return it on POST request"""
    # Parse data from the request
    try:
        author = request.form['author'].strip()
        body = request.form['body'].strip()
        category_path = request.form['category']
        id = request.form['id']
        timestamp = int(request.form['timestamp'])
        title = request.form['title'].strip()
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate data from the request
    if author == '' or body == '' or title == '':
        return jsonify({'error': "Post title, body and author can't be a blank"}), 400  # noqa

    if not is_valid_category(category_path):
        return jsonify({'error': 'Wrong Category'}), 400

    # Create a new post and store it in Database
    try:
        new_post = Post(author=author, body=body, category_path=category_path,
                        comment_count=0, deleted=False, id=id,
                        timestamp=timestamp, title=title, vote_score=0)
        db.session.add(new_post)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(new_post.serialize)


@api.route('/posts/', methods=['GET', 'POST'])
def handle_requests_posts():
    """ Handle HTTP requests for API Endpoint: /posts """
    # POST /posts       : Add a new post and return it
    if request.method == 'POST':
        return add_post(request)
    # GET /posts        : Return all posts in JSON
    return jsonify_all_posts()


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


# Helper Functions
def is_valid_category(category_path):
    """ Check if a category_path is valid"""

    try:
        category = db.session.query(Category).filter_by(
            path=category_path).one()
        return True
    except Exception:
        return False
