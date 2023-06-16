from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

school_bp = Blueprint('school', __name__)


@school_bp.route('/school/<int:school_id>')
def school(school_id):
    school = School.query.get_or_404(school_id)
    documents = Document.query.filter_by(school_id=school.id).all()
    return render_template('school.html', school=school, documents=documents)
