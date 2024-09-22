from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class TaskItem(models.Model):
    """
    Represents a task item with various attributes such as title, description, priority, and assigned users.

    Fields:
    - `assignedTo`: A JSON-encoded TextField containing the usernames of the assigned users.
    - `assignedToID`: Many-to-Many relationship with `CustomUser`, referencing the actual user objects assigned to this task.
    - `category`: The category of the task (e.g., "Work", "Personal").
    - `categoryboard`: The category board of the task, used for grouping under a specific board.
    - `colors`: A JSON-encoded TextField representing colors (can be used for visual organization).
    - `description`: A text description of the task.
    - `dueDate`: The due date of the task.
    - `prio`: The priority of the task (e.g., "High", "Medium", "Low").
    - `title`: The title of the task.

    Methods:
    - `__str__`: Returns a string representation of the task, consisting of its title and description.
    """
    assignedTo = models.TextField()
    assignedToID = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks', blank=True)
    category = models.CharField(max_length=100)
    categoryboard = models.CharField(max_length=100)
    colors = models.TextField()
    description = models.TextField(blank=True)
    dueDate = models.DateField()
    prio = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title} - {self.description}'


class Subtask(models.Model):
    """
    Represents a subtask related to a specific task item.

    Fields:
    - `title`: The title of the subtask.
    - `subtaskStatus`: The completion status of the subtask.
    - `parent_task`: ForeignKey relationship to a parent `TaskItem` instance.

    Relationships:
    - Each `Subtask` belongs to exactly one parent `TaskItem`.
    If the parent `TaskItem` is deleted, all related `Subtask` instances will also be deleted.
    """
    title = models.CharField(max_length=100)
    subtaskStatus = models.BooleanField(default=False)
    parent_task = models.ForeignKey(
        TaskItem,
        related_name='subtasks',
        on_delete=models.CASCADE
    )


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model with additional fields.

    Additional Fields:
    - `initials`: Initials of the user (up to 10 characters).
    - `color`: User-specific color in hex format (e.g., "#FFFFFF" for white).
    - `rememberlogin`: Indicates if the user wants to remember their login details (Boolean).

    Relationships:
    - Inherits all fields and methods from `AbstractUser`.
    """
    initials = models.CharField(max_length=10)
    color = models.CharField(max_length=7)
    rememberlogin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email


class Contacts(models.Model):
    """
    Represents a contact associated with a user.

    Fields:
    - `firstname`: First name of the contact.
    - `lastname`: Last name of the contact.
    - `fullname`: Full name of the contact.
    - `initials`: Initials of the contact.
    - `email`: Email address of the contact.
    - `phone`: Phone number of the contact.
    - `color`: User-specific color in hex format (e.g., "#FFFFFF" for white).
    - `id`: Primary key that is auto-generated.
    - `taskassigned`: Boolean field indicating whether a task is assigned to this contact.
    - `contactAssignedTo`: ForeignKey to a user (`CustomUser`) responsible for this contact.

    Relationships:
    - A `Contact` is linked to a specific `CustomUser`.
    """
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    initials = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    taskassigned = models.BooleanField(("Task assigned"), default=False)
    contactAssignedTo = models.ForeignKey(CustomUser, related_name='contacts', on_delete=models.CASCADE)
