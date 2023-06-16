from flask import render_template, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/<int:subscription_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def subscription(subscription_id):
    return ''

@subscription_bp.route('/user/<int:user_id>', methods=['GET'])
def subscriptions_for_user(user_id):
    return ''
