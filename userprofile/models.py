from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userprofile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_githubid=models.CharField(max_length=70,default="NOT PROVIDED")
    project_name=models.CharField(max_length=25,default="NOT PROVIDED")
    project_about=models.CharField(max_length=300,default="NOT PROVIDED")
    project_link=models.CharField(max_length=100,default="NOT PROVIDED")

    def __str__(self):
        return self.user.username