from rest_framework import serializers

from post.models import Post, Profile

from django.contrib.auth.models import User
import random
import string

def string_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))



class UserSerializer(serializers.ModelSerializer):
    #posts = serializers.StringRelatedField(many=True)
    #profile = serializers.PrimaryKeyRelatedField(read_only=True, source="profile.avatar_thumbnail")
    #profile = serializers.PrimaryKeyRelatedField(read_only=True)
    #profile = serializers.StringRelatedField(read_only=True)
    profile = serializers.ImageField(read_only=True,  source="profile.avatar")

    class Meta:
        model = User
        #fields = "__all__"
        fields = ["id", "url", "email", "password", "profile", "username"]
        extra_kwargs = {'password': {'write_only': True}}
        #read_only_fields = ['post_set']



    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):

        user = User.objects.get(email = validated_data['email'])

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        user.set_password(validated_data['password'])
        user.save()

        return instance






class PostSerializer(serializers.ModelSerializer):

    #user = UserSerializer(read_only=True)
    #user_avatar = serializers.ReadOnlyField(source='user.profile.avatar')
    #author = serializers.CharField(source='user.email')
    #author = UserSerializer()
    user_avatar = serializers.ImageField(read_only=True, source="user.profile.avatar")
    # depth = 1

    class Meta:
        model = Post
        #fields = "__all__"
        fields = ["url", "id", "title", "user", "user_avatar", "rating", "content", "like", "picture", "picture_thumbnail",
                  "video"]
        read_only_fields = ['picture_thumbnail']

        #expandable_fields = dict(
         #   user=UserSerializer,
        #)





class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["url", "id", "user", "avatar", "avatar_thumbnail"]
        read_only_fields = ['avatar_thumbnail']

