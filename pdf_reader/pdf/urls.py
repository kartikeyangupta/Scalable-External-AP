from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:file_id>", views.view_pdf_content, name="view_pdf_content"),
    path("add", views.uploadpdf, name="uploadpdf"),
]