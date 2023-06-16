# auth.py

from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()

@login_manager.user_loader
def get_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
