from rest_framework import serializers
from ..models import Post
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostModelSerializer(serializers.ModelSerializer):
    likes = UserModelSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'likes', 'author', 'like_count', 'is_liked')
    def get_author(self, obj):
        return obj.author.username
    def get_like_count(self, obj):
        return len(obj.likes.all())
    def get_is_liked(self, obj):
        user = self.context['request'].user 
        return True if user in obj.likes.all() else False