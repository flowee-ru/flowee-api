from rest_framework import generics

from . import serializers, models


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
