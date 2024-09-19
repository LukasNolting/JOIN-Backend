import json
from django.http import JsonResponse
from rest_framework import serializers
from .models import Contacts, CustomUser, Subtask, TaskItem
from django.contrib.auth import get_user_model

User = get_user_model()

class JSONListField(serializers.ListField):
    def to_representation(self, value):
        # Wenn value None ist, gib eine leere Liste zurück
        if value is None:
            return []
        # Lade den JSON-String als Liste
        return json.loads(value)

    def to_internal_value(self, data):
        # Speichere die Liste als JSON-String
        return data


class SubtaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField  # Verwende title im Modell
    subtaskStatus = serializers.BooleanField  # Verwende subtaskStatus im Modell

    class Meta:
        model = Subtask
        fields = ['id','title', 'subtaskStatus']


class TaskItemSerializer(serializers.ModelSerializer):
    assignedTo = JSONListField(child=serializers.CharField())
    colors = JSONListField(child=serializers.CharField())
    subtasks = SubtaskSerializer(many=True, required=False)
    assignedToID = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:
        model = TaskItem
        fields = '__all__'

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assignedToID = validated_data.pop('assignedToID', [])
        assignedTo = validated_data.pop('assignedTo', [])
        colors = validated_data.pop('colors', [])

        # Erstelle das TaskItem-Objekt
        task = TaskItem.objects.create(**validated_data)

        # Setze die Many-to-Many-Beziehung für assignedToID
        task.assignedToID.set(assignedToID)
        task.assignedTo = json.dumps(assignedTo)
        task.colors = json.dumps(colors)
        task.save()

        # Erstelle Subtasks
        for subtask_data in subtasks_data:
            Subtask.objects.create(parent_task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        print(subtasks_data)
        assignedToID = validated_data.pop('assignedToID', [])
        assignedTo = validated_data.pop('assignedTo', [])
        colors = validated_data.pop('colors', [])

        # Aktualisiere die TaskItem-Felder
        instance.assignedTo = json.dumps(assignedTo)  # Konvertiere in JSON-String
        instance.colors = json.dumps(colors)  # Konvertiere in JSON-String        
        instance.category = validated_data.get('category', instance.category)
        instance.categoryboard = validated_data.get('categoryboard', instance.categoryboard)
        instance.description = validated_data.get('description', instance.description)
        instance.dueDate = validated_data.get('dueDate', instance.dueDate)
        instance.prio = validated_data.get('prio', instance.prio)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Aktualisiere Many-to-Many-Beziehung
        instance.assignedToID.set(assignedToID)
        
        instance.subtasks.all().delete()

        # Verwalte Subtasks
        current_subtasks = instance.subtasks.all()
        incoming_subtasks = {subtask['title'] for subtask in subtasks_data}

        # Lösche Subtasks, die nicht mehr vorhanden sind
        for subtask in current_subtasks:
            if subtask.title not in incoming_subtasks:
                subtask.delete()

        # Erstelle oder aktualisiere bestehende Subtasks
        for subtask_data in subtasks_data:
            print(subtask_data)
            subtask_name = subtask_data.get('title')
            subtask_status = subtask_data.get('subtaskStatus')
            subtask_id = subtask_data.get('id')

            if subtask_id:
                try:
                    subtask = Subtask.objects.get(id=subtask_id, parent_task=instance)
                    subtask.title = subtask_name
                    subtask.subtaskStatus = subtask_status
                    subtask.save()
                       
                except Subtask.DoesNotExist:
                    Subtask.objects.create(parent_task=instance, title=subtask_name, subtaskStatus=subtask_status)
            else:
                Subtask.objects.create(parent_task=instance, title=subtask_name, subtaskStatus=subtask_status)

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(str(validated_data))
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
        return JsonResponse(validated_data)
    
class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'    