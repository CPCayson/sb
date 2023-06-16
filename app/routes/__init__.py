from flask import Blueprint

# Define the blueprints
user_bp = Blueprint('user', __name__, url_prefix='/users')
document_bp = Blueprint('document', __name__, url_prefix='/documents')
subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscriptions')
school_bp = Blueprint('school', __name__, url_prefix='/schools')
comment_bp = Blueprint('comment', __name__, url_prefix='/comments')
bookmark_bp = Blueprint('bookmark', __name__, url_prefix='/bookmarks')
rank_bp = Blueprint('rank', __name__)
#auth_bp =  Blueprint('auth', __name__)
 

# Import the route files to register the routes
from app.routes import user, document, subscription, school, comment, bookmark, rank

# Register the blueprints
user_bp.register_blueprint(user.user_bp)
document_bp.register_blueprint(document.document_bp)
subscription_bp.register_blueprint(subscription.subscription_bp)
school_bp.register_blueprint(school.school_bp)
comment_bp.register_blueprint(comment.comment_bp)
bookmark_bp.register_blueprint(bookmark.bookmark_bp)
rank_bp.register_blueprint(rank.rank_bp)
#auth_bp.register_blueprint(auth.auth_bp)
