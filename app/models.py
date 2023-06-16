from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db, login_manager





# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    bookmarked_files = db.relationship('Document', secondary='bookmarks',
                                       backref=db.backref('bookmarked_by', lazy='dynamic'))
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
# Subscription model
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Add other subscription fields


# Document model
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    thumbnail = db.Column(db.String(256))
    textbook = db.Column(db.String(256))
    subject = db.Column(db.String(256))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))  # change this line
    professor = db.Column(db.String(256))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref=db.backref('document_comments', lazy=True, cascade='all, delete'))
    likes = db.relationship('Like', backref='document', lazy='dynamic')
    dislikes = db.relationship('Dislike', backref='document', lazy='dynamic')
    suggested_edits = db.relationship('SuggestedEdit', backref='document', lazy='dynamic')
    school = db.relationship('School', backref='documents', lazy=True)  # add this line

# School model
class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    # Add other school fields


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    document = db.relationship('Document', backref=db.backref('related_comments', lazy=True, cascade='all, delete'))
# Like model
class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))

    user = db.relationship('User', backref='likes')

class Dislike(db.Model):
    __tablename__ = 'dislikes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))

    user = db.relationship('User', backref='dislikes')

class SuggestedEdit(db.Model):
    __tablename__ = 'suggested_edits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    suggested_title = db.Column(db.String(256))
    suggested_subject = db.Column(db.String(256))
    upvotes = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='suggested_edits')
# Bookmark association table
bookmarks = db.Table('bookmarks',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                     db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True))
