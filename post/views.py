import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

from post.serializers import PostSerializer, UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from post.models import Post, Profile
from rest_framework import viewsets

from django_filters import rest_framework as filters
from rest_framework.decorators import detail_route

from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.


def string_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        #fields = ["username", "email"]
        fields = {
            'email': ['contains'],
        }


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    #def perform_create(self, serializer):
        #user = User.objects.get(pk= self.request.data["user_id"])
        #serializer.save(user = user)


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('username', 'email')
    filter_class = UserFilter


    #def perform_create(self, serializer):
        #serializer.save(username = string_generator(), password = self.request.data["password"])



    @detail_route(methods=['post'])
    def auth_some_user(self, request):
        # u = User.objects.all().first()
        # if check_password('the default password', u.password):
        #     print ('user password matches default password')
        # else:
        #     print ('user a set custom password')
        user = User.objects.get(email = request.data['email'])

        return JsonResponse(user)



from django.forms.models import model_to_dict



@api_view(['POST'])
def auth_user(request):
    user = User.objects.get(email = request.data['email'])

    if check_password(request.data['password'], user.password):
            return JsonResponse(model_to_dict(user))
    else:
        return Response({"error": "error occurs"})

    # data = JSONParser().parse(request)
    # serializer = UserSerializer(data=data)
    #
    # if serializer.is_valid():
    #
    #     user = User.objects.get(email=serializer.data['email'])
    #     if check_password(serializer.data['password'], user.password):
    #         return Response(serializer.data)
    #     else:
    #         return Response({"error": "error occurs"})


