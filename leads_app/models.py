# from django.db import models
# import random
import uuid
from django.db import models
import random
from bson import ObjectId

# STATUS_CHOICES = [
#     ('Pending Checker', 'Pending Checker'),
#     ('Approved', 'Approved'),
#     ('Rejected', 'Rejected'),
#     ('Processed', 'Processed'),
# ]

# class Campaign(models.Model):
#     campaign_id = models.CharField( max_length=10, unique=True,blank=True, null=True)  # Changed to unique=True and added null=True
#     # campaign_id = models.CharField(max_length=10, primary_key=True, blank=True)  # No null=True for PK
#     # cust_id = models.CharField(max_length=100, blank=True, null=True)
#     # cust_email = models.EmailField(blank=True, null=True)
#     # customer_name = models.CharField(max_length=100, blank=True, null=True)
#     created_by = models.CharField(max_length=100)  # Fixed typo: 'blank=true' should be 'blank=True'
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Checker')
#     created_on = models.DateTimeField(auto_now_add=True)
#     checker = models.CharField(max_length=100, blank=True, null=True)
#     reviewed_on = models.DateTimeField(blank=True, null=True)
#     template_id = models.ForeignKey('templates_app.Template', on_delete=models.SET_NULL, null=True, blank=True)  # Changed from ForeignKey to CharField

#     def save(self, *args, **kwargs):
#         if not self.campaign_id:
#             while True:
#                 new_id = f"CM{random.randint(100000, 999999)}"
#                 if not Campaign.objects.filter(campaign_id=new_id).exists():
#                     self.campaign_id = new_id
#                     break
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.campaign_id} - {self.customer_name}"

# class Lead(models.Model):
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='leads')
#     name = models.CharField(max_length=100)
#     email = models.EmailField()

#     def __str__(self):
#         return self.email

def generate_campaign_id():
    return f'CM{random.randint(10000, 99999)}'

STATUS_CHOICES = [
    ('Pending Checker', 'Pending Checker'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Processed', 'Processed'),
]

class Campaign(models.Model):
    campaign_id = models.CharField(primary_key=True, max_length=20, default=generate_campaign_id, editable=False)
    created_by = models.CharField(max_length=100, default='system')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Checker')
    created_on = models.DateTimeField(auto_now_add=True)
    checker = models.CharField(max_length=100, blank=True, null=True)
    reviewed_on = models.DateTimeField(blank=True, null=True)
    template_id = models.ForeignKey('templates_app.Template', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.campaign_id}"

def generate_lead_id():
    return str(ObjectId())

class Lead(models.Model):
    lead_id = models.CharField(primary_key=True, max_length=24, default=generate_lead_id, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.email
