from django.http import JsonResponse
from rest_framework import serializers
from .models import CustomUser

# class TaskItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskItem
#         fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # write_only_fields = ('password',)
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