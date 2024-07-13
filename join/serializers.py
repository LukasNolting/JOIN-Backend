from django.http import JsonResponse
from rest_framework import serializers
from .models import CustomUser, TaskItem
from rest_framework import serializers
from django.conf import settings

# class TaskItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskItem
#         fields = '__all__'
        

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
 
 
 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TaskItem
import json

User = get_user_model()

class JSONListField(serializers.ListField):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        return json.dumps(data)

class TaskItemSerializer(serializers.ModelSerializer):
    assignedTo = JSONListField(child=serializers.CharField())
    colors = JSONListField(child=serializers.CharField())
    subtasks = JSONListField(child=serializers.CharField(), required=False)
    assignedToID = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:
        model = TaskItem
        fields = '__all__'

    def create(self, validated_data):
        assignedToID = validated_data.pop('assignedToID')
        task = TaskItem.objects.create(**validated_data)
        task.assignedToID.set(assignedToID)
        return task

    def update(self, instance, validated_data):
        assignedToID = validated_data.pop('assignedToID')
        instance.assignedTo = validated_data.get('assignedTo', instance.assignedTo)
        instance.category = validated_data.get('category', instance.category)
        instance.categoryboard = validated_data.get('categoryboard', instance.categoryboard)
        instance.colors = validated_data.get('colors', instance.colors)
        instance.description = validated_data.get('description', instance.description)
        instance.dueDate = validated_data.get('dueDate', instance.dueDate)
        instance.prio = validated_data.get('prio', instance.prio)
        instance.subtasks = validated_data.get('subtasks', instance.subtasks)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        instance.assignedToID.set(assignedToID)
        return instance
