from django.db import models

# Create your models here.

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    issue_date = models.CharField(max_length=100)
    final_date = models.IntegerField()
    employment_length = models.FloatField()
    home_ownership = models.CharField(max_length=100)
    income_category = models.CharField(max_length=100)
    annual_income = models.IntegerField()
    loan_amount = models.IntegerField()
    term = models.CharField(max_length=100)
    application_type = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    interest_payments = models.CharField(max_length=100)
    loan_condition = models.CharField(max_length=100)
    interest_rate = models.FloatField()
    grade = models.CharField(max_length=10)
    debt_to_income_ratio = models.FloatField()
    total_payment = models.FloatField()
    total_principle_to_recover = models.FloatField()
    total_recoveries = models.FloatField()
    installment = models.FloatField()
    region = models.CharField(max_length=100)
    Email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.Email})"
