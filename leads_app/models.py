from django.db import models

STATUS_CHOICES = [
    ('Pending Checker', 'Pending Checker'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Processed', 'Processed'),
]

class Campaign(models.Model):
    campaign_id = models.CharField( max_length=10, unique=True) 
    # campaign_id = models.CharField(max_length=10, primary_key=True) ,
    cust_id = models.CharField(max_length=100)
    cust_email = models.EmailField()
    customer_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Checker')
    created_on = models.DateTimeField(auto_now_add=True)
    checker = models.CharField(max_length=100, blank=True, null=True)
    reviewed_on = models.DateTimeField(blank=True, null=True)
    template_id = models.ForeignKey('templates_app.Template', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.campaign_id} - {self.customer_name}"
class Lead(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.email