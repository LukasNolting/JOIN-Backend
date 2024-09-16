from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import TaskItem, CustomUser, Subtask
from .serializers import TaskItemSerializer, UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
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
            'name': user.first_name + " " + user.last_name
        })


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserGetView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class TaskView(APIView):
    permission_classes = []

    def get(self, request, id=None, format=None):
        # Wenn eine ID übergeben wird, das spezifische TaskItem abrufen
        if id:
            task = get_object_or_404(TaskItem, id=id)
            serializer = TaskItemSerializer(task)
        else:
            # Alle Tasks abrufen
            tasks = TaskItem.objects.all()
            serializer = TaskItemSerializer(tasks, many=True)
        
        # Gib die serialisierten Daten zurück
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        task = get_object_or_404(TaskItem, id=id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id, format=None):
        task = get_object_or_404(TaskItem, id=id)
        serializer = TaskItemSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_removed_subtasks(self, task, incoming_subtask_ids):
        existing_subtasks = task.subtasks.all()
        for subtask in existing_subtasks:
            if subtask.id not in incoming_subtask_ids:
                subtask.delete()

    def update_or_create_subtask(self, task, subtask_data):
        subtask_id = subtask_data.get('id')

        if subtask_id:
            try:
                subtask = Subtask.objects.get(id=subtask_id, parent_task=task)
                subtask.title = subtask_data.get('title', subtask.title)
                subtask.is_checked = subtask_data.get('is_checked', subtask.is_checked)
                subtask.save()
            except Subtask.DoesNotExist:
                Subtask.objects.create(
                    parent_task=task,
                    title=subtask_data.get('title', 'New Subtask'),
                    is_checked=subtask_data.get('is_checked', False)
                )
        else:
            Subtask.objects.create(
                parent_task=task,
                title=subtask_data.get('title', 'New Subtask'),
                is_checked=subtask_data.get('is_checked', False)
            )

    def handle_subtasks(self, task, subtasks_data):
        incoming_subtask_ids = {subtask['id'] for subtask in subtasks_data if subtask.get('id')}
        self.delete_removed_subtasks(task, incoming_subtask_ids)
        for subtask_data in subtasks_data:
            self.update_or_create_subtask(task, subtask_data)
