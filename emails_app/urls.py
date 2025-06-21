from django.urls import path
from templates_app.views import SendEmailView  # adjust import path
from .views import SendCampaignEmailsView

urlpatterns = [
    path('', SendEmailView.as_view(), name='send-email'),
    #   path('send-campaign-emails/', SendCampaignEmailsView.as_view(), name='send-campaign-emails'),
    path('send/', SendCampaignEmailsView.as_view(), name='send-campaign-emails'),
]
