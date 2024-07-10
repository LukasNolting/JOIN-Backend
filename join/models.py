from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class TaskItem(models.Model):
#     assignedTo = models.CharField(max_length=100)
#     assignedToID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     category = models.CharField(max_length=100)
#     categoryboard = models.CharField(max_length=100)
#     colors = models.CharField(max_length=100)
#     description = models.CharField(max_length=100)
#     dueDate = models.DateField()
#     prio = models.CharField(max_length=100)
#     subtasks = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
    
#     def __str__(self):
#         return f'{self.title} - {self.description}'


class CustomUser(AbstractUser):
    initials = models.CharField(max_length=10)
    color = models.CharField(max_length=7)
    rememberlogin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
