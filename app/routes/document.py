from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User, Document, School, Comment, Dislike, Like
from werkzeug.urls import url_parse
from PIL import Image
from werkzeug.utils import secure_filename
import os
import PyPDF2
from pdf2image import convert_from_path
import fitz  # this is pymupdf
from datetime import datetime
from app import db
document_bp = Blueprint('document', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


@document_bp.route('/', methods=['GET', 'POST'])
@document_bp.route('/index', methods=['GET', 'POST'])
def index():
    documents = Document.query.all()
    users = User.query.all()  # Fetch all users
    users_list = list(users)
    return render_template('index.html', title='Home', documents=documents, users=users_list)
    
@document_bp.route('/profile', methods=['GET', 'POST'])
def penis():
    documents = Document.query.all()
    users = User.query.all()  # Fetch all users
    users_list = list(users)
    return render_template('profile.html', title='Home', user=users_list)


@document_bp.route('/document/<int:document_id>', methods=['GET', 'POST'])
def document(document_id):
    document = Document.query.get_or_404(document_id)
    suggested_edits = SuggestedEdit.query.filter_by(document_id=document_id).order_by(SuggestedEdit.upvotes.desc()).all()
    if suggested_edits and suggested_edits[0].upvotes > document.upvotes:
        document.title = suggested_edits[0].suggested_title
        document.subject = suggested_edits[0].suggested_subject
        db.session.commit()
    return render_template('document.html', title=document.title, document=document)


@document_bp.route('/files/<filename>')
def uploaded_file(filename):
    file = UploadedFile.query.filter_by(filename=filename).first_or_404()
    return render_template('file.html', file=file)


@document_bp.route('/upload', methods=['GET', 'POST'])
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
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdfs', filename)
            f.save(file_path)
            thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnails', filename)
            generate_thumbnail(file_path, thumbnail_path)
            textbook = form.textbook.data
            subject = form.subject.data
            professor = form.professor.data
            upload_date = datetime.utcnow()
            uploaded_file = Document(
                filename=filename,
                thumbnail=f'thumbnails/{filename}',
                textbook=textbook,
                subject=subject,
                professor=professor,
                upload_date=upload_date,
                user=current_user
            )
            db.session.add(uploaded_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('document.index', filename=filename))
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


@document_bp.route('/generate_pdf/<int:file_id>')
def generate_pdf(file_id):
    file = Document.query.get_or_404(file_id)
    pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnail', file.filename)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], 'thumbnail', file.filename)
