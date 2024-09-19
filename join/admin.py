from django.contrib import admin


from .models import TaskItem, CustomUser, Subtask, Contacts

# from join.models import TaskItem

# Register your models here.
# admin.site.register(TaskItem)



@admin.register(TaskItem)
class TaskItemAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'category',)
    search_fields = ('title', 'description', 'category', 'author__username')
    # filter_horizontal = ('assignedTo',)

    def get_assigned_users(self, obj):
        return ", ".join([f"{user.first_name} {user.last_name}" for user in obj.assignedTo.all()])
    get_assigned_users.short_description = 'Assigned To'


# admin.site.register(Contact)
# """
# Admin interface configuration for the Contact model.
# """

@admin.register(CustomUser)
class CustomUserItemAdmin(admin.ModelAdmin):

    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined')


@admin.register(Subtask)
class SubtasksAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Subtask model.
    """

    list_display = ('id','title', 'subtaskStatus')

@admin.register(Contacts)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'initials', 'email', 'phone', 'color', 'taskassigned')    