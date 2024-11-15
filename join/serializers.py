import json
from django.http import JsonResponse
from rest_framework import serializers
from .models import Contacts, CustomUser, Subtask, TaskItem
from django.contrib.auth import get_user_model

User = get_user_model()

class JSONListField(serializers.ListField):
    """
    Custom field for handling JSON-encoded lists in the model.

    This serializer field is used to serialize a JSON string stored in the 
    database into a Python list and vice versa.
    """

    def to_representation(self, value):
        """
        Convert the JSON string into a Python list.

        Args:
            value (str): JSON-encoded string representing a list.

        Returns:
            list: Python list representation of the input value. 
            Returns an empty list if value is None.
        """
        if value is None:
            return []
        return json.loads(value)

    def to_internal_value(self, data):
        """
        Convert the input list into a JSON string.

        Args:
            data (list): Python list to be converted into a JSON string.

        Returns:
            str: JSON-encoded string representation of the list.
        """
        return data


class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtask model.

    This serializer handles the conversion of Subtask model instances 
    into JSON format and vice versa.
    """

    title = serializers.CharField()
    subtaskStatus = serializers.BooleanField()

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'subtaskStatus']


class TaskItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskItem model.

    Handles the serialization and deserialization of TaskItem objects, 
    including nested subtasks and assigned users.
    """

    assignedTo = JSONListField(child=serializers.CharField())
    colors = JSONListField(child=serializers.CharField())
    subtasks = SubtaskSerializer(many=True, required=False)
    assignedToID = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = TaskItem
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new TaskItem instance.

        Handles the creation of a TaskItem, including associated subtasks and assigned users.

        Args:
            validated_data (dict): Validated data from the request.

        Returns:
            TaskItem: Newly created TaskItem instance.
        """
        subtasks_data = validated_data.pop('subtasks', [])
        assignedToID = validated_data.pop('assignedToID', [])
        assignedTo = validated_data.pop('assignedTo', [])
        colors = validated_data.pop('colors', [])

        # Create the TaskItem object
        task = TaskItem.objects.create(**validated_data)

        # Set many-to-many relationship for assigned users
        task.assignedToID.set(assignedToID)
        task.assignedTo = json.dumps(assignedTo)
        task.colors = json.dumps(colors)
        task.save()

        # Create subtasks
        for subtask_data in subtasks_data:
            Subtask.objects.create(parent_task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        """
        Update an existing TaskItem instance.

        Handles updating of a TaskItem, including associated subtasks and assigned users.

        Args:
            instance (TaskItem): The existing TaskItem instance.
            validated_data (dict): Validated data from the request.

        Returns:
            TaskItem: Updated TaskItem instance.
        """
        subtasks_data = validated_data.pop('subtasks', [])
        assignedToID = validated_data.pop('assignedToID', [])
        assignedTo = validated_data.pop('assignedTo', [])
        colors = validated_data.pop('colors', [])

        # Update TaskItem fields
        instance.assignedTo = json.dumps(assignedTo)
        instance.colors = json.dumps(colors)
        instance.category = validated_data.get('category', instance.category)
        instance.categoryboard = validated_data.get('categoryboard', instance.categoryboard)
        instance.description = validated_data.get('description', instance.description)
        instance.dueDate = validated_data.get('dueDate', instance.dueDate)
        instance.prio = validated_data.get('prio', instance.prio)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Update many-to-many relationship
        instance.assignedToID.set(assignedToID)

        # Delete all existing subtasks and recreate them based on new data
        instance.subtasks.all().delete()

        # Manage subtasks
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')

            # If the subtask exists, update it
            if subtask_id:
                try:
                    subtask = Subtask.objects.get(id=subtask_id, parent_task=instance)
                    subtask.title = subtask_data.get('title')
                    subtask.subtaskStatus = subtask_data.get('subtaskStatus')
                    subtask.save()
                except Subtask.DoesNotExist:
                    # If the subtask does not exist, create a new one
                    Subtask.objects.create(parent_task=instance, **subtask_data)
            else:
                # If no subtask ID is provided, create a new subtask
                Subtask.objects.create(parent_task=instance, **subtask_data)

        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Handles the serialization and deserialization of CustomUser objects.
    Provides special handling for password fields to ensure they are write-only.
    """

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new CustomUser instance.

        Args:
            validated_data (dict): Validated data from the request.

        Returns:
            CustomUser: Newly created CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            initials=validated_data['initials'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            color=validated_data['color'],
            rememberlogin=validated_data['rememberlogin'],
        )
        return user

    def get(self, validated_data):
        """
        Custom get method (if needed).

        Args:
            validated_data (dict): Validated data from the request.

        Returns:
            JsonResponse: JSON response with the validated data.
        """
        return JsonResponse(validated_data)


class ContactsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contacts model.

    Handles the serialization and deserialization of Contacts objects.
    """

    class Meta:
        model = Contacts
        fields = '__all__'
