from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os
from resume import Resume, JobDescription, DividePaths, SortId
from pathlib import Path

app = Flask(__name__)

jobDescription = JobDescription('/Users/swaroop/Desktop/swaroop/jds/jobDescription1.txt')

app.secret_key = "super secret key"

app.config['UPLOAD_RESUME'] = '/Users/swaroop/Desktop/Resumes'

app.config['UPLOAD_JD'] = '/Users/swaroop/Desktop/JD'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jd/upload')
def jd_upload():
    return render_template('jobdescription.html')


@app.route('/jd_uploaded', methods=['POST', 'GET'])
def jd_uploaded():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_JD'], filename))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('try_again'))


@app.route('/try_again')
def try_again():
    return render_template('try_again.html')

# @app.route('/resume/:id:')

@app.route('/resume/upload')
def upload_files():
    return render_template('resumes.html')


@app.route('/resumes_uploaded', methods=['POST', 'GET'])
def res_uploaded():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename_jd = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_RESUME'], filename_jd))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('try_again'))


@app.route('/resume/compare')
def compare_to_jds():

    flag = 0
    jd_path = app.config['UPLOAD_JD']
    paths = Path(jd_path).glob('*.txt')
    for path in paths:
        jd_path = path
        flag += 1
        break
    paths = Path(app.config['UPLOAD_RESUME']).glob('*.pdf')
    for path in paths:
        flag += 1
        break
    if flag != 2:
        return "<h1>Please upload both JobDescription and Resumes</h1>"
    else:
        jd = JobDescription(jd_path)
        id_list = list()
        divide_obj = DividePaths(app.config['UPLOAD_RESUME'])
        for file in divide_obj.path_list:
            resume = Resume(file)
            resume.compare_with(jd)
            id_list.append(resume.id())
        sort_id = SortId()
        scores = sort_id.find(sort_id.sort_scores(id_list))

        return render_template('id_score.html', result=scores)


app.run()
