# # leads_app/urls.py
# from django.urls import path
# from .views import LeadListCreateView
# from .views import CampaignListCreateView  # your view for handling campaigns

# urlpatterns = [
#     path('leads/', LeadListCreateView.as_view(), name='lead-list-create'),
#      path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
# ]

from django.urls import path
from .views import (
    get_leads_by_campaign,
    LeadListCreateView,
    CampaignListCreateView,
    CampaignDetailView,  # NEW,
)

urlpatterns = [
    path('leads/', LeadListCreateView.as_view(), name='lead-list-create'),
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('campaigns/<str:campaign_id>/', CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaigns/<str:campaign_id>/leads/', get_leads_by_campaign, name='get-leads-by-campaign'),  # NEW
]
