import uuid
from urllib.parse import parse_qs

from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers, models


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class MediamtxAuthView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data['path']
        live_key = parse_qs(request.data['query'])['k'][0]
        
        try:
            models.User.objects.get(username=username, live_key=uuid.UUID(live_key))
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return Response(status=status.HTTP_200_OK)
