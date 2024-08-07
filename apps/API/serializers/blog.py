from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.API.models import Blog, Like, Comment
from apps.API.serializers.users import UserSerializer
from apps.users.models import User
from data.config import DOMAIN


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']


class BlogSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["id", "image", "title", "user", "user_id", "likes_count"]

    def get_likes_count(self, obj):
        return Like.objects.filter(blog=obj).count()

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = get_object_or_404(User, id=user_id)
        return Blog.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_id = validated_data.pop("user_id", None)
        if user_id:
            user = get_object_or_404(User, id=user_id)
            instance.user = user
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata["image"] = DOMAIN + instance.image.url

        return redata


class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user_id']


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = MiniUserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'user_id', 'created_at']
        
    def to_representation(self, instance):
        redata = super().to_representation(instance)
        try:
            redata["created_at"] = datetime.strftime(
                instance.created_at, "%d-%m-%Y %H:%M:%S"
            )
        except:
            redata["created_at"] = datetime.strftime(
                datetime.now(), "%d-%m-%Y %H:%M:%S"
            )

        return redata
