from leads_app.models import DraftLead
from django.core.mail import send_mail

def execute_campaign_emails(campaign_id):
    leads = DraftLead.objects.filter(campaign_id=campaign_id, status='Approved')
    for lead in leads:
        if lead.template_id:
            # Load HTML content from file
            html_path = lead.template_id.html_file.path
            with open(html_path, 'r') as f:
                html_content = f.read()

            send_mail(
                subject="Campaign Email",
                message='',
                from_email='noreply@engage.ai',
                recipient_list=[lead.cust_email],
                html_message=html_content
            )

            lead.status = 'Processed'
            lead.save()
