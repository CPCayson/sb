from flask import render_template, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

rank_bp = Blueprint('like', __name__)


@rank_bp.route('/like/<int:document_id>', methods=['POST'])
@login_required
def like_document(document_id):
    document = Document.query.get_or_404(document_id)
    like = Like.query.filter_by(document_id=document.id, user_id=current_user.id).first()
    if like:
        flash('You have already upvoted this document.', 'error')
        return redirect(url_for('document', document_id=document_id))
    like = Like(document_id=document.id, user_id=current_user.id)
    db.session.add(like)
    document.ranking += 1
    db.session.commit()
    flash('You have liked this document.')
    return redirect(url_for('document', document_id=document_id))


@rank_bp.route('/dislike/<int:document_id>', methods=['POST'])
@login_required
def dislike_document(document_id):
    document = Document.query.get_or_404(document_id)
    dislike = Dislike(user_id=current_user.id, document_id=document_id)
    db.session.add(dislike)
    document.ranking -= 1
    db.session.commit()
    flash('You have disliked this document.')
    return redirect(url_for('document', document_id=document_id))


@rank_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return jsonify(upvotes=comment.upvotes)

@rank_bp.route('/comments/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.downvotes += 1
    db.session.commit()
    return jsonify(downvotes=comment.downvotes)