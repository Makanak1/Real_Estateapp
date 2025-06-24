from rest_framework import serializers
from django.contrib.auth import get_user_model
user = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('name', 'email', 'is_realtor')
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name', 'email','password']  # Add more fields as needed
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
        }
        
    def update(self, instance, validated_data):
        # Prevent password from being saved here
        validated_data.pop('password', None)
        return super().update(instance, validated_data)
