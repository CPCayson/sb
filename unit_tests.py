

import unittest
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from app.models import User, Document, Subscription, Comment, Like, Dislike, SuggestedEdit,  bookmarks, db

basedir = os.path.abspath(os.path.dirname(__file__))

# Create a Flask application for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db' # Use an in-memory SQLite database for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)


class RouteModelRelationshipTestCase(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(username='john', email='john@example.com')
        self.document = Document(filename='example.pdf')
        self.subscription = Subscription()
        self.comment = Comment(content='Great document!')
        self.like = Like()
        self.dislike = Dislike()
        self.suggested_edit = SuggestedEdit(suggested_title='New Title')
        db.session.add_all([self.user, self.document, self.subscription, self.comment, self.like,
                            self.dislike, self.suggested_edit])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_document_relationship(self):
        self.user.documents.append(self.document)
        db.session.commit()
        self.assertEqual(self.user.documents.first(), self.document)
        self.assertEqual(self.document.user, self.user)

    def test_user_subscription_relationship(self):
        self.user.subscriptions.append(self.subscription)
        db.session.commit()
        self.assertEqual(self.user.subscriptions.first(), self.subscription)
        self.assertEqual(self.subscription.user, self.user)


    def test_document_school_relationship(self):
        with app.app_context():
            school = School(name='University')
            document = Document(filename='example.pdf', school=school)
            db.session.add(school)
            db.session.add(document)
            db.session.commit()

            self.assertEqual(document.school, school)
            self.assertIn(document, school.documents) 

    def test_document_comment_relationship(self):
        with app.app_context():
            document = Document(filename='example.pdf')
            comment = Comment(content='Great document!', document=document)
            db.session.add(document)
            db.session.add(comment)
            db.session.commit()

            self.assertEqual(document.comments.first(), comment)
            self.assertEqual(comment.document, document)

    def test_document_like_relationship(self):
        with app.app_context():
            document = Document(filename='example.pdf')
            like = Like(document=document)
            db.session.add(document)
            db.session.add(like)
            db.session.commit()

            self.assertEqual(document.likes.first(), like)
            self.assertEqual(like.document, document)

    def test_document_dislike_relationship(self):
        with app.app_context():
            document = Document(filename='example.pdf')
            dislike = Dislike(document=document)
            db.session.add(document)
            db.session.add(dislike)
            db.session.commit()

            self.assertEqual(document.dislikes.first(), dislike)
            self.assertEqual(dislike.document, document)

    def test_document_suggested_edit_relationship(self):
        with app.app_context():
            document = Document(filename='example.pdf')
            suggested_edit = SuggestedEdit(document=document, suggested_title='New Title')
            db.session.add(document)
            db.session.add(suggested_edit)
            db.session.commit()

            self.assertEqual(document.suggested_edits.first(), suggested_edit)
            self.assertEqual(suggested_edit.document, document)


if __name__ == '__main__':
  unittest.main()
