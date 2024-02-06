from django.db import models

class PDF_File(models.Model):
    name = models.CharField(max_length=30)
    timestamp = models.DateTimeField("date published", auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.timestamp}'

class File_Content(models.Model):
    content = models.TextField()
    file_name = models.ForeignKey(PDF_File, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content}-{self.file_name}'