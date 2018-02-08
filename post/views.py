import random
import string

from flask import jsonify

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.db.models import Q

from post.serializers import PostSerializer, UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from post.models import Post, Profile
from rest_framework import viewsets

from django_filters import rest_framework as filters
from rest_framework.decorators import detail_route

from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt



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



class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        #fields = ["username", "email"]
        fields = {
            'title': ['icontains'],
            'content':['icontains']

        }



class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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




def search(request, query):


    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    #posts = Post.objects.all().filter(title=query)

    data = []

    for post in posts:
        data.append({"title":post.title})

    json_results = JsonResponse(data, safe=False)
    return json_results



from rest_framework import generics
class SearchList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        query = self.kwargs['query']

        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


        return posts