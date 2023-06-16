
import os
from decouple import config
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

class Config(object):

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app1.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = r'C:\Users\cpcay\OneDrive\Desktop\StudyBuddy\app\static'
    PDF_FOLDER = r'C:\Users\cpcay\OneDrive\Desktop\StudyBuddy\app\static'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    
    
    


                



    
