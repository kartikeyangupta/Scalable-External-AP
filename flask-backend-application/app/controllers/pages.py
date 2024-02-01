import os
from flask import render_template, Blueprint, request, jsonify, flash, \
                 redirect, get_flashed_messages
from app.forms import *
from werkzeug.utils import secure_filename


blueprint = Blueprint('pages', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    # Method to get all files in our server
    if request.method == "GET":
        messages = get_flashed_messages()
        return render_template('pages/placeholder.uploads.html', 
                                messages=messages, files=['internet-bill.pdf', 'offer-letter.pdf']), 200
    
    

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
        file_path = os.path.join('uploads', filename)
        pdf_file.save(file_path)
        flash('PDF file uploaded !')
        return redirect('/', "message")
    return render_template('forms/upload.html', form=form)
