from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import Request
from .serializers import (RequestSerializer)
from webspiders.models import PostgreSpider

from django.apps import apps

from pprint import pprint


class SaveRequest(APIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserRequests(APIView):

    def post(self, request):
        user = apps.get_model('authentication', 'User').objects.get(id=request.user.id)
        requests = user.request_set.all()
        data = dict()
        for request in requests:
            data[request.id] = {
                'id': request.id,
                'connection_string': request.connection_string,
                'date': request.created_at
            }

        return Response(data, status=status.HTTP_200_OK)


class GetOldData(APIView):
    def post(self, request):
        requestObj = apps.get_model('request', 'Request').objects.get(id=request.data['id'])
        metadata = apps.get_model('metadata', 'Metadata').objects.get(id=requestObj.metadata_id)
        return Response(metadata.response, status=status.HTTP_200_OK)


class DeleteUserRequest(APIView):

    def post(self, request):
        user_id = 4
        user = apps.get_model('authentication', 'User').objects.get(id=user_id)
        request_user = apps.get_model('request', 'Request').objects.get(id=request.POST['request_id'])
        if request_user.user_id == user.id:
            request_user.delete()
            data = {
                'message': 'Request deleted.'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'User can not delete this request.'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
