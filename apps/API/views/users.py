from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from apps.users.models import User
from apps.API.serializers import UserSerializer


class UsersListApiView(APIView):
    def get(self, request: Request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)