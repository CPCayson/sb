
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.models import User, Document, School, Comment, Dislike, Like
from app.forms import LoginForm, RegistrationForm, UploadForm
from werkzeug.urls import url_parse
from PIL import Image
from werkzeug.utils import secure_filename
import os
import PyPDF2
from pdf2image import convert_from_path
import fitz  # this is pymupdf
from datetime import datetime



ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/test')
def tester():
    documents = Document.query.all()
    return render_template('test.html', title='test', documents=documents)

@app.route('/comment')
def commentss():
    document = Document.query.first()  # Replace with your logic to retrieve the document
    return render_template('comment.html', document=document)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    documents = Document.query.all()
    return render_template('index.html', title='Home', documents=documents)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    documents = Document.query.filter_by(user_id=user.id).all()
    bookmarked_files = user.bookmarked_files
    def is_bookmarked(self, document):
        return document in self.bookmarked_files
    return render_template('user.html', user=user, documents=documents, bookmarked_files=bookmarked_files)


@app.route('/school/<int:school_id>')
def school(school_id):
    school = School.query.get_or_404(school_id)
    documents = Document.query.filter_by(school_id=school.id).all()
    return render_template('school.html', school=school, documents=documents)


@app.route('/bookmark_file/<int:file_id>', methods=['POST'])
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


@app.route('/unbookmark/<int:file_id>', methods=['POST'])
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


@app.route('/document/<int:document_id>', methods=['GET', 'POST'])
def document(document_id):
    document = Document.query.get_or_404(document_id)
    suggested_edits = SuggestedEdit.query.filter_by(document_id=document_id).order_by(SuggestedEdit.upvotes.desc()).all()
    if suggested_edits and suggested_edits[0].upvotes > document.upvotes:
        document.title = suggested_edits[0].suggested_title
        document.subject = suggested_edits[0].suggested_subject
        db.session.commit()
    return render_template('document.html', title=document.title, document=document)


@app.route('/files/<filename>')
def uploaded_file(filename):
    file = UploadedFile.query.filter_by(filename=filename).first_or_404()
    return render_template('file.html', file=file)




@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit() and request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            f = form.file.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs', filename)
            f.save(file_path)
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', filename)
            generate_thumbnail(file_path, thumbnail_path)
            textbook = form.textbook.data
            subject = form.subject.data
            school = form.school.data
            professor = form.professor.data
            upload_date = datetime.utcnow()
            uploaded_file = Document(
                filename=filename,
                thumbnail=f'thumbnails/{filename}',
                textbook=textbook,
                subject=subject,
                school=school,
                professor=professor,
                upload_date=upload_date,
                user=current_user
            )
            db.session.add(uploaded_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('index', filename=filename))
    files = Document.query.all()
    return render_template('upload.html', form=form, files=files)


def generate_thumbnail(pdf_path, output_path, size=(200, 200)):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail(size)
    img.save(output_path, "PNG")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/generate_pdf/<int:file_id>')
def generate_pdf(file_id):
    file = Document.query.get_or_404(file_id)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnail', file.filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'thumbnail', file.filename)


@app.route('/like/<int:document_id>', methods=['POST'])
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


@app.route('/dislike/<int:document_id>', methods=['POST'])
@login_required
def dislike_document(document_id):
    document = Document.query.get_or_404(document_id)
    dislike = Dislike(user_id=current_user.id, document_id=document_id)
    db.session.add(dislike)
    document.ranking -= 1
    db.session.commit()
    flash('You have disliked this document.')
    return redirect(url_for('document', document_id=document_id))


@app.route('/suggest_edit/<int:document_id>', methods=['POST'])
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


@app.route('/upvote_suggested_edit', methods=['POST'])
@login_required
def upvote_suggested_edit():
    form = UpvoteSuggestedEditForm()
    if form.validate_on_submit():
        suggested_edit = SuggestedEdit.query.get_or_404(form.suggested_edit_id.data)
        suggested_edit.upvotes += 1
        db.session.commit()
        flash('You have upvoted a suggested edit!', 'success')

    return redirect(url_for('document', document_id=suggested_edit.document_id))


@app.route('/document/<int:document_id>/comment', methods=['POST'])
@login_required
def comment(document_id):
    document = Document.query.get_or_404(document_id)
    content = request.form.get('content')
    comment = Comment(user_id=current_user.id, document_id=document.id, content=content)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('document', document_id=document.id))


@app.route('/comments/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return jsonify(upvotes=comment.upvotes)

@app.route('/comments/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.downvotes += 1
    db.session.commit()
    return jsonify(downvotes=comment.downvotes)


@app.route('/comment/<int:file_id>', methods=['POST'])
@login_required
def comment_file(file_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, document_id=file_id)
        db.session.add(comment)
        db.session.commit()
        return render_template('comment.html', comment=comment)
    return redirect(url_for('file', file_id=file_id))
    
@app.route('/comments/document/<int:document_id>', methods=['GET'])
def get_comments(document_id):
    document = Document.query.get_or_404(document_id)
    comments = Comment.query.filter_by(document_id=document_id).all()
    return render_template('comments.html', document=document, comments=comments)
