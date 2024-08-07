from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from data.config import current_time
from datetime import datetime


class MainAPIView(APIView):
    def get(self, request: Request):
        return Response(
            {"about": "This API Created for hackathon of Mars IT School 🚀"}
        )


class DatetimeAPIView(APIView):
    def get(self, request: Request):
        return Response(
            datetime.strftime(current_time(time_zone=False), "%d-%m-%Y %H:%M:%S")
        )
