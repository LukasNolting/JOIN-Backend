from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.conf import settings
from django.db import models

class TaskItem(models.Model):
    assignedTo = models.TextField()
    assignedToID = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks', blank=True)
    category = models.CharField(max_length=100)
    categoryboard = models.CharField(max_length=100)
    colors = models.TextField()
    description = models.TextField(blank=True)
    dueDate = models.DateField()
    prio = models.CharField(max_length=100)
    subtasks = models.TextField(default="No subtasks", blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title} - {self.description}'





class CustomUser(AbstractUser):
    initials = models.CharField(max_length=10)
    color = models.CharField(max_length=7)
    rememberlogin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
