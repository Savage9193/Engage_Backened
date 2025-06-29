# leads_app/serializers.py

from rest_framework import serializers
from .models import Campaign, Lead

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'  # Or list them explicitly if you want more control
# class LeadSerializer(serializers.ModelSerializer):
#     campaign = serializers.SlugRelatedField(
#         slug_field='campaign_id',
#         queryset=Campaign.objects.all()
#     )
#     class Meta:
#         model = Lead
#         fields = '__all__'
class LeadSerializer(serializers.ModelSerializer):
        model = Lead
        fields = '__all__'
