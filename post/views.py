from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from post.serializers import PostSerializer, UserSerializer, ProfileSerializer, AttachmentSerializer
from django.contrib.auth.models import User
from post.models import Post, Profile, Attachment
from rest_framework import viewsets



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
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return posts



@csrf_exempt
def like_post(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        post = Post.objects.get(id=id)
        post.like = post.like + 1
        post.save()

    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

