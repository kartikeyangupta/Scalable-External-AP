from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from flask_wtf.file import FileField, FileAllowed, FileRequired, SubmitField
from wtforms import FileField, SubmitField, validators
# from wtforms.validators import Required, FileAllowed, FileField


class UploadForm(FlaskForm):
    #validators=[FileRequired() , FileAllowed(['pdf'], 'PDF files only!')]
    # file = FileField('PDF File', validators=[Required(), FileAllowed(['pdf'])])
    file = FileField(u'PDF File')
    submit = SubmitField('upload')