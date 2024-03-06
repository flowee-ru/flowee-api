import requests
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException

from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    captcha = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.User
        fields = ['username', 'password', 'captcha', 'tokens']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    def create(self, validated_data):
        user = models.User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_captcha(self, value):
        response = requests.post('https://hcaptcha.com/siteverify', data={
            'secret': settings.HCAPTCHA_SECRET_KEY,
            'response': value,
        })
        response_data = response.json()
        if not response_data['success']:
            raise serializers.ValidationError('hCaptcha validation failed')
        return value


class UserSerializer(serializers.ModelSerializer):
    live = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.User
        fields = ['username', 'display_name', 'bio', 'live_name', 'live']
    
    def get_live(self, obj):
        try:
            response = requests.get(f'{settings.MEDIAMTX_API_URL}/v3/paths/get/live/{obj.get_username()}')
        except requests.RequestException:
            raise APIException('Failed to get data from streaming server')
        
        if response.status_code == 200:
            data = response.json()
            return {
                'ready_time': data['readyTime'],
                'viewers': len(data['readers']),
                'url': f'{settings.MEDIAMTX_HLS_URL}/live/{obj.get_username()}/index.m3u8',
            }
        else:
            return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token
