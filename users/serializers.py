from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'userId',
            'firstName',
            'lastName',
            'email',
            'password',
            'phone'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            # use indexing for mandatory fields
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            password=validated_data['password'],
            # use get for optional fields
            phone=validated_data.get('phone', ''),
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)    

