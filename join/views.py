from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Contacts, TaskItem, CustomUser, Subtask
from .serializers import ContactsSerializer, TaskItemSerializer, UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class LoginView(ObtainAuthToken):
    """
    View for user login and token generation.

    POST:
    - Validates the user's credentials and returns a token along with user details.
    - If the user does not have a token, it creates one.
    - Response includes user information such as email, initials, color, and full name.

    Parameters:
    - `request`: The HTTP request object containing login data (username and password).

    Returns:
    - JSON response with the token and user details.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'initials': user.initials,
            'color': user.color,
            'rememberlogin': user.rememberlogin,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'name': f"{user.first_name} {user.last_name}"
        })


class UserCreateView(generics.CreateAPIView):
    """
    View for creating a new user.

    Inherits from `CreateAPIView` and uses the `UserSerializer` to validate and create a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserGetView(generics.ListAPIView):
    """
    View for retrieving a list of all users.

    Inherits from `ListAPIView` and uses the `UserSerializer` to serialize the user data.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class TaskView(APIView):
    """
    API view for handling task-related operations.

    Methods:
    - GET: Retrieve a single task or a list of all tasks.
    - POST: Create a new task.
    - DELETE: Delete a specific task by ID.
    - PUT: Update a specific task by ID.
    """
    permission_classes = []

    def get(self, request, id=None, format=None):
        """
        Retrieve a single task or a list of all tasks.

        Parameters:
        - `id` (optional): The ID of a specific task to retrieve.

        Returns:
        - JSON response with the serialized task data.
        """
        if id:
            task = get_object_or_404(TaskItem, id=id)
            serializer = TaskItemSerializer(task)
        else:
            tasks = TaskItem.objects.all()
            serializer = TaskItemSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new task.

        Parameters:
        - `request`: The HTTP request object containing task data.

        Returns:
        - JSON response with the created task data.
        """
        serializer = TaskItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Delete a specific task by ID.

        Parameters:
        - `id`: The ID of the task to delete.

        Returns:
        - HTTP 204 No Content response on successful deletion.
        """
        task = get_object_or_404(TaskItem, id=id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id, format=None):
        """
        Update a specific task by ID.

        Parameters:
        - `id`: The ID of the task to update.
        - `request`: The HTTP request object containing updated task data.

        Returns:
        - JSON response with the updated task data.
        """
        task = get_object_or_404(TaskItem, id=id)
        serializer = TaskItemSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_removed_subtasks(self, task, incoming_subtask_ids):
        """
        Helper function to delete subtasks that are not in the incoming data.

        Parameters:
        - `task`: The task object.
        - `incoming_subtask_ids`: A set of subtask IDs that are expected to remain.
        """
        existing_subtasks = task.subtasks.all()
        for subtask in existing_subtasks:
            if subtask.id not in incoming_subtask_ids:
                subtask.delete()

    def update_or_create_subtask(self, task, subtask_data):
        """
        Helper function to update or create a subtask.

        Parameters:
        - `task`: The parent task object.
        - `subtask_data`: Data of the subtask to be updated or created.
        """
        subtask_id = subtask_data.get('id')
        if subtask_id:
            try:
                subtask = Subtask.objects.get(id=subtask_id, parent_task=task)
                subtask.title = subtask_data.get('title', subtask.title)
                subtask.subtaskStatus = subtask_data.get('subtaskStatus', subtask.subtaskStatus)
                subtask.save()
            except Subtask.DoesNotExist:
                Subtask.objects.create(
                    parent_task=task,
                    title=subtask_data.get('title', 'New Subtask'),
                    subtaskStatus=subtask_data.get('subtaskStatus', False)
                )
        else:
            Subtask.objects.create(
                parent_task=task,
                title=subtask_data.get('title', 'New Subtask'),
                subtaskStatus=subtask_data.get('subtaskStatus', False)
            )

    def handle_subtasks(self, task, subtasks_data):
        """
        Helper function to handle subtasks creation, update, and deletion.

        Parameters:
        - `task`: The parent task object.
        - `subtasks_data`: List of subtasks data to be processed.
        """
        incoming_subtask_ids = {subtask['id'] for subtask in subtasks_data if subtask.get('id')}
        self.delete_removed_subtasks(task, incoming_subtask_ids)
        for subtask_data in subtasks_data:
            self.update_or_create_subtask(task, subtask_data)


class ContactsView(APIView):
    """
    API view for handling contact-related operations.

    Methods:
    - GET: Retrieve a list of all contacts.
    - POST: Create a new contact.
    - DELETE: Delete a specific contact by ID.
    - PUT: Update a specific contact by ID.
    """
    permission_classes = []

    def get(self, request, format=None):
        """
        Retrieve a list of all contacts.

        Returns:
        - JSON response with the serialized contact data.
        """
        contacts = Contacts.objects.all()
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new contact.

        Parameters:
        - `request`: The HTTP request object containing contact data.

        Returns:
        - JSON response with the created contact data.
        """
        serializer = ContactsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        """
        Delete a specific contact by ID.

        Parameters:
        - `id`: The ID of the contact to delete.

        Returns:
        - HTTP 204 No Content response on successful deletion.
        """
        contact = get_object_or_404(Contacts, id=id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id, format=None):
        """
        Update a specific contact by ID.

        Parameters:
        - `id`: The ID of the contact to update.
        - `request`: The HTTP request object containing updated contact data.

        Returns:
        - JSON response with the updated contact data.
        """
        contact = get_object_or_404(Contacts, id=id)
        serializer = ContactsSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
