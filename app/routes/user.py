from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    documents = Document.query.filter_by(user_id=user.id).all()
    bookmarked_files = user.bookmarked_files
    def is_bookmarked(self, document):
        return document in self.bookmarked_files
    return render_template('user.html', user=user, documents=documents, bookmarked_files=bookmarked_files)
