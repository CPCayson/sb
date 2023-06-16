from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.user import user_bp
    from app.routes.document import document_bp
    from app.routes.subscription import subscription_bp
    from app.routes.school import school_bp
    from app.routes.comment import comment_bp
    from app.routes.rank import rank_bp
    from app.routes.suggested_edit import suggested_edit_bp
    from app.routes.bookmark import bookmark_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(school_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(rank_bp)
    app.register_blueprint(suggested_edit_bp)
    app.register_blueprint(bookmark_bp)

    return app

from app import models