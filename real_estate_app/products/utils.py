from real_estate_app import UPLOADED_FILES_DIR,os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import url_for

def save_file(f):
    filename = secure_filename(f.filename)
    filename = f'{datetime.now()}_{filename}'
    file_dir = (os.path.join(
        UPLOADED_FILES_DIR, filename
    ))
    f.save(file_dir)
    file_path = url_for('uploaded_file',filename=filename)
    return file_path