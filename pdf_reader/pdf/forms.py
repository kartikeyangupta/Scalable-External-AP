from django import forms

class PDFFileForm(forms.Form):
    file_name = forms.FileField(required=True, label="Upload PDF File", validators=[])