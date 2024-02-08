from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, validators

class UploadForm(FlaskForm):
    file = FileField('PDF File')
    submit = SubmitField('upload')