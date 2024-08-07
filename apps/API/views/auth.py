from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..utils import post_template, registration_check, login_check
from apps.API.serializers import UserSerializer, TokenSerializer


class SignupApiView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request: Request):
        error = registration_check(request.data)
        if error is None:
            data, HttpStatus = post_template(
                request=request, serializerName=UserSerializer
            )
            return Response(data, status=HttpStatus)
        return Response(error, status=status.HTTP_401_UNAUTHORIZED)


class SiginApiView(APIView):
    @swagger_auto_schema(request_body=TokenSerializer)
    def post(self, request):
        error = login_check(request.data)
        serializer = TokenSerializer(data=request.data)
        if error is None:
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(error, status=status.HTTP_400_BAD_REQUEST)
