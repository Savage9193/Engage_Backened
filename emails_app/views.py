# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.core.mail import EmailMessage
# # from .serializers import EmailSerializer

# # class SendEmailView(APIView):
# #     def post(self, request):
# #         serializer = EmailSerializer(data=request.data)
# #         if serializer.is_valid():
# #             to_email = serializer.validated_data['to_email']
# #             subject = serializer.validated_data['subject']
# #             body = serializer.validated_data['message_body']
# #             attachment = request.FILES.get('attachment')

# #             email = EmailMessage(
# #                 subject=subject,
# #                 body=body,
# #                 from_email=None,  # will use EMAIL_HOST_USER
# #                 to=[to_email],
# #             )
# #             email.content_subtype = "html"  # Send HTML content

# #             if attachment:
# #                 email.attach(attachment.name, attachment.read(), attachment.content_type)

# #             try:
# #                 email.send()
# #                 return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
# #             except Exception as e:
# #                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import EmailMessage
# from templates_app.models import Template
# from leads_app.models import Campaign

# class SendCampaignEmailsView(APIView):
#     def post(self, request):
#         campaign_id = request.data.get("campaign_id")
#         template_id = request.data.get("template_id")
        
# # 8923200046    
#         # Validate Template
#         try:
#             template = Template.objects.get(template_id=template_id)
#         except Template.DoesNotExist:
#             return Response({"error": "Template not found."}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch leads by campaign
#         leads = Campaign.objects.filter(campaign_id=campaign_id) 
#         if not leads.exists():
#             return Response({"error": "No leads found for this campaign."}, status=status.HTTP_400_BAD_REQUEST)

#         # Prepare email content
#         subject = f"Campaign {campaign_id}"
#         html_content = template.html_file.read().decode("utf-8") if template.html_file else template.description

#         sent_to = []
#         for lead in leads:
#             email = EmailMessage(
#                 subject=subject,
#                 body=html_content,
#                 to=[lead.email],
#             )
#             email.content_subtype = "html"
#             email.send()
#             sent_to.append(lead.email)

#         return Response({
#             "message": f"Emails sent to all leads under {campaign_id}",
#             "sent_to": sent_to
#         }, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from leads_app.models import Campaign
from django.conf import settings
import mimetypes

class SendCampaignEmailsView(APIView):
    def post(self, request):
        campaign_id = request.data.get("campaign_id")
        approved_by = request.data.get("approved_by")

        if not campaign_id or not approved_by:
            return Response({"error": "campaign_id and approved_by are required"}, status=400)

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)

        if campaign.status != "Approved":
            return Response({"error": "Campaign is not approved yet"}, status=400)

        if not campaign.template_id:
            return Response({"error": "No template assigned to this campaign"}, status=400)

        leads = campaign.leads.all()
        if not leads:
            return Response({"error": "No leads found for this campaign"}, status=400)

        # Load HTML content
        html_path = campaign.template_id.html_file.path
        mime_type, _ = mimetypes.guess_type(html_path)
        if mime_type != 'text/html':
            return Response({"error": "Uploaded file is not an HTML file."}, status=400)
        try:
            with open(html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            return Response({"error": "Failed to decode HTML content. Please upload a valid UTF-8 encoded HTML file."}, status=400)

        # with open(html_path, 'r', encoding='utf-8') as file:
        #     html_content = file.read()

        # Send email to each lead
        for lead in leads:
            email = EmailMessage(
                subject=f"Campaign Email - {campaign_id}",
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[lead.email]
            )
            email.content_subtype = "html"
            email.send()

        # Mark campaign as processed
        campaign.status = "Processed"
        campaign.save()

        return Response({"message": f"Emails sent to all leads in campaign {campaign_id}."}, status=200)
