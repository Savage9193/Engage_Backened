from rest_framework import generics
from .models import Campaign
from .serializers import CampaignSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Campaign

class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

# class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    lookup_field = 'campaign_id'  # or 'pk' depending on your URL
class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    lookup_field = 'campaign_id'

    def patch(self, request, *args, **kwargs):
        print("PATCH HIT >>>")
        return self.partial_update(request, *args, **kwargs)
    def get_object(self):
        print("Looking for campaign:", self.kwargs['campaign_id'])
        return super().get_object()


@api_view(['POST'])
def approve_campaign(request, campaign_id):
    try:
        # campaign = Campaign.objects.get(id=campaign_id)
        campaign = Campaign.objects.get(campaign_id=campaign_id)

        campaign.approved = True  # or some similar field
        campaign.save()
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
# leads_app/views.py
from rest_framework import generics
from .models import Lead
from .serializers import LeadSerializer

class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Campaign
from .serializers import LeadSerializer
from rest_framework import status

@api_view(['GET'])
def get_leads_by_campaign(request, campaign_id):
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        leads = campaign.leads.all()
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)

