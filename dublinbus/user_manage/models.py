from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    # lname = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    # phone = models.CharField(max_length=30, default='', null=True)
    email = models.CharField(max_length=30)
    question = models.CharField(max_length=30)
    answer = models.CharField(max_length=30)
    gender = models.CharField(max_length=6)
    regtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name + self.email


