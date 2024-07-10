from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import generics
from .models import CustomUser



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

  

        
# class TaskItemView(APIView):

#     # authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = []

#     def get(self, request, format=None):

#         todos = TaskItem.objects.all()
#         serializer = TaskItemSerializer(todos, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = TaskItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

        