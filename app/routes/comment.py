from flask import render_template, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

comment_bp = Blueprint('comment', __name__)



@comment_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return jsonify(upvotes=comment.upvotes)

@comment_bp.route('/comments/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.downvotes += 1
    db.session.commit()
    return jsonify(downvotes=comment.downvotes)


@comment_bp.route('/comment/<int:file_id>', methods=['POST'])
@login_required
def comment_file(file_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, document_id=file_id)
        db.session.add(comment)
        db.session.commit()
        return render_template('comment.html', comment=comment)
    return redirect(url_for('file', file_id=file_id))
    
@comment_bp.route('/comments/document/<int:document_id>', methods=['GET'])
def get_comments(document_id):
    document = Document.query.get_or_404(document_id)
    comments = Comment.query.filter_by(document_id=document_id).all()
    return render_template('comments.html', document=document, comments=comments)
