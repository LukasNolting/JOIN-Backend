from django.contrib import admin
from .models import TaskItem, CustomUser, Subtask, Contacts

@admin.register(TaskItem)
class TaskItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TaskItem model.

    This class customizes the Django admin interface for the TaskItem model, 
    allowing for better visibility and management of TaskItem objects.
    """

    list_display = ('id', 'title', 'category')
    """
    Specifies the fields to be displayed in the list view of TaskItem in the admin interface.
    It shows the ID, title, and category of each TaskItem.
    """

    search_fields = ('title', 'description', 'category', 'author__username')
    """
    Defines the fields that can be searched in the admin search bar.
    Allows administrators to search TaskItems by title, description, category, and author's username.
    """

    def get_assigned_users(self, obj):
        """
        Returns a comma-separated list of full names of users assigned to the task.

        Args:
            obj (TaskItem): The current TaskItem object.

        Returns:
            str: A string of assigned users' full names.

        This method is used to display the assigned users in a more readable format
        in the TaskItem list view. It concatenates the first and last names of 
        users assigned to the task.
        """
        return ", ".join([f"{user.first_name} {user.last_name}" for user in obj.assignedTo.all()])
    
    get_assigned_users.short_description = 'Assigned To'
    """
    Sets the label for the get_assigned_users method in the admin list display.
    This label will be used as the column header for the method output.
    """

@admin.register(CustomUser)
class CustomUserItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CustomUser model.

    This class customizes the Django admin interface for the CustomUser model, 
    enabling easy management of user accounts.
    """

    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined')
    """
    Specifies the fields to be displayed in the list view of CustomUser in the admin interface.
    It shows the email, first name, last name, username, and the date the user joined.
    """

@admin.register(Subtask)
class SubtasksAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Subtask model.

    This class customizes the Django admin interface for the Subtask model, 
    allowing for better visibility and management of Subtask objects.
    """

    list_display = ('id', 'title', 'subtaskStatus')
    """
    Specifies the fields to be displayed in the list view of Subtask in the admin interface.
    It shows the ID, title, and subtask status of each Subtask.
    """

@admin.register(Contacts)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contacts model.

    This class customizes the Django admin interface for the Contacts model, 
    enabling easy management of contact information.
    """

    list_display = ('id', 'firstname', 'lastname', 'initials', 'email', 'phone', 'color', 'taskassigned')
    """
    Specifies the fields to be displayed in the list view of Contacts in the admin interface.
    It shows the ID, first name, last name, initials, email, phone number, color, and task assignment status of each contact.
    """
