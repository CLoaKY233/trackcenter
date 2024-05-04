from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class permissionmanager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username