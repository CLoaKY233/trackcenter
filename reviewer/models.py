from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class projectgrade(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0, verbose_name='Grade')
    remarks = models.TextField(blank=True, null=True, default="No remarks yet", verbose_name='Remarks')
    is_graded = models.BooleanField(default=False, verbose_name='Is Graded')

    def __str__(self):
        return f'{self.user.username} Grade: {self.grade}'



