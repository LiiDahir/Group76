from django.db import models

# Create your models here.
class Images(models.Model):
    id=models.CharField(max_length=100,primary_key=True)
    images=models.ImageField(upload_to="dataset/check/")