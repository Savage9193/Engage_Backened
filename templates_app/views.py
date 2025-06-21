from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Template
from .serializers import TemplateSerializer
from rest_framework.response import Response
from rest_framework import status

class TemplateListCreateView(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    parser_classes = (MultiPartParser, FormParser)

    # def perform_create(self, serializer):
    #     # Generate template ID dynamically (e.g., ET0001, ET0002, etc.)
    #     last_template = Template.objects.order_by('-template_id').first()
    #     if last_template:
    #         last_id = int(last_template.template_id.replace("ET", ""))
    #         new_id = f"ET{last_id + 1:04d}"
    #     else:
    #         new_id = "ET0001"

    #     serializer.save(template_id=new_id)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from .models import Template
from .serializers import TemplateSerializer

class TemplateDeleteView(DestroyAPIView):
    queryset = Template.objects.all()
    lookup_field = 'template_id'
    serializer_class = TemplateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Template deleted successfully"}, status=status.HTTP_200_OK)


# templates_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage

class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        to_email = request.data.get('to_email')
        subject = request.data.get('subject')
        message_body = request.data.get('message_body')
        attachment = request.FILES.get('attachment')

        if not all([to_email, subject, message_body]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        email = EmailMessage(subject, message_body, to=[to_email])
        email.content_subtype = 'html'

        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        try:
            email.send()
            return Response({"message": "Email sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
