import os
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = basedir + '/app/uploads/'
VORLAGEN_FOLDER = basedir + '/app/vorlagen/'
ALLOWED_EXTENSIONS = set(['xml'])
HOME = "/as"

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DEBUG_MODE=True