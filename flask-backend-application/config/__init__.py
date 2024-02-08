import os


BASE_DIR = os.path.abspath(os.path.dirname(__name__))
FILE_DIR = os.path.abspath(os.path.dirname(__name__))+'/uploads'
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
# DB_URL = 'postgresql+psycopy2://{user}:{pw}@{url}/{db}'.format(user='',pw='', url='', db='')
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
AWS_ACCESS_KEY_ID = os.environ.get('AWS_SECRET_ACCESS_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = 'text-extract-bucket-mumbai'