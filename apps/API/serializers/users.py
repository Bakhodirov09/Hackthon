from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'password',
                  'phone_number', 'contact',
                  'created_at', 'updated_at')

    def create(self, data):
        user = User.objects.create(
            full_name = data['full_name'],
            phone_number = data['phone_number'],
            password = data['password']
        )
        return user
