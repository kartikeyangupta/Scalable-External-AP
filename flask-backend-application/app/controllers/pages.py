import datetime
import os
from flask import render_template, Blueprint, request, jsonify, flash, \
                 redirect, get_flashed_messages
from app.forms import *
from werkzeug.utils import secure_filename
from app.models.files import File, Content
from app.extentions import db
from celery_tasks.tasks import upload_pdf_to_s3
import config

blueprint = Blueprint('pages', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    # Method to get all files in our server
    if request.method == "GET":
        messages = get_flashed_messages()
        pdfs,files = [], File.query.all()
        for file in files:
            pdfs.append({'name':file.name, 
                         'time_stamp':str(file.time_stamp),
                         'url': f'/pdf/{file.id}'})
            
        return render_template('pages/placeholder.uploads.html', 
                                messages=messages, files=pdfs), 200

@blueprint.route('/pdf/<id>', methods=['GET'])
def get_pdf_content(id):
    # Method to get all files in our server
    if request.method == "GET":
        content = Content.query.filter_by(file_id=id)
        file = File.query.filter_by(id=id).all()[0]
        return render_template('pages/placeholder.content.html', 
                                file_name = file.name, 
                                file_date = file.time_stamp,
                                content = content.content), 200

    

@blueprint.route('/add', methods=['POST', 'GET'])
def add_file():
    form = UploadForm(request.form)
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"message": "No file given"}), 404
        pdf_file = request.files['file']
        if pdf_file.filename == '' or pdf_file.filename.split('.')[1].lower() != 'pdf':
            flash('Wrong file being pushed')
            return redirect('/', "message")
        filename = secure_filename(pdf_file.filename)
        filetime = datetime.datetime.utcnow()
        new_file = File(name=filename)
        db.session.add(new_file)
        db.session.commit()
        db.session.close()
        filename = "_".join([filename, str(filetime)])
        file_path = os.path.join(config.FILE_DIR, filename)
        pdf_file.save(file_path)
        result_of_upload = upload_pdf_to_s3.delay(file_path, filename)
        # result_of_extratct = textract_from_pdf.delay(filename)
        flash('PDF file uploaded !')
        return redirect('/', "message")
    return render_template('forms/upload.html', form=form)
