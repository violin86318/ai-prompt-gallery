import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN', '***')
    DATABASE_ID = os.environ.get('DATABASE_ID', '***')
