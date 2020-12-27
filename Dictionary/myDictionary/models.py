from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=255)
    uname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    date=models.DateField()
    def __str__(self):
        return self.uname

class History(models.Model):
    uname=models.CharField(max_length=255)
    word=models.CharField(max_length=255)
    def __str__(self):
        return self.uname
