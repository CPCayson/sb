
from flask import render_template, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

suggested_edit_bp = Blueprint('suggested_edit', __name__)



@suggested_edit_bp.route('/suggest_edit/<int:document_id>', methods=['POST'])
@login_required
def suggest_edit(document_id):
    form = SuggestEditForm()
    if form.validate_on_submit():
        suggested_edit = SuggestedEdit(
            document_id=document_id,
            user_id=current_user.id,
            suggested_title=form.title.data,
            suggested_subject=form.subject.data
        )
        db.session.add(suggested_edit)
        db.session.commit()
        flash('Your suggested edit has been submitted!')
    return redirect(url_for('document', document_id=document_id))


@suggested_edit_bp.route('/upvote_suggested_edit', methods=['POST'])
@login_required
def upvote_suggested_edit():
    form = UpvoteSuggestedEditForm()
    if form.validate_on_submit():
        suggested_edit = SuggestedEdit.query.get_or_404(form.suggested_edit_id.data)
        suggested_edit.upvotes += 1
        db.session.commit()
        flash('You have upvoted a suggested edit!', 'success')

    return redirect(url_for('document', document_id=suggested_edit.document_id))
