import json
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
import os
from flask import Flask
from flask_cors import CORS

from process import processCSV

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return {"message": 'Sanitization Server for SDM : Sever Online'}


@app.route('/processCSV', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return ""
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return processCSV(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
    return json.dumps({"bru": "hu"})


# listen
if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True)
