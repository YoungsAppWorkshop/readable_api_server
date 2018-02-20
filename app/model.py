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
        return "<Category (name='%s', path='%s')>" % (self.name, self.path)

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
        id: string. UUID(v4). Primary key
        timestamp: int. timestamp of the post created
        title: string. Title of the post
        body: string. Body of the post
        author: string. Author name of the post
        category: string. Category path of the post. Foreign Key
        vote_score: int. Vote score of the post
        deleted: bool. Flag variable if the post is deleted
        comment_count: int. Number of comments for the post
    """
    __tablename__ = 'post'

    id = db.Column(db.String(36), primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    category_path = db.Column(db.String(32), db.ForeignKey('category.path'))
    category = db.relationship(Category)
    vote_score = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, nullable=False)
    comment_count = db.Column(db.Integer)

    def __repr__(self):
        """ Define string representations of the object """
        return "<Post (id='%s', title='%s')>" % (self.id, self.title)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'title': self.title,
            'body': self.body,
            'author': self.author,
            'category': self.category_path,
            'voteScore': self.vote_score,
            'deleted': self.deleted,
            'commentCount': self.comment_count
        }


class Comment(db.Model):
    """  A class which represents a Comment

    Attributes:
        id: string. UUID(v4). Primary key
        parent_id: string. UUID(v4). ID of a Post. Foreign Key
        timestamp: int. timestamp of the comment created
        body: string. Body of the comment
        author: string. Author name of the comment
        vote_score: int. Vote score of the comment
        deleted: bool. Flag variable if the comment is deleted
        parent_deleted: bool. Flag variable if the parent post is deleted
    """
    __tablename__ = 'comment'

    id = db.Column(db.String(36), primary_key=True)
    parent_id = db.Column(db.String(36), db.ForeignKey('post.id'))
    post = db.relationship(Post)
    timestamp = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    vote_score = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, nullable=False)
    parent_deleted = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """ Define string representations of the object """
        return "<Comment (id='%s', author='%s')>" % (self.id, self.author)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'parentId': self.parent_id,
            'timestamp': self.timestamp,
            'body': self.body,
            'author': self.author,
            'voteScore': self.vote_score,
            'deleted': self.deleted,
            'parentDeleted': self.parent_deleted
        }
