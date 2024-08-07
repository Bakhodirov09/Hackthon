from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.API.models import Blog, Like, Comment
from apps.users.models import User
from apps.API.serializers.blog import BlogSerializer, CommentSerializer, LikeSerializer
from apps.API.utils import (
    get_template,
    post_template,
    get_one_template,
    put_template,
    delete_template,
)


class BlogListCreateAPIView(APIView):
    def get(self, request):
        data = get_template(request, Blog, BlogSerializer)
        return Response({"data": data})

    @swagger_auto_schema(request_body=BlogSerializer)
    def post(self, request):
        data, HttpStatus = post_template(request, BlogSerializer)
        return Response(data, status=HttpStatus)


class BlogDetailAPIView(APIView):
    def get(self, request, id):
        data = get_one_template(request, Blog, BlogSerializer, id)
        return Response({"data": data})

    def delete(self, request, id):
        data, HttpStatus = delete_template(request, Blog, id)
        return Response(data, status=HttpStatus)


class LikeToggleAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LikeSerializer)
    def post(self, request, blog_id):
        user_id = request.data.get("user_id")
        blog = get_object_or_404(Blog, pk=blog_id)
        user = get_object_or_404(User, pk=user_id)

        like = Like.objects.filter(user=user, blog=blog).first()

        if like:
            if like.like_status:
                like.delete()
                return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
            else:
                like.like_status = True
                like.save()
                return Response(
                    {"like_status": like.like_status}, status=status.HTTP_200_OK
                )
        else:
            # Create a new like if none exists
            Like.objects.create(user=user, blog=blog, like_status=True)
            return Response({"like_status": True}, status=status.HTTP_201_CREATED)


class CommentListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        comments = Comment.objects.filter(blog_id=blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, blog_id):
        user_id = request.data.get("user_id")
        text = request.data.get("text")

        if not user_id or not text:
            return Response(
                {"error": "user_id and text are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, id=user_id)
        blog = get_object_or_404(Blog, id=blog_id)

        comment = Comment.objects.create(user=user, blog=blog, text=text)
        serializer = CommentSerializer(comment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CommentDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        data = get_one_template(request, Comment, CommentSerializer, id)
        return Response({"data": data})

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data, HttpStatus = delete_template(request, Comment, id)
        return Response(data, status=HttpStatus)
