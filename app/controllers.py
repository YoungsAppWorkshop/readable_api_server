from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

# Import the database object and models
from . import db
from .models import Category, Comment, Post


# Define the blueprint: 'api'
api = Blueprint('api', __name__)


@api.route('/categories', methods=['GET'])
def jsonify_all_categories():
    """ GET     /categories
            - Return all categories in JSON
    """
    try:
        categories = db.session.query(Category).order_by(Category.path)
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(categories=[category.serialize for category in categories])  # noqa


@api.route('/<category>/posts', methods=['GET'])
def jsonify_posts_for_category(category):
    """ GET     /:category/posts
            - Return all posts for a category in JSON
    """
    try:
        posts = db.session.query(Post)\
            .filter(Post.category_path == category)\
            .filter(Post.deleted.is_(False))\
            .order_by(Post.timestamp)
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


@api.route('/posts', methods=['GET', 'POST'])
def handle_requests_posts():
    """ Handle HTTP requests for API Endpoint: /posts """
    # GET   /posts      : Return all posts in JSON
    if request.method == 'GET':
        return jsonify_all_posts()
    # POST  /posts      : Add a new post and return it
    return add_post(request)


def jsonify_all_posts():
    """ GET     /posts
            - Return all posts in JSON
    """
    try:
        posts = db.session.query(Post)\
            .filter(Post.deleted.is_(False))\
            .order_by(Post.timestamp)
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([post.serialize for post in posts])


def add_post(request):
    """ POST    /posts
            - Add a new Post and return it in JSON
    """
    # Parse data from the request
    try:
        author = request.get_json()['author'].strip()
        body = request.get_json()['body'].strip()
        category_path = request.get_json()['category']
        id = request.get_json()['id']
        timestamp = int(request.get_json()['timestamp'])
        title = request.get_json()['title'].strip()
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
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Duplicate Post ID'}), 400
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(new_post.serialize)


@api.route('/posts/<post_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_requests_post(post_id):
    """ Handle HTTP requests for API Endpoint: /posts/:id """

    # GET       /posts/:id      : Return the post information in JSON
    if request.method == 'GET':
        return jsonify_post(post_id)
    # POST      /posts/:id      : Vote on the post
    if request.method == 'POST':
        return vote_post(post_id, request)
    # PUT       /posts/:id      : Edit the details of the post
    if request.method == 'PUT':
        return edit_post(post_id, request)
    # DELETE    /posts/:id      : Delete the post
    return delete_post(post_id)


def jsonify_post(post_id):
    """ GET     /posts/:id
            - Return the post information in JSON
    """
    try:
        post = db.session.query(Post)\
            .filter(Post.id == post_id)\
            .filter(Post.deleted.is_(False))\
            .one()
    except NoResultFound:
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(post.serialize)


def vote_post(post_id, request):
    """ POST    /posts/:id
            - Vote for/against a post and return it in JSON
    """
    # Parse data from the request
    try:
        option = request.get_json()['option']
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate option from the request
    if option != 'upVote' and option != 'downVote':
        return jsonify({'error': "'option' parameter can be either 'upVote' or 'downVote'"}), 400  # noqa

    # Vote for/against the post and store it in database
    try:
        post = db.session.query(Post)\
            .filter(Post.id == post_id)\
            .filter(Post.deleted.is_(False))\
            .one()
        if option == 'upVote':
            post.vote_score += 1
        else:
            post.vote_score -= 1
        db.session.add(post)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(post.serialize)


def edit_post(post_id, request):
    """ PUT     /posts/:id
            - Edit a post and return it in JSON
    """
    # Parse data from the request
    try:
        body = request.get_json()['body'].strip()
        title = request.get_json()['title'].strip()
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate data from the request
    if body == '' or title == '':
        return jsonify({'error': "Post title, body can't be a blank"}), 400

    # Edit the post and store it in database
    try:
        post = db.session.query(Post)\
            .filter(Post.id == post_id)\
            .filter(Post.deleted.is_(False))\
            .one()
        post.body = body
        post.title = title
        db.session.add(post)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(post.serialize)


def delete_post(post_id):
    """ DELETE  /posts/:id
            - Delete a Post and return it in JSON
    """
    try:
        # Set the deleted flag for the post to True
        post = db.session.query(Post)\
            .filter(Post.id == post_id)\
            .filter(Post.deleted.is_(False))\
            .one()
        post.deleted = True
        db.session.add(post)
        # Set the parent_deleted flag for all child comments to True
        comments = db.session.query(Comment)\
            .filter(Comment.parent_id == post_id)\
            .update({Comment.parent_deleted: True}, synchronize_session=False)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(post.serialize)


@api.route('/posts/<post_id>/comments', methods=['GET'])
def jsonify_comments_for_post(post_id):
    """ GET     /posts/:id/comments
            - Return all comments for a post in JSON
    """
    try:
        comments = db.session.query(Comment)\
            .filter(Comment.parent_id == post_id)\
            .filter(Comment.deleted.is_(False))\
            .filter(Comment.parent_deleted.is_(False))\
            .order_by(Comment.timestamp)
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify([comment.serialize for comment in comments])


@api.route('/comments', methods=['POST'])
def add_comment():
    """ POST    /comments
            - Add a comment to a post and return it in JSON
    """
    # Parse data from the request
    try:
        author = request.get_json()['author'].strip()
        body = request.get_json()['body'].strip()
        id = request.get_json()['id']
        parent_id = request.get_json()['parentId']
        timestamp = int(request.get_json()['timestamp'])
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate data from the request
    if author == '' or body == '':
        return jsonify({'error': "Comment body and author can't be a blank"}), 400  # noqa

    # Validate if the parent post exists
    try:
        post = db.session.query(Post).filter(Post.id == parent_id).one()
    except NoResultFound:
        return jsonify({'error': 'No Parent Post Found'}), 403
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500

    # Validate if the parent post is deleted
    if post.deleted:
        return jsonify({'error': 'Parent Post Deleted'}), 403

    # Create a new comment and store it in Database
    try:
        new_comment = Comment(author=author, body=body, deleted=False, id=id,
                              parent_deleted=False, parent_id=parent_id,
                              timestamp=timestamp, vote_score=0)
        db.session.add(new_comment)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Duplicate Comment ID'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(new_comment.serialize)


@api.route('/comments/<comment_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_requests_comment(comment_id):
    """ Handle HTTP requests for API Endpoint: /comments/:id """

    # GET       /comments/:id       : Return the comment information in JSON
    if request.method == 'GET':
        return jsonify_comment(comment_id)
    # POST      /comments/:id       : Vote on the comment
    if request.method == 'POST':
        return vote_comment(comment_id, request)
    # PUT       /comments/:id       : Edit the details of the comment
    if request.method == 'PUT':
        return edit_comment(comment_id, request)
    # DELETE    /comments/:id       : Delete the comment
    return delete_comment(comment_id)


def jsonify_comment(comment_id):
    """ GET     /comments/:id
            - Return the comment information in JSON
    """
    try:
        comment = db.session.query(Comment)\
            .filter(Comment.id == comment_id)\
            .filter(Comment.deleted.is_(False))\
            .filter(Comment.parent_deleted.is_(False))\
            .one()
    except NoResultFound:
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(comment.serialize)


def vote_comment(comment_id, request):
    """ POST    /comments/:id
            - Vote for/against a comment and return it in JSON
    """
    # Parse data from the request
    try:
        option = request.get_json()['option']
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate option from the request
    if option != 'upVote' and option != 'downVote':
        return jsonify({'error': "'option' parameter can be either 'upVote' or 'downVote'"}), 400  # noqa

    # Vote for/against the comment and store it in database
    try:
        comment = db.session.query(Comment)\
            .filter(Comment.id == comment_id)\
            .filter(Comment.deleted.is_(False))\
            .filter(Comment.parent_deleted.is_(False))\
            .one()
        if option == 'upVote':
            comment.vote_score += 1
        else:
            comment.vote_score -= 1
        db.session.add(comment)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(comment.serialize)


def edit_comment(comment_id, request):
    """ PUT     /comments/:id
            - Edit a comment and return it in JSON
    """
    # Parse data from the request
    try:
        body = request.get_json()['body'].strip()
    except Exception:
        return jsonify({'error': 'Bad Request'}), 400

    # Validate data from the request
    if body == '':
        return jsonify({'error': "Comment body can't be a blank"}), 400

    # Edit the comment and store it in database
    try:
        comment = db.session.query(Comment)\
            .filter(Comment.id == comment_id)\
            .filter(Comment.deleted.is_(False))\
            .filter(Comment.parent_deleted.is_(False))\
            .one()
        comment.body = body
        db.session.add(comment)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(comment.serialize)


def delete_comment(comment_id):
    """ DELETE  /comments/:id
            - Delete a comment and return it in JSON
    """
    try:
        # Set the deleted flag for the comment to True
        comment = db.session.query(Comment)\
            .filter(Comment.id == comment_id)\
            .filter(Comment.deleted.is_(False))\
            .filter(Comment.parent_deleted.is_(False))\
            .one()
        comment.deleted = True
        db.session.add(comment)
        db.session.commit()
    except NoResultFound:
        db.session.rollback()
        return jsonify({'error': 'No Result Found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify(comment.serialize)


# Helper Functions
def is_valid_category(category_path):
    """ Check if a category_path is valid"""
    try:
        category = db.session.query(Category).filter_by(path=category_path).one()  # noqa
    except Exception:
        return False
    else:
        return True
