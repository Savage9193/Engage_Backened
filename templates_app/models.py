from django.db import models

PRODUCT_CHOICES = [
    ('Loan', 'Loan'),
    ('Insurance', 'Insurance'),
]

class Template(models.Model):
    template_id = models.CharField(primary_key=True, max_length=10, unique=True)  # e.g., ET0001
    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES)
    description = models.CharField(max_length=30)
    html_file = models.FileField(upload_to='templates_html/')
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.template_id

    