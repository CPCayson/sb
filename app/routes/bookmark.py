from flask import render_template, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

bookmark_bp = Blueprint('bookmark', __name__)

@bookmark_bp.route('/bookmark_file/<int:file_id>', methods=['POST'])
@login_required
def bookmark_file(file_id):
    file = Document.query.get(file_id)
    if file is None:
        flash('File not found.')
        return redirect(url_for('index'))
    if file in current_user.bookmarked_files:
        flash('You have already bookmarked this file.')
        return redirect(url_for('index'))
    current_user.bookmarked_files.append(file)
    db.session.commit()
    flash('You have bookmarked this file.')
    return redirect(url_for('index'))


@bookmark_bp.route('/unbookmark/<int:file_id>', methods=['POST'])
@login_required
def unbookmark_file(file_id):
    file = Document.query.get(file_id)
    if file is None:
        flash('File not found.')
        return redirect(url_for('index'))
    if file not in current_user.bookmarked_files:
        flash('You have not bookmarked this file.')
        return redirect(url_for('index'))
    current_user.bookmarked_files.remove(file)
    db.session.commit()
    flash('You have unbookmarked this file.')
    return redirect(url_for('index'))