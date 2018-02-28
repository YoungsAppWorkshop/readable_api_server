from . import db


class Category(db.Model):
    """ A class which represents Category of Posts

    Attributes:
        name: string. Name of Category
        path: string. Path in URL. Primary key
    """
    __tablename__ = 'category'

    name = db.Column(db.String(32), nullable=False)
    path = db.Column(db.String(32), primary_key=True)

    def __repr__(self):
        """ Define string representations of the object """
        return "Category(name='{}', path='{}')".format(self.name, self.path)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'path': self.path
        }


class Post(db.Model):
    """  A class which represents a Post

    Attributes:
        author: string. Author name of the post
        body: string. Body of the post
        category_path: string. Category path of the post. Foreign Key
        comment_count: int. Number of comments for the post
        deleted: bool. Flag variable if the post is deleted
        id: string. UUID(v4). Primary key
        timestamp: datetime.datetime(). timestamp of the post created
        title: string. Title of the post
        vote_score: int. Vote score of the post
    """
    __tablename__ = 'post'

    author = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    category_path = db.Column(db.String(32), db.ForeignKey('category.path'))
    category = db.relationship(Category)
    comment_count = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, nullable=False)
    id = db.Column(db.String(36), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(), nullable=False)
    vote_score = db.Column(db.Integer)

    def __repr__(self):
        """ Define string representations of the object """
        return "Post(id='{}', title='{}')".format(self.id, self.title)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format
                - timestamp: convert Python datetime.datetime() object to
                    JavaScript Date.now() object (time in milliseconds)
        """
        return {
            'author': self.author,
            'body': self.body,
            'category': self.category_path,
            'commentCount': self.comment_count,
            'deleted': self.deleted,
            'id': self.id,
            'timestamp': int(self.timestamp.timestamp() * 1000),
            'title': self.title,
            'voteScore': self.vote_score
        }


class Comment(db.Model):
    """  A class which represents a Comment

    Attributes:
        author: string. Author name of the comment
        body: string. Body of the comment
        deleted: bool. Flag variable if the comment is deleted
        id: string. UUID(v4). Primary key
        parent_deleted: bool. Flag variable if the parent post is deleted
        parent_id: string. UUID(v4). ID of a Post. Foreign Key
        timestamp: datetime.datetime(). timestamp of the comment created
        vote_score: int. Vote score of the comment
    """
    __tablename__ = 'comment'

    author = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    deleted = db.Column(db.Boolean, nullable=False)
    id = db.Column(db.String(36), primary_key=True)
    parent_deleted = db.Column(db.Boolean, nullable=False)
    parent_id = db.Column(db.String(36), db.ForeignKey('post.id'))
    post = db.relationship(Post)
    timestamp = db.Column(db.DateTime, nullable=False)
    vote_score = db.Column(db.Integer)

    def __repr__(self):
        """ Define string representations of the object """
        return "Comment(id='{}', parent_id='{}')".format(self.id, self.parent_id)  # noqa

    @property
    def serialize(self):
        """ Return object data in easily serializeable format
                - timestamp: convert Python datetime.datetime() object to
                    JavaScript Date.now() object (time in milliseconds)
        """
        return {
            'author': self.author,
            'body': self.body,
            'deleted': self.deleted,
            'id': self.id,
            'parentDeleted': self.parent_deleted,
            'parentId': self.parent_id,
            'timestamp': int(self.timestamp.timestamp() * 1000),
            'voteScore': self.vote_score
        }
