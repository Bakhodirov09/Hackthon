from rest_framework import status, serializers

from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

from apps.users.models import User


def registration_check(form_data):
    phone_number = form_data.get("phone_number")
    password = form_data.get("password")

    if len(password) < 8:
        return {"error": "Пароль должен быть больше 8 символов!"}
    if User.objects.filter(phone_number=phone_number).exists():
        return {"error": "Номер телефона уже зарегистрирован!"}
    if len(phone_number) > 13:
        return {"error": "Номер должен состоять из 13 символов! Пример: +998*********"}
    elif len(phone_number) < 13:
        return {"error": "Номер должен состоять из 13 символов! Пример: +998*********"}

    return None


def login_check(form_data):
    phone_number = form_data.get("phone_number")
    password = form_data.get("password")

    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return {"error": "Неверный номер телефона!"}

    if not check_password(password, user.password):
        return {"error": "Неверный пароль!"}

    return None


def get_template(request, model: models.Model, 
                serializer: serializers.Serializer | serializers.ModelSerializer):
    queryset = model.objects.all()
    serializer = serializer(queryset, many=True)
    return serializer.data


def get_one_template(request, model: models.Model, serializer, pk):
    blog = get_object_or_404(model, pk=pk)
    serializer = serializer(blog)
    return serializer.data


def post_template(request, 
                serializer: serializers.Serializer | serializers.ModelSerializer):
    serializer = serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ({"data": serializer.data}, status.HTTP_201_CREATED)
    return ({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


def put_template(request, model: models.Model, serializer, pk):
    if not model.objects.filter(id=pk).exists():
        return ({"error": "Data does not exists!"}, status.HTTP_204_NO_CONTENT)

    instance = model.objects.get(id=pk)
    serializer = serializer(data=request.data)
    
    if serializer.is_valid():
        serializer.update(instance, serializer.validated_data)
        return (
            {f"data": serializer.data},
            status.HTTP_205_RESET_CONTENT,
        )

    return (serializer.errors, status.HTTP_400_BAD_REQUEST)


def delete_template(request, model: models.Model, pk):
    if not model.objects.filter(id=pk).exists():
        return ({"error": "Data does not exists!"}, status.HTTP_204_NO_CONTENT)

    model.objects.get(id=pk).delete()
    return ({"data": f"Deleted data by id [{pk}]"}, status.HTTP_418_IM_A_TEAPOT)
