from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "super secret key"

ALLOWED_EXTENSIONS = ['pdf']

app.config['UPLOAD_FOLDER'] = '/Users/swaroop/Desktop/upload'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload_file():
    return render_template('file.html')


@app.route('/uploaded', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("successful")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('try_again'))


@app.route('/try_again')
def try_again():
    return render_template('try_again.html')


app.run()
