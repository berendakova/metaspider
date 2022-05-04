from rest_framework import serializers

from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(source='metadata.response', read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'connection_string', 'data']

    def create(self, validated_data):
        # user сидит в validated_data (передается так serializer.save(user=request.user))
        return Request.objects.create_request(**validated_data)
