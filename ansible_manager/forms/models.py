from django.db import models

# Create your models here.
class Exercise(models.Model):
    name=models.CharField(max_length=200)
    pdf_file=models.FileField(upload_to='exercises/')

    def __str__(self):
        return self.name
        
