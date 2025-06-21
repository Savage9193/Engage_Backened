from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message_body = serializers.CharField()
    attachment = serializers.FileField(required=False)
