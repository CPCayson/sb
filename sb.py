from app import create_app, db
from app.models import User, Subscription, Document, School, Comment, Like, Dislike, SuggestedEdit
from flask.cli import with_appcontext
from flask_migrate import upgrade, init, migrate, stamp
import sys
import click
app = create_app()
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Comment': Comment,
        'Document': Document,
        'Like': Like,
        'Dislike': Dislike,
        'SuggestedEdit': SuggestedEdit
    }
    
def seed_database():
    # Create sample users
    
    # Create sample users
    user1 = User.query.filter_by(username='user1').first()
    if user1 is None:
        user1 = User(username='user1', email='user1ple.com')
        user1.set_password('password1')
    else:
        # Modify existing user with a unique username
        user1.email = 'new-email@exle.com'
        # Modify other user attributes as needed

    # Repeat the same approach for user2
    user2 = User.query.filter_by(username='user2').first()
    if user2 is None:
        user2 = User(username='user2', email='user2@example.com')
        user2.set_password('password2')
    else:
        # Modify existing user with a unique username
        user2.email = 'new-email@.com'
        # Modify other user attributes as neede
        
    # Create sample subscriptions
    subscription1 = Subscription(user=user1)
    subscription2 = Subscription(user=user2)

    # Create sample schools
    school1 = School(name='School 1')
    school2 = School(name='School 2')

    # Create sample documents
    document1 = Document(filename= r'C:\Users\cpcay\Downloads\C_Cayson_Resume_June.pdf', user=user1, school=school1, professor='Ally', subject='Botany')
    document2 = Document(filename=r'C:\Users\cpcay\Downloads\C_Cayson_Resume_June.pdf', user=user2, school=school2, professor='Ball', subject='Anatomy')

    # Create sample comments
    comment1 = Comment(content='Great document!', user=user1, document=document1)
    comment2 = Comment(content='Nice work!', user=user2, document=document2)

    # Create sample likes
    like1 = Like(user=user1, document=document1)
    like2 = Like(user=user2, document=document2)

    # Create sample dislikes
    dislike1 = Dislike(user=user1, document=document1)
    dislike2 = Dislike(user=user2, document=document2)

    # Create sample suggested edits
    suggested_edit1 = SuggestedEdit(user=user1, document=document1, suggested_title='New Title')
    suggested_edit2 = SuggestedEdit(user=user2, document=document2, suggested_title='Updated Title')

    # Add the objects to the session and commit the changes
    db.session.add_all([user1, user2, subscription1, subscription2, school1, school2,
                        document1, document2, comment1, comment2, like1, like2,
                        dislike1, dislike2, suggested_edit1, suggested_edit2])
    db.session.commit()

# Define custom migration commands
@app.cli.command("db_upgrade")
@with_appcontext
def db_upgrade():
    upgrade()

@app.cli.command("db_init")
@with_appcontext
def db_init():
    init()

@app.cli.command("db_migrate")
@with_appcontext
def db_migrate_():
    migrate()

@app.cli.command("db_stamp")
@with_appcontext
def db_stamp_():
    stamp()

@app.cli.command("create_user")
@click.option("--username", prompt=True)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def create_user_command(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print("User created successfully!")
if __name__ == '__main__':
    with app.app_context():  # Add this line to run the code within the application context
        seed_database()
    app.run()

