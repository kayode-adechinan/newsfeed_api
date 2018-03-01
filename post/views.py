from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import PostSerializer, UserSerializer, ProfileSerializer, AttachmentSerializer
from django.contrib.auth.models import User
from post.models import Post, Profile, Attachment
from rest_framework import viewsets
from post.helpers import send_password_reset_mail, generate_user_password


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class AttachmentView(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SearchList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):

        query = self.kwargs['query']

        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__username__icontains=query) | Q(user__email__icontains=query) 
        )
        return posts


class SearchUserPost(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):

        userID = self.kwargs['userID']

        posts = Post.objects.filter( user_id=userID  )
        return posts


class UserPasswordReset(APIView):
    """
    Set user password.
    """
    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, email, format=None):
        user = self.get_object(email)
        password = generate_user_password()
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        send_password_reset_mail(user.email, password)
        return Response(serializer.data)