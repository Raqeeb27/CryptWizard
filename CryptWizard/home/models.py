from django.db import models

# Create your models here.
class Registered_Users(models.Model):
    username = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50, unique=True)
    lastname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)